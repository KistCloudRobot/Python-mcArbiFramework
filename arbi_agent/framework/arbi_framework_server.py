from arbi_agent.framework.server import message_service

from typing import Union


class ArbiFrameworkServer:
    def __init__(self, server_name: str, broker_type: int):
        self.server_name = server_name
        self.broker_type = broker_type
        self.message_service = message_service.MessageService(self.server_name, self.broker_type)

    def start(self, broker_url: str, center_url: str = None):
        self.message_service.initialize(broker_url, center_url)
        print("Server start : " + self.server_name)
