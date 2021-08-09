from abc import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arbi_agent.model.value.value import Value
    from arbi_agent.model.variable import Variable
    from arbi_agent.model.function.function import Function
    from arbi_agent.model.generalized_list import GeneralizedList


class Expression(metaclass=ABCMeta):
    @abstractmethod
    def is_value(self) -> bool:
        pass

    @abstractmethod
    def is_variable(self) -> bool:
        pass

    @abstractmethod
    def is_function(self) -> bool:
        pass

    @abstractmethod
    def is_generalized_list(self) -> bool:
        pass

    @abstractmethod
    def as_value(self) -> "Value":
        pass

    @abstractmethod
    def as_variable(self) -> "Variable":
        pass

    @abstractmethod
    def as_function(self) -> "Function":
        pass

    @abstractmethod
    def as_generalized_list(self) -> "GeneralizedList":
        pass

    @abstractmethod
    def evaluate(self, binding):
        pass
