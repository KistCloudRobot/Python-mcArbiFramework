from arbi_agent.model.function.function import Function
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant
from arbi_agent.model.variable import Variable
from arbi_agent.model.expression.expression import Expression

from typing import TYPE_CHECKING, Dict, KeysView, Union

if TYPE_CHECKING:
    from arbi_agent.model.expression.expression import Expression


class Binding:
    def __init__(self):
        self.binding_map: Dict[str, "Expression"] = dict()

    def get_bounded_variable_names(self) -> KeysView[str]:
        return self.binding_map.keys()

    def copy(self, binding: "Binding") -> "Binding":
        if binding is not None:
            for var_name in binding.get_bounded_variable_names():
                self.bind(var_name, binding.retrieve(var_name))

        return self

    def bind(self, var: Union[Variable, str], expression: "Expression"):
        if type(var) is str:
            self.binding_map[var] = expression
        elif type(var) is Variable:
            self.bind(var.get_name(), expression)

    def unbind(self, var: Union[Variable, str]):
        from arbi_agent.model.generalized_list import GeneralizedList

        if type(var) is str:
            del self.binding_map[var]
        elif type(var) is Variable:
            self.unbind(var.get_name())
        elif type(var) is Expression:
            if var.is_variable():
                self.unbind(var.as_variable())
            elif var.is_generalized_list():
                self.unbind(var.as_generalized_list())
            elif var.is_function():
                self.unbind(var.as_function())
        elif type(var) is GeneralizedList:
            for i in range(var.get_expression_size()):
                self.unbind(var.get_expression(i))
        elif type(var) is Function:
            for i in range(var.get_expression_size()):
                self.unbind(var.get_expression(i))

    def retrieve(self, var):
        if type(var) is str:
            if var in self.binding_map:
                return self.binding_map[var]
            else:
                return GeneralizedListConstant.UNDEFINED_EXPRESSION
        elif type(var) is Variable:
            return self.retrieve(var.get_name())

    def __str__(self):
        _str = "{"
        for key in self.binding_map.keys():
            _str = _str + '"' + key + '"' + ": " + str(self.binding_map.get(key)) + ", "
        _str = _str[:-2] + "}"
        return _str
