from abc import *


class ArbiMessageAdaptor(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, message):
        pass

