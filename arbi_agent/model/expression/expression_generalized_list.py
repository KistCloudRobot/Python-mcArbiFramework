from arbi_agent.model.expression.expression import Expression
from arbi_agent.model import generalized_list_factory as GLFactory
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arbi_agent.model.value.value import Value
    from arbi_agent.model.variable import Variable
    from arbi_agent.model.function.function import Function
    from arbi_agent.model.generalized_list import GeneralizedList


class GLExpression(Expression):

    def __init__(self, gl):
        self.gl = gl

    def is_value(self) -> bool:
        return False

    def is_variable(self) -> bool:
        return False

    def is_function(self) -> bool:
        return False

    def is_generalized_list(self) -> bool:
        return True

    def as_value(self) -> "Value":
        raise Exception()

    def as_variable(self) -> "Variable":
        raise Exception()

    def as_function(self) -> "Function":
        raise Exception()

    def as_generalized_list(self) -> "GeneralizedList":
        return self.gl

    def evaluate(self, binding):
        return GLFactory.new_generalized_list(self.gl.evaluate(binding))

    def __str__(self):
        return str(self.gl)
