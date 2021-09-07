from arbi_agent.model.value.value import Value
from arbi_agent.model.value.value_float import FloatValue
from arbi_agent.model.value.value_string import StringValue
from arbi_agent.model.value.value_undifined import UndefinedValue
from arbi_agent.model.variable import Variable
from arbi_agent.model.expression.expression import Expression
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.expression.expression_undifined import UndefinedExpression
from arbi_agent.model.function.function import Function
from arbi_agent.model.parser import gl_parser_implementation as GLParser


def new_generalized_list(name: str, *expressions: Expression) -> "generalized_list.GeneralizedList":
    from arbi_agent.model import generalized_list
    return generalized_list.GeneralizedList(name, *expressions)


def new_gl_from_gl_string(string: str) -> "generalized_list.GeneralizedList":
    from arbi_agent.model import generalized_list
    return GLParser.parse_generalized_list(string)


def int_value(value: int) -> Value:
    from arbi_agent.model.value.value_int import IntValue
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
    from arbi_agent.model.expression.expression_variable import VariableExpression
    if isinstance(variable, Variable):
        return VariableExpression(variable)
    elif isinstance(variable, str):
        return VariableExpression(Variable(variable))
    else:
        print("variable expression error: not proper argument type")
    return None


def new_function(identifier: str, *expressions) -> Function:

    if identifier == "add":
        from arbi_agent.model.function.addition import Addition
        return Addition(identifier, *expressions)
    elif identifier == "sub":
        from arbi_agent.model.function.subtraction import Subtraction
        return Subtraction(identifier, *expressions)
    elif identifier == "mul":
        from arbi_agent.model.function.multipication import Mulitipication
        return Mulitipication(identifier, *expressions)
    elif identifier == "div":
        from arbi_agent.model.function.division import Division
        return Division(identifier, *expressions)
    elif identifier == "mod":
        from arbi_agent.model.function.modulo import Modulo
        return Modulo(identifier, *expressions)
    elif identifier == "gt":
        from arbi_agent.model.function.greater_than import GreaterThan
        return GreaterThan(identifier, *expressions)
    elif identifier == "ge":
        from arbi_agent.model.function.greater_than_equals import GreaterThanEquals
        return GreaterThanEquals(identifier, *expressions)
    elif identifier == "lt":
        from arbi_agent.model.function.less_than import LessThan
        return LessThan(identifier, *expressions)
    elif identifier == "le":
        from arbi_agent.model.function.less_than_equeals import LessThanEquals
        return LessThanEquals(identifier, *expressions)
    elif identifier == "eq":
        from arbi_agent.model.function.equals import Equals
        return Equals(identifier, *expressions)
    elif identifier == "ne":
        from arbi_agent.model.function.not_equals import NotEquals
        return NotEquals(identifier, *expressions)
    elif identifier == "not":
        from arbi_agent.model.function.function_not import Not
        return Not(identifier, *expressions)
    elif identifier == "and":
        from arbi_agent.model.function.function_and import And
        return And(identifier, *expressions)
    elif identifier == "or":
        from arbi_agent.model.function.function_or import Or
        return Or(identifier, *expressions)


def escape(content: str):
    return content.replace("<", "&lt;").replace(">", "&gt;")\
        .replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos")


def unescape(content: str):
    return content.replace("&lt;", "<").replace("&gt;", ">")\
        .replace("&amp;", "&").replace("&quot;", '"').replace("&apos", "'")
