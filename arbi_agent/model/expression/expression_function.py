from arbi_agent.model.expression import expression
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arbi_agent.model.value.value import Value
    from arbi_agent.model.variable import Variable
    from arbi_agent.model.function.function import Function
    from arbi_agent.model.generalized_list import GeneralizedList


class FunctionExpression(expression.Expression):
    def __init__(self, function: "Function"):
        self.func: "Function" = function

    def is_value(self) -> bool:
        return False

    def is_variable(self) -> bool:
        return False

    def is_function(self) -> bool:
        return True

    def is_generalized_list(self) -> bool:
        return False

    def as_value(self) -> "Value":
        raise Exception()

    def as_variable(self) -> "Variable":
        raise Exception()

    def as_function(self) -> "Function":
        return self.func

    def as_generalized_list(self) -> "GeneralizedList":
        raise Exception()

    def evaluate(self, binding):
        return self.func.evaluate(binding)

    def __str__(self):
        return str(self.func)
