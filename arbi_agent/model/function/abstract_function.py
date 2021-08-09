from copy import deepcopy
from arbi_agent.model.function.function import Function

class AbstractFunction(Function) :

    def __init__(self, name, *expressions) :
        self.name = name
        if expressions == None :
            self.expressions = []
        else :
            self.expressions = deepcopy(expressions)

    def get_name(self) :
        return self.name

    def get_expression_size(self) :
        return self.expressions.__len__()

    def get_expression(self, index) :
        return self.expressions[index]

    def __str__(self) :
        str_function = "#(" + self.name

        buffer = []

        for expression in self.expressions :
            buffer.append(" " + str(expression))

        str_function = str_function + ''.join(map(str, buffer)) + ")"
        return str_function
    

    