from abc import *


class LTMMessageAdaptor(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, message):
        pass
