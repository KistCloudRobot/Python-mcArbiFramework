from abc import *


class LTMMessageListener(metaclass=ABCMeta):

    @abstractmethod
    def message_received(self, message):
        pass
