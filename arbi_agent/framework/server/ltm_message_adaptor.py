from abc import *
from arbi_agent.framework.server.message_adaptor import MessageAdaptor


class LTMMessageAdaptor(MessageAdaptor, metaclass=ABCMeta):

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def notify(self, message):
        pass
