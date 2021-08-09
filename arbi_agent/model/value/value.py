from abc import *


class Value(metaclass=ABCMeta):

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def int_value(self) -> int:
        pass

    @abstractmethod
    def float_value(self) -> float:
        pass

    @abstractmethod
    def string_value(self) -> str:
        pass

    @abstractmethod
    def boolean_value(self) -> bool:
        pass

    @abstractmethod
    def add(self, value: "Value") -> "Value":
        pass

    @abstractmethod
    def sub(self, value: "Value") -> "Value":
        pass

    @abstractmethod
    def mul(self, value: "Value") -> "Value":
        pass

    @abstractmethod
    def div(self, value: "Value") -> "Value":
        pass

    @abstractmethod
    def mod(self, value: "Value") -> "Value":
        pass

    @abstractmethod
    def lt(self, value: "Value") -> bool:
        pass

    @abstractmethod
    def gt(self, value: "Value") -> bool:
        pass

    @abstractmethod
    def eq(self, value: "Value") -> bool:
        pass

    @abstractmethod
    def equals(self, obj) -> bool:
        pass
