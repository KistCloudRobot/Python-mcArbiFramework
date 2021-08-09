from abc import *


class ArbiMessageAdaptor(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message):
        pass
