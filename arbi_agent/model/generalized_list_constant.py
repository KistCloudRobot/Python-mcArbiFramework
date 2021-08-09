from arbi_agent.model.expression import expression_undifined
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.value.value_undifined import UndefinedValue
from arbi_agent.model.value.value_int import IntValue


class GeneralizedListConstant:
    UNDEFINED_VALUE = UndefinedValue()
    TRUE_VALUE = IntValue(1)
    FALSE_VALUE = IntValue(0)

    UNDEFINED_EXPRESSION = expression_undifined.UndefinedExpression()
    TRUE_EXPRESSION = ValueExpression(TRUE_VALUE)
    FALSE_EXPRESSION = ValueExpression(FALSE_VALUE)
