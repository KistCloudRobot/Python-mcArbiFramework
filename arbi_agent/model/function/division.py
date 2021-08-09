from arbi_agent.model.function.abstract_function import AbstractFunction
from arbi_agent.model.value.value_int import IntValue
from arbi_agent.model.expression.expression_value import ValueExpression

class Division(AbstractFunction) :

    def __init__(self, *expressions) :
        super().__init__("div", *expressions)

    def evaluate(self, binding) :
        result = IntValue(0)
        for expression in self.expressions :
            evaluated_expression = expression.evaluate(binding)
            if evaluated_expression.is_value() :
                result = result.div(evaluated_expression.as_value())
        
        return ValueExpression(result)