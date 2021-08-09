from abc import *


class MessageAdaptor(metaclass=ABCMeta):
    @abstractmethod
    def initialize(self, server_url: str, broker_url: str):
        pass
