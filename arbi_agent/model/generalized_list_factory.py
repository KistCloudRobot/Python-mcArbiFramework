from arbi_agent.model.value.value import Value
from arbi_agent.model.value.value_int import IntValue
from arbi_agent.model.value.value_float import FloatValue
from arbi_agent.model.value.value_string import StringValue
from arbi_agent.model.value.value_undifined import UndefinedValue
from arbi_agent.model.variable import Variable
from arbi_agent.model import generalized_list
from arbi_agent.model.expression.expression import Expression
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.expression.expression_variable import VariableExpression
from arbi_agent.model.expression.expression_undifined import UndefinedExpression
from arbi_agent.model.function.function import Function
from arbi_agent.model.function.addition import Addition
from arbi_agent.model.function.subtraction import Subtraction
from arbi_agent.model.function.multipication import Mulitipication
from arbi_agent.model.function.division import Division
from arbi_agent.model.function.modulo import Modulo
from arbi_agent.model.function.greater_than import GreaterThan
from arbi_agent.model.function.greater_than_equals import GreaterThanEquals
from arbi_agent.model.function.less_than import LessThan
from arbi_agent.model.function.less_than_equeals import LessThanEquals
from arbi_agent.model.function.equals import Equals
from arbi_agent.model.function.not_equals import NotEquals
from arbi_agent.model.function.function_not import Not
from arbi_agent.model.function.function_and import And
from arbi_agent.model.function.function_or import Or
from arbi_agent.model.parser import gl_parser_implementation as GLParser


def new_generalized_list(name: str, *expressions: Expression) -> generalized_list.GeneralizedList:
    return generalized_list.GeneralizedList(name, *expressions)


def new_gl_from_gl_string(string: str) -> generalized_list.GeneralizedList:
    return GLParser.parse_generalized_list(string)


def int_value(value: int) -> Value:
    return IntValue(value)


def float_value(value: float) -> Value:
    return FloatValue(value)


def string_value(value: str) -> Value:
    return StringValue(value)


def undefined_value() -> Value:
    return UndefinedValue()


def value_expression(value: Value) -> Expression:
    if isinstance(value, Value):
        return ValueExpression(value)

    if isinstance(value, int):
        value = int_value(value)
    elif isinstance(value, float):
        value = float_value(value)
    elif isinstance(value, str):
        value = string_value(value)
    else:
        print("value expression error: not proper argument type")

    return ValueExpression(value)


def undefined_expression() -> Expression:
    return UndefinedExpression()


def variable_expression(variable: Variable) -> Expression:

    if isinstance(variable, Variable):
        return VariableExpression(variable)
    elif isinstance(variable, str):
        return VariableExpression(Variable(variable))
    else:
        print("variable expression error: not proper argument type")

    return None


def new_function(identifier: str, *expressions) -> Function:

    if identifier == "add":
        return Addition(identifier, *expressions)
    elif identifier == "sub":
        return Subtraction(identifier, *expressions)
    elif identifier == "mul":
        return Mulitipication(identifier, *expressions)
    elif identifier == "div":
        return Division(identifier, *expressions)
    elif identifier == "mod":
        return Modulo(identifier, *expressions)
    elif identifier == "gt":
        return GreaterThan(identifier, *expressions)
    elif identifier == "ge":
        return GreaterThanEquals(identifier, *expressions)
    elif identifier == "lt":
        return LessThan(identifier, *expressions)
    elif identifier == "le":
        return LessThanEquals(identifier, *expressions)
    elif identifier == "eq":
        return Equals(identifier, *expressions)
    elif identifier == "ne":
        return NotEquals(identifier, *expressions)
    elif identifier == "not":
        return Not(identifier, *expressions)
    elif identifier == "and":
        return And(identifier, *expressions)
    elif identifier == "or":
        return Or(identifier, *expressions)


def escape(content: str):
    return content.replace("<", "&lt;").replace(">", "&gt;")\
        .replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos")


def unescape(content: str):
    return content.replace("&lt;", "<").replace("&gt;", ">")\
        .replace("&amp;", "&").replace("&quot;", '"').replace("&apos", "'")
