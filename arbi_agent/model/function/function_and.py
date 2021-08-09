from arbi_agent.model.function.abstract_function import AbstractFunction
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant

class And(AbstractFunction) :

    def __init__(self, *expressions) :
        super().__init__("and", *expressions)
        if expressions.__len__() < 2 :
            raise Exception()

    def evaluate(self, binding) :
        check = False
        for expression in self.expressions :
            evaluated_expression = expression.evaluate(binding)
            if evaluated_expression.is_value() :
                check = True
                if evaluated_expression.as_value().boolean_value() is False:
                    return GeneralizedListConstant.FALSE_EXPRESSION
        
        if check is False :
            raise Exception()
        
        return GeneralizedListConstant.TRUE_EXPRESSION