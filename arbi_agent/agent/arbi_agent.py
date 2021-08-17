from abc import *
from typing import Union

from arbi_agent.agent.communication.arbi_agent_message_toolkit import ArbiAgentMessageToolkit
from arbi_agent.agent.logger.logger_manager import LoggerManager
from arbi_agent.agent.arbi_agent_message import ArbiAgentMessage


class ArbiAgent(metaclass=ABCMeta):
    def __init__(self):
        self.agent_url: Union[None, str] = None
        self.broker_url: Union[None, str] = None
        self.broker_type: Union[None, int] = None
        self.running: bool = False
        self.message_toolkit: Union[None, ArbiAgentMessageToolkit] = None

    def initialize(self, **kwds):
        print("Arbi Agent Initialze")

        self.agent_url = kwds["agent_url"]
        self.broker_type = kwds["broker_type"]

        if "broker_url" in kwds:
            self.broker_url = kwds["broker_url"]
        else:
            self.broker_url = "tcp://172.16.165.225:61616"

        print("Agent URL: " + self.agent_url)
        print("Broker URL: " + self.broker_url)

        self.running = True
        self.message_toolkit = ArbiAgentMessageToolkit(self.broker_url, self.agent_url, self, self.broker_type)
        LoggerManager.get_instance().init_logger_manager(self.broker_url, self.agent_url, self.broker_type, self)

        print("Agent start! : " + self.agent_url)

        self.on_start()

    def close(self):
        self.message_toolkit.close()

    def is_running(self):
        return self.running

    def get_full_message(self) -> ArbiAgentMessage:
        return self.message_toolkit.get_full_message()

    def on_start(self):
        pass

    # def on_stop(self):
    #     pass

    def on_data(self, sender: str, data: str):
        pass

    def on_request(self, sender: str, request: str) -> str:
        return "ignored"

    def on_query(self, sender: str, query: str) -> str:
        return "ignored"

    def on_subscribe(self, sender: str, subscribe: str) -> str:
        return "ignored"

    def on_unsubscribe(self, sender: str, unsubscribe: str):
        pass

    def on_notify(self, sender: str, notification: str):
        pass

    def on_system(self, sender: str, data: str):
        print('[ data ]' + data)
        LoggerManager.get_instance().change_filter_option(data)

    # def on_request_stream(self, sender, rule):
    #     return "no data stream"

    # def on_release_stream(self, sender, stream_id):
    #     pass

    # def on_stream(self, data):
    #     pass

    def send(self, receiver: str, data: str):
        self.message_toolkit.send(receiver, data)

    def request(self, receiver: str, request: str) -> str:
        return self.message_toolkit.request(receiver, request)

    def query(self, receiver: str, query: str) -> str:
        return self.message_toolkit.query(receiver, query)

    def subscribe(self, receiver: str, subscribe: str) -> str:
        return self.message_toolkit.subscribe(receiver, subscribe)

    def unsubscribe(self, receiver: str, content: str):
        self.message_toolkit.unsubscribe(receiver, content)

    def notify(self, receiver: str, notification: str):
        self.message_toolkit.notify(receiver, notification)

    def system(self, receiver: str, data: str):
        self.message_toolkit.system(receiver, data)

    # def request_stream(self, receiver, rule):
    #     return self.message_toolkit.request_stream(receiver, rule)

    # def release_stream(self, receiver, stream_id):
    #     self.message_toolkit.release_stream(receiver, stream_id)
