from abc import *


class Function(metaclass=ABCMeta):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_expression_size(self):
        pass

    @abstractmethod
    def get_expression(self):
        pass

    @abstractmethod
    def evaluate(self, binding):
        pass
