from arbi_agent.model.function.abstract_function import AbstractFunction
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant
from arbi_agent.model.value.value import Value

class NotEquals(AbstractFunction) :

    def __init__(self, *expressions) :
        super().__init__("ne", *expressions)
        if expressions.__len__() < 2 :
            raise Exception()

    def evaluate(self, binding) :
        check = False
        value = GeneralizedListConstant.UNDEFINED_VALUE
        for expression in self.expressions :
            evaluated_expression = expression.evaluate(binding)
            if evaluated_expression.is_value() :
                next_value = evaluated_expression.as_value()
                if value == GeneralizedListConstant.UNDEFINED_VALUE :
                    value = next_value
                else :
                    check = True
                    if value.eq(next_value) :
                        return GeneralizedListConstant.FALSE_EXPRESSION
                    else :
                        value = next_value
        
        if check is False :
            raise Exception()
        
        return GeneralizedListConstant.TRUE_EXPRESSION