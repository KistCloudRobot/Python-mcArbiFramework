from arbi_agent.model.value.value import Value
from arbi_agent.configuration import GLValueType
from arbi_agent.model import generalized_list_factory as GeneralizedListFactory


class FloatValue(Value):
    def __init__(self, value):
        self.value = value

    def get_type(self):
        return GLValueType.TYPE_FLOAT

    def int_value(self) -> int:
        return int(self.value)

    def float_value(self) -> float:
        return self.value

    def string_value(self) -> str:
        return str(self.value)

    def boolean_value(self) -> bool:
        return self.value != 0

    def add(self, value: Value) -> Value:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return FloatValue(self.value + value.float_value())
        elif value.get_type() == GLValueType.TYPE_STRING:
            return GeneralizedListFactory.string_value(str(self.value) + value.string_value())

        raise Exception()

    def sub(self, value: Value) -> Value:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return FloatValue(self.value - value.float_value())

        raise Exception()

    def mul(self, value: Value) -> Value:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return FloatValue(self.value * value.float_value())

        raise Exception()

    def div(self, value: Value) -> Value:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return FloatValue(self.value / value.float_value())

        raise Exception()

    def mod(self, value: Value) -> Value:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return FloatValue(self.value % value.int_value())

        raise Exception()

    def lt(self, value: Value) -> bool:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return self.value < value.float_value()

        raise Exception()

    def gt(self, value: Value) -> bool:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return self.value > value.float_value()

        raise Exception()

    def eq(self, value: Value) -> bool:
        if (value.get_type() == GLValueType.TYPE_INT
                or value.get_type() == GLValueType.TYPE_FLOAT):
            return self.value == value.float_value()

        return False

    def equals(self, obj: Value) -> bool:
        if obj == self:
            return True

        if type(obj) is Value:
            return self.eq(obj)
        else:
            return False

    def hashcode(self) -> int:
        return hash(self.value)

    def __str__(self):
        return str(self.value)
