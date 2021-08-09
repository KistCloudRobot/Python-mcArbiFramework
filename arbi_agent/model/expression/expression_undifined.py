from arbi_agent.model.expression import expression
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arbi_agent.model.value.value import Value
    from arbi_agent.model.variable import Variable
    from arbi_agent.model.function.function import Function
    from arbi_agent.model.generalized_list import GeneralizedList


class UndefinedExpression(expression.Expression):
    def is_value(self) -> bool:
        return False

    def is_variable(self) -> bool:
        return False

    def is_function(self) -> bool:
        return False

    def is_generalized_list(self) -> bool:
        return False

    def as_value(self) -> "Value":
        raise Exception()

    def as_variable(self) -> "Variable":
        raise Exception()

    def as_function(self) -> "Function":
        raise Exception()

    def as_generalized_list(self) -> "GeneralizedList":
        raise Exception()

    def evaluate(self, binding):
        return self

    def __str__(self):
        return "undefined"
