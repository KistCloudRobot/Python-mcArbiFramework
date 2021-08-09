from arbi_agent.model.function.abstract_function import AbstractFunction
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant

class Not(AbstractFunction) :

    def __init__(self, *expressions) :
        super().__init__("not", *expressions)
        if expressions.__len__() != 1 :
            raise Exception()

    def evaluate(self, binding) :
        evaluated_expression = self.expressions[0].evaluate(binding)
        if evaluated_expression.is_value() :
            if evaluated_expression.as_value().boolean_value() :
                return GeneralizedListConstant.FALSE_EXPRESSION
            else :
                return GeneralizedListConstant.TRUE_EXPRESSION

        raise Exception()
