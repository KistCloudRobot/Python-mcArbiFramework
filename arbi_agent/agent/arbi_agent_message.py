import uuid
import time
import threading

from arbi_agent.configuration import AgentMessageAction


class ArbiAgentMessage:

    def __init__(self, **kwds):

        if ("sender" not in kwds
                or "receiver" not in kwds
                or "action" not in kwds
                or "content" not in kwds
        ):
            print("ERROR : not enough message component")
            return

        self.sender = kwds["sender"]
        self.receiver = kwds["receiver"]
        self.action = kwds["action"]
        self.content = kwds["content"]

        if "conversation_id" in kwds:
            self.conversation_id = kwds["conversation_id"]
        else:
            self.conversation_id = str(uuid.uuid4())

        if "timestamp" in kwds:
            self.timestamp = kwds["timestamp"]
        else:
            self.timestamp = int(time.time() * 1000)

        if (self.action is AgentMessageAction.Query
                or self.action is AgentMessageAction.Request
                or self.action is AgentMessageAction.Subscribe
                or self.action is AgentMessageAction.RequestStream):
            self.lock = threading.Condition()
            self.response = None

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_action(self):
        return self.action

    def get_content(self):
        return self.content

    def get_conversation_id(self):
        return self.conversation_id

    def get_response(self):
        with self.lock:
            while self.response is None:
                self.lock.wait()
            return self.response.get_content()

    def set_response(self, response):
        with self.lock:
            self.response = response
            self.lock.notify()

    def get_timestamp(self):
        return self.timestamp
