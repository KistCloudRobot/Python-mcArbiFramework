import time

import zmq
import threading
import json

from arbi_agent.agent.communication.arbi_message_adaptor import ArbiMessageAdaptor
from arbi_agent.agent.communication.arbi_message_queue import ArbiMessageQueue
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.configuration import AgentMessageAction


class ZeroMQAgentAdaptor(ArbiMessageAdaptor):
    def __init__(self, broker_url: str, adaptor_url: str, queue: ArbiMessageQueue, daemon=True):
        self.url = adaptor_url
        self.queue = queue

        self.context = zmq.Context.instance()

        self.producer = self.context.socket(zmq.DEALER)
        self.producer.setsockopt(zmq.IDENTITY, bytes(self.url, encoding="utf-8"))
        self.producer.connect(broker_url)

        self.consumer = self.context.socket(zmq.DEALER)
        self.consumer.setsockopt(zmq.IDENTITY, bytes(self.url + "/message", encoding="utf-8"))
        self.consumer.connect(broker_url)
        self.poller = zmq.Poller()
        self.poller.register(self.consumer, zmq.POLLIN)

        self.is_alive = True

        self.lock = threading.Lock()

        self.message_received_thread = threading.Thread(target=self.message_received, args=())
        self.message_received_thread.daemon = daemon
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
            sockets = dict(self.poller.poll(2000))
            if sockets:
                while True:
                    time.sleep(0.1)
                    message = self.consumer.recv_string()
                    try:
                        data = json.loads(message)
                        break
                    except:
                        continue

                if data["command"] != "Arbi-Agent":
                    print("WTF : " + str(data))
                    continue

                sender = data["sender"]
                receiver = data["receiver"]
                action = AgentMessageAction[data["action"]]
                content = data["content"]
                conversation_id = data["conversationID"]
                timestamp = data["timestamp"]

                agent_message = ArbiAgentMessage(sender=sender, receiver=receiver, action=action,
                                                 content=content, conversation_id=conversation_id,
                                                 timestamp=timestamp)
                self.queue.enqueue(agent_message)
            else:
                # print("what?")
                pass

    def send(self, message: ArbiAgentMessage):
        data = dict()

        data["sender"] = message.get_sender()
        data["receiver"] = message.get_receiver()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["timestamp"] = message.get_timestamp()

        data["command"] = "Arbi-Agent"

        self.lock.acquire()

        json_message = json.dumps(data)

        self.producer.send_multipart([bytes("", encoding="utf-8"),
                                      bytes(str(json_message), encoding="utf-8")])

        self.lock.release()

