import zmq
import threading
import json

from ...ltm_message import LTMMessage
from ..ltm_message_adaptor import LTMMessageAdaptor
from arbi_agent.configuration import LTMMessageAction


class ZeroMQLTMAdaptor(LTMMessageAdaptor):
    def __init__(self, broker_url, adaptor_url, queue):
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

        self.lock = threading.Lock()

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
            try:
                self.consumer.recv()
                message = self.consumer.recv()

                data = json.loads(str(message, encoding="utf-8"))

                if data["command"] != "Long-Term-Memory":
                    return

                client = data["client"]
                action = LTMMessageAction[data["action"]]
                content = data["content"]
                conversation_id = data["conversationID"]

                agent_message = LTMMessage(client=client, action=action, content=content, conversation_id=conversation_id)
                self.queue.enqueue(agent_message)

            except AssertionError as e:
                print("what?")
                continue

            except Exception as e:
                print('whaaat?')
                continue

    def send(self, message):
        data = dict()

        data["client"] = message.get_client()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()

        data["command"] = "Long-Term-Memory"

        self.lock.acquire()

        json_message = json.dumps(data)

        self.producer.send_multipart([bytes("", encoding="utf-8"), bytes(str(json_message), encoding="utf-8")])

        self.lock.release()
