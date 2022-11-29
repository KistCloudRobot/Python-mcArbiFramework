import time

import stomp
import threading
import json

from arbi_agent.agent.communication.adaptor.arbi_message_adaptor import ArbiMessageAdaptor
from arbi_agent.agent.communication.arbi_message_queue import ArbiMessageQueue
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage
from arbi_agent.configuration import AgentMessageAction, ServerContents


class ActiveMQAgentAdaptor(ArbiMessageAdaptor, stomp.ConnectionListener):
    def __init__(self, broker_host: str, broker_port: int, agent_uri: str, queue: ArbiMessageQueue, daemon=True):
        self.agent_uri = agent_uri
        self.queue = queue
        self.is_alive = True
        self.lock = threading.Lock()

        hosts = [(broker_host, broker_port)]
        self.conn = stomp.Connection(host_and_ports=hosts)
        self.conn.set_listener('', self)

    def start(self):
        self.conn.connect(wait=True)
        self.conn.subscribe(destination=self.agent_uri + "/message", id=self.agent_uri)

    def close(self):
        if self.conn is not None:
            self.conn.disconnect()

        self.is_alive = False

    def on_message(self, frame):
        data = json.loads(frame.body)

        if data["command"] != "Arbi-Agent":
            print("unknown message command : " + str(data))
            return

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

    def send(self, message: ArbiAgentMessage):
        data = dict()

        data["sender"] = message.get_sender()
        data["receiver"] = message.get_receiver()
        data["action"] = message.get_action().name
        data["content"] = message.get_content()
        data["conversationID"] = message.get_conversation_id()
        data["timestamp"] = message.get_timestamp()
        data["command"] = "Arbi-Agent"

        json_message = json.dumps(data)

        self.lock.acquire()

        self.conn.send(body=json_message, destination=ServerContents.SERVER_URI)

        self.lock.release()
