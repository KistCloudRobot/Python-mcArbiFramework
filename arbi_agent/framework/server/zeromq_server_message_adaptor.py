import threading
import time
import zmq
import json

from arbi_agent.framework.server.ltm_message_adaptor import LTMMessageAdaptor
from arbi_agent.framework.server.message_deliver_adaptor import MessageDeliverAdaptor
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.ltm.ltm_message import LTMMessage
from arbi_agent.configuration import AgentMessageAction, LTMMessageAction


class ZeroMQServerMessageAdaptor(LTMMessageAdaptor, MessageDeliverAdaptor):
    def __init__(self, service: "MessageService", agent_name: str):
        self.service = service
        self.socket_map = dict()
        self.agent_name = agent_name

        self.lock = threading.Lock()

        self.on_message_thread = threading.Thread(target=self.on_message, args=())
        self.on_message_thread.daemon = True

        self.context = None
        self.consumer = None
        self.producer = None

        self.server_url = None
        self.center_url = None

    def initialize(self, server_url: str, center_url: str):
        self.context = zmq.Context.instance()
        self.consumer = self.context.socket(zmq.ROUTER)

        self.server_url = server_url
        self.consumer.bind(self.server_url)

        self.center_url = center_url
        self.producer = self.context.socket(zmq.DEALER)
        self.producer.setsockopt(zmq.IDENTITY, bytes(self.agent_name, encoding="utf-8"))
        self.producer.connect(self.center_url)
        print("center server connected : " + self.center_url)

        self.send_init_message()

        self.on_message_thread.start()

    def send_init_message(self):
        message = dict()
        message["sender"] = self.agent_name
        message["address"] = self.server_url
        message["command"] = "RegisterRouter"

        json_message = json.dumps(message)
        print("send init message : " + json_message)
        self.producer.send_multipart([bytes("", encoding="utf-8"),
                                      bytes(json_message, encoding="utf-8")])

    def get_agent_name(self, address: str) -> str:
        split_address = address.split("/")
        if len(split_address) > 3:
            return split_address[3]
        else:
            return ""

    def connect_router(self, server_name: str, ip_address: str):
        dealer = self.context.socket(zmq.DEALER)
        dealer.connect(ip_address)
        self.socket_map[server_name] = dealer

    def route(self, server_name: str, message: str):
        self.socket_map.get(server_name).send(message)
        print("routed : " + server_name + " : " + message)

    def handle_router_list(self, data: dict):
        router_list = data["content"]
        for router_info in router_list:
            name = router_info["name"]
            address = router_info["address"]
            if name != self.agent_name and name not in self.socket_map.keys():
                socket = self.context.socket(zmq.DEALER)
                socket.setsockopt(zmq.IDENTITY, bytes(self.agent_name, encoding="utf-8"))
                socket.connect(address)
                self.socket_map[name] = socket
                print("router added", name, ":", address)

    def on_message(self):
        while True:
            time.sleep(1)
            sender_id = self.consumer.recv_string()
            self.consumer.recv_string()
            message = self.consumer.recv_string()
            print("receive message in server")
            print("\tsender id\t:", sender_id)
            print("\tmessage\t\t:", message)
            self.handle_message(sender_id, message)

    def handle_message(self, sender_id, message):
        data = json.loads(message)

        command = data["command"]

        if command is None:
            print("server zeromq adaptor: no command")
            return

        if command.startswith("Arbi-Agent"):
            sender = data["sender"]
            receiver = data["receiver"]
            action = AgentMessageAction[data["action"]]
            content = data["content"]
            conversation_id = data["conversationID"]
            arbi_message = ArbiAgentMessage(sender=sender, receiver=receiver, action=action,
                                            content=content, conversation_id=conversation_id)
            self.service.message_received(arbi_message)
        elif command.startswith("Long-Term-Memory"):
            client = data['client']
            action = LTMMessageAction[data['action']]
            content = data['content']
            query_id = data['conversationID']
            ltm_message = LTMMessage(client=client, action=action,
                                     content=content, conversation_id=query_id)
            self.service.message_received(ltm_message)
        elif command.startswith("Address-List"):
            self.handle_router_list(data)

    def send(self, message):
        receiver_url = message.get_client()
        destination = receiver_url + "/message"

        data = dict()
        data["client"] = message.get_client()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["command"] = "Long-Term-Memory"

        json_message = json.dumps(data)

        self.consumer.send_multipart([bytes(destination, encoding="utf-8"),
                                      bytes("", encoding="utf-8"),
                                      bytes(json_message, encoding="utf-8")])

    def notify(self, message):
        pass

    def deliver(self, message):
        data = dict()
        data["sender"] = message.get_sender()
        data["receiver"] = message.get_receiver()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["command"] = "Arbi-Agent"

        json_message = json.dumps(data)

        receiver_url = message.get_receiver()
        receiver_name = self.get_agent_name(receiver_url)

        if receiver_name == self.agent_name:
            destination = receiver_url + "/message"

            print("deliver message in server")
            print("\tdestination\t:", destination)
            print("\tmessage\t\t:", json_message)

            self.consumer.send_multipart([bytes(destination, encoding="utf-8"),
                                          bytes("", encoding="utf-8"),
                                          bytes(json_message, encoding="utf-8")])
        else:
            print("routing message in server")
            print("\treceiver\t:", receiver_name)
            print("\tmessage\t\t:", json_message)

            self.socket_map.get(receiver_name).send_multipart([bytes("", encoding="utf-8"),
                                                               bytes(json_message, encoding="utf-8")])
