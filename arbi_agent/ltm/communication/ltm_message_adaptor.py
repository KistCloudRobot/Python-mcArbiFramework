from abc import *


class LTMMessageAdaptor(metaclass=ABCMeta):
    
    @abstractmethod
    def send(self, message):
        pass
