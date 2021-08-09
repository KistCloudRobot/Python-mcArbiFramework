from abc import *
from arbi_agent.framework.server.message_adaptor import MessageAdaptor


class MessageDeliverAdaptor(MessageAdaptor, metaclass=ABCMeta):
    @abstractmethod
    def deliver(self, message):
        pass
