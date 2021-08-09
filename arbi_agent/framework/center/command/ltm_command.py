from abc import *


class LTMCommand(metaclass=ABCMeta):

    @abstractmethod
    def deploy(self, ltm_service, author, fact):
        pass
