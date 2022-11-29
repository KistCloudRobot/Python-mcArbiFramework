import stomp
import threading
import json

from arbi_agent.ltm.communication.adaptor.ltm_message_adaptor import LTMMessageAdaptor
from arbi_agent.ltm.ltm_message import LTMMessage
from arbi_agent.configuration import LTMMessageAction, ServerContents


class ActiveMQLTMAdaptor(LTMMessageAdaptor, stomp.ConnectionListener):
    def __init__(self, broker_host, broker_port, ltm_uri, queue):
        self.ltm_uri = ltm_uri
        self.queue = queue
        self.is_alive = True
        self.lock = threading.Lock()

        hosts = [(broker_host, broker_port)]
        self.conn = stomp.Connection(host_and_ports=hosts)
        self.conn.set_listener('', self)

    def start(self):
        self.conn.connect(wait=True)
        self.conn.subscribe(destination=self.ltm_uri + "/message", id=self.ltm_uri)

    def close(self):
        if self.conn is not None:
            self.conn.disconnect()

        self.is_alive = False

    def on_message(self, frame):
        data = json.loads(frame.body)

        if data["command"] != "Long-Term-Memory":
            print("unknown message command : " + str(data))
            return

        client = data["client"]
        action = LTMMessageAction[data["action"]]
        content = data["content"]
        conversation_id = data["conversationID"]

        agent_message = LTMMessage(client=client, action=action, content=content, conversation_id=conversation_id)
        self.queue.enqueue(agent_message)

    def send(self, message):
        data = dict()

        data["client"] = message.get_client()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()

        data["command"] = "Long-Term-Memory"

        json_message = json.dumps(data)

        self.lock.acquire()

        self.conn.send(body=json_message, destination=ServerContents.SERVER_URI)

        self.lock.release()
