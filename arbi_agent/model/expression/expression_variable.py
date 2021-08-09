from arbi_agent.model.expression.expression import Expression
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arbi_agent.model.value.value import Value
    from arbi_agent.model.variable import Variable
    from arbi_agent.model.function.function import Function
    from arbi_agent.model.generalized_list import GeneralizedList


class VariableExpression(Expression):
    def __init__(self, variable):
        self.variable = variable

    def is_value(self) -> bool:
        return False

    def is_variable(self) -> bool:
        return True

    def is_function(self) -> bool:
        return False

    def is_generalized_list(self) -> bool:
        return False

    def as_value(self) -> "Value":
        raise Exception()

    def as_variable(self) -> "Variable":
        return self.variable

    def as_function(self) -> "Function":
        raise Exception()

    def as_generalized_list(self) -> "GeneralizedList":
        raise Exception()

    def evaluate(self, binding):
        if binding is None:
            return GeneralizedListConstant.UNDEFINED_EXPRESSION
        else:
            return binding.retrieve(self.variable)

    def __str__(self):
        return str(self.variable)
