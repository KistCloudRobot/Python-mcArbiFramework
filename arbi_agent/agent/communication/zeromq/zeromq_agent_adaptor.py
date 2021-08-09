import zmq
import threading
import json

from arbi_agent.agent.communication.arbi_message_adaptor import ArbiMessageAdaptor
from arbi_agent.agent.communication.arbi_message_queue import ArbiMessageQueue
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.configuration import AgentMessageAction


class ZeroMQAgentAdaptor(ArbiMessageAdaptor):
    def __init__(self, broker_url: str, adaptor_url: str, queue: ArbiMessageQueue):
        self.url = adaptor_url
        self.queue = queue

        self.context = zmq.Context.instance()

        self.producer = self.context.socket(zmq.DEALER)
        self.producer.setsockopt(zmq.IDENTITY, bytes(self.url, encoding="utf-8"))
        self.producer.connect(broker_url)

        self.consumer = self.context.socket(zmq.DEALER)
        self.consumer.setsockopt(zmq.IDENTITY, bytes(self.url + "/message", encoding="utf-8"))
        self.consumer.connect(broker_url)

        self.is_alive = True

        self.message_received_thread = threading.Thread(target=self.message_received, args=())
        self.message_received_thread.daemon = True
        self.message_received_thread.start()

    def close(self):
        if self.producer is not None:
            self.producer.close()

        if self.consumer is not None:
            self.consumer.close()

        if self.context is not None:
            self.context.destroy()

        self.is_alive = False

    def message_received(self):
        while self.is_alive:
            self.consumer.recv_string()
            message = self.consumer.recv_string()

            print("receive message in agent")
            print("\tmessage\t\t:", message)

            data = json.loads(message)

            if data["command"] != "Arbi-Agent":
                return

            sender = data["sender"]
            receiver = data["receiver"]
            action = AgentMessageAction[data["action"]]
            content = data["content"]
            conversation_id = data["conversationID"]

            agent_message = ArbiAgentMessage(sender=sender, receiver=receiver, action=action,
                                             content=content, conversation_id=conversation_id)
            self.queue.enqueue(agent_message)

    def send(self, message: ArbiAgentMessage):
        data = dict()

        data["sender"] = message.get_sender()
        data["receiver"] = message.get_receiver()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()

        data["command"] = "Arbi-Agent"

        json_message = json.dumps(data)

        print("send message in agent")
        print("\tmessage\t\t:", json_message)

        self.producer.send_multipart([bytes("", encoding="utf-8"),
                                      bytes(str(json_message), encoding="utf-8")])
