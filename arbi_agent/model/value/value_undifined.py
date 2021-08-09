from arbi_agent.model.value.value import Value
from arbi_agent.configuration import GLValueType


class UndefinedValue(Value):

    def get_type(self):
        return GLValueType.TYPE_UNDIFINED

    def int_value(self) -> int:
        raise Exception()

    def float_value(self) -> float:
        raise Exception()

    def string_value(self) -> str:
        raise Exception()

    def boolean_value(self) -> bool:
        raise Exception()

    def add(self, value: Value) -> Value:
        raise Exception()

    def sub(self, value: Value) -> Value:
        raise Exception()

    def mul(self, value: Value) -> Value:
        raise Exception()

    def div(self, value: Value) -> Value:
        raise Exception()

    def mod(self, value: Value) -> Value:
        raise Exception()

    def lt(self, value: Value) -> bool:
        raise Exception()

    def gt(self, value: Value) -> bool:
        raise Exception()

    def eq(self, value: Value) -> bool:
        raise Exception()

    def equals(self, obj):
        raise Exception()

    def __str__(self):
        return "undefined"
