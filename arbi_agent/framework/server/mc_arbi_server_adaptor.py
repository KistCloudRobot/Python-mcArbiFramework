import threading
import time
import json
import zmq

from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.ltm.ltm_message import LTMMessage
from arbi_agent.framework.server.message_deliver_adaptor import MessageDeliverAdaptor
from arbi_agent.framework.server.ltm_message_adaptor import LTMMessageAdaptor
from arbi_agent.configuration import AgentMessageAction, LTMMessageAction


class McArbiServerAdaptor(MessageDeliverAdaptor, LTMMessageAdaptor):

    def __init__(self, service: "MessageService"):
        self.service = service
        self.socket_map = dict()
        self.router_map = dict()

        self.context = None
        self.consumer = None

        self.on_message_thread = threading.Thread(target=self.on_message, args=())
        self.on_message_thread.daemon = True

    def initialize(self, server_url: str, broker_url: str):
        self.context = zmq.Context.instance()
        self.consumer = self.context.socket(zmq.ROUTER)
        self.consumer.bind(server_url)
        self.on_message_thread.start()

    def get_agent_id(self, address: str) -> str:
        adr_list = address.split('/')
        return adr_list[2]

    def router_connected(self, server_name: str, ip_address: str):
        dealer = self.context.socket(zmq.DEALER)
        dealer.setsockopt(zmq.IDENTITY, bytes("center", encoding="utf-8"))
        dealer.connect(ip_address)
        self.socket_map[server_name] = dealer
        self.router_map[server_name] = ip_address
        send_data: str = self.generate_publish_message()
        for agent_name in self.socket_map.keys():
            socket = self.socket_map.get(agent_name)
            socket.send_multipart([bytes("", encoding="utf-8"),
                                   bytes(send_data, encoding="utf-8")])

    def generate_publish_message(self) -> str:
        message = dict()
        message["sender"] = "center"
        message["command"] = "Address-List"
        router_list = list()
        for key in self.router_map.keys():
            router_info = {"name": key,
                           "address": self.router_map.get(key)}
            router_list.append(router_info)
        message["content"] = router_list
        return json.dumps(message)

    def connect_router(self, server_name: str, ip_address: str):
        dealer = self.context.socket(zmq.DEALER)
        dealer.setsockopt(zmq.IDENTITY, bytes(server_name, encoding="utf-8"))
        dealer.connect(ip_address)

    def route(self, server_name: str, message: str):
        self.socket_map.get(server_name).send(message)
        print("routed : " + server_name + " : " + message)

    def handle_message(self, sender_id: str, message: str):
        data = json.loads(message)

        if data["command"] is None:
            print("server zeromq adaptor: no command")
            return

        if data["command"].startswith("Arbi-Agent"):
            sender = data["sender"]
            receiver = data["receiver"]
            action = AgentMessageAction[data["action"]]
            content = data["content"]
            conversation_id = data["conversationID"]
            arbi_message = ArbiAgentMessage(sender=sender, receiver=receiver, action=action,
                                            content=content, conversation_id=conversation_id)
            self.service.message_received(arbi_message)
        elif data["command"].startswith("Long-Term-Memory"):
            client = data['client']
            action = LTMMessageAction[data['action']]
            content = data['content']
            query_id = data['conversationID']
            ltm_message = LTMMessage(client=client, action=action,
                                     content=content, conversation_id=query_id)
            self.service.message_received(ltm_message)
        elif data["command"].startswith("RegisterRouter"):
            sender: str = data["sender"]
            address: str = data["address"]
            self.router_connected(sender, address)

    def on_message(self):
        while True:
            time.sleep(1)
            sender_id = self.consumer.recv_string()
            self.consumer.recv_string()
            message = self.consumer.recv_string()
            print('receive on mc server: ' + message)
            self.handle_message(sender_id, message)

    def send(self, message: LTMMessage):
        receiver_url = message.get_client()
        destination = receiver_url + "/message"

        data = dict()
        data["client"] = message.get_client()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["command"] = "Long-Term-Memory"

        json_message = json.dumps(data)

        print("send message : " + json_message)

        self.consumer.send_multipart([bytes(destination, encoding="utf-8"),
                                      bytes("", encoding="utf-8"),
                                      bytes(json_message, encoding="utf-8")])

    def notify(self, message: LTMMessage):
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

    def deliver(self, message: ArbiAgentMessage):
        receiver_url = message.get_receiver()
        destination = receiver_url + "/message"

        data = dict()
        data["sender"] = message.get_sender()
        data["receiver"] = message.get_receiver()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["command"] = "Arbi-Agent"

        json_message = json.dumps(data)
        print("send: " + json_message)
        self.consumer.send_multipart([bytes(destination, encoding="utf-8"),
                                      bytes("", encoding="utf-8"),
                                      bytes(json_message, encoding="utf-8")])
