import threading
import time
import uuid


class LTMMessage:

    def __init__(self, **kwds):

        if ("client" not in kwds 
            or "action" not in kwds 
            or "content" not in kwds
        ):
            print("ERROR : not enough message component")
            return

        self.client = kwds["client"]
        self.action = kwds["action"]
        self.content = kwds["content"]
        
        if "conversation_id" in kwds:
            self.conversation_id = kwds["conversation_id"]
        else:
            self.conversation_id = str(uuid.uuid4())

        self.lock = threading.Condition()
        self.response = None

    def get_conversation_id(self):
        return self.conversation_id

    def get_client(self):
        return self.client

    def get_content(self):
        return self.content

    def get_action(self):
        return self.action

    def get_response(self):
        with self.lock:
            while self.response is None:
                self.lock.wait()
            return self.response.get_content()

    def set_response(self, response):
        with self.lock:
            self.response = response
            self.lock.notify()
