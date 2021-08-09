from copy import deepcopy

from arbi_agent.model.value.value import Value
from arbi_agent.model.function.function import Function
from arbi_agent.model.variable import Variable
from arbi_agent.model import binding
from arbi_agent.model.expression import expression
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.expression.expression_generalized_list import GLExpression
from arbi_agent.model.generalized_list_constant import GeneralizedListConstant


class GeneralizedList:
    def __init__(self, name, *expressions: expression.Expression):
        self.name = name
        self.expressions = deepcopy(expressions)

    def get_name(self):
        return self.name

    def get_expression_size(self):
        return self.expressions.__len__()

    def get_expression(self, index: int) -> expression.Expression:
        return self.expressions[index]

    def evaluate(self, b):
        evaluated_expressions = []
        for i in range(self.expressions.__len__()):
            evaluated_expressions.append(self.expressions[i].evaluate(b))
        return GeneralizedList(self.name, *evaluated_expressions)

    def get_bounded_expression(self, variable, b, unifier):
        if b is not None:
            bounded_expression = b.retrieve(variable)
        else:
            bounded_expression = GeneralizedListConstant.UNDEFINED_EXPRESSION

        if bounded_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
            bounded_expression = unifier.retrieve(variable)

        if bounded_expression.is_variable():
            raise Exception()

        return bounded_expression

    def get_evaluated_expression(self, function, b, unifier):
        return function.evaluate(binding.Binding().copy(unifier))

    def unify(self, *args):
        if args.__len__() == 4:
            if (type(args[2]) != binding.Binding and args[2] is not None) or \
                    (type(args[3]) != binding.Binding and args[2] is not None):
                raise Exception()

            if isinstance(args[0], expression.Expression):
                if isinstance(args[1], expression.Expression):
                    if args[0].is_value():
                        return self.unify(args[1], args[0].as_value(), args[2], args[3])
                    elif args[0].is_variable():
                        return self.unify(args[1], args[0].as_variable(), args[2], args[3])
                    elif args[0].is_function():
                        return self.unify(args[1], args[0].as_function(), args[2], args[3])
                    elif args[0].is_generalized_list():
                        return self.unify(args[1], args[0].as_generalized_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], Value):
                    if args[0].is_value():
                        return self.unify(args[1], args[0].as_value())
                    elif args[0].is_variable():
                        return self.unify(args[0].as_variable(), args[1], args[2], args[3])
                    elif args[0].is_function():
                        return self.unify(args[0].as_function(), args[1], args[2], args[3])
                    return False
                elif isinstance(args[1], Variable):
                    if args[0].is_value():
                        return self.unify(args[1], args[0].as_value(), args[2], args[3])
                    elif args[0].is_variable():
                        return self.unify(args[1], args[0].as_variable(), args[2], args[3])
                    elif args[0].is_function():
                        return self.unify(args[1], args[0].as_function(), args[2], args[3])
                    elif args[0].is_generalized_list():
                        return self.unify(args[1], args[0].as_generalized_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], Function):
                    if args[0].is_value():
                        return self.unify(args[1], args[0].as_value(), args[2], args[3])
                    elif args[0].is_variable():
                        return self.unify(args[1], args[0].as_variable(), args[2], args[3])
                    elif args[0].is_function():
                        return self.unify(args[1], args[0].as_function(), args[2], args[3])
                    elif args[0].is_generalized_list():
                        return self.unify(args[1], args[0].as_generalized_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], GeneralizedList):
                    if args[0].is_variable():
                        return self.unify(args[1], args[0].as_variable(), args[2], args[3])
                    elif args[0].is_generalized_list():
                        return self.unify(args[1], args[0].as_generalized_list(), args[2], args[3])
                    return False

            elif isinstance(args[0], Variable):
                if isinstance(args[1], Value):
                    lh_bounded_expression = self.get_bounded_expression(args[0], args[2], args[3])
                    if lh_bounded_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
                        args[3].bind(args[0], ValueExpression(args[1]))
                        return True
                    elif lh_bounded_expression.is_value():
                        return self.unify(lh_bounded_expression.as_value(), args[1])
                    return False
                elif isinstance(args[1], Variable):
                    lh_bounded_expression = self.get_bounded_expression(args[0], args[2], args[3])
                    if lh_bounded_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
                        rh_bounded_expression = self.get_bounded_expression(args[1], args[2], args[3])
                        if rh_bounded_expression != GeneralizedListConstant.UNDEFINED_EXPRESSION:
                            args[3].bind(args[0], rh_bounded_expression)
                        return True
                    elif lh_bounded_expression.is_value():
                        return self.unify(args[1], lh_bounded_expression.as_value(), args[2], args[3])
                    elif lh_bounded_expression.is_generalized_list():
                        return self.unify(args[1], lh_bounded_expression.as_generalizes_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], Function):
                    lh_bounded_expression = self.get_bounded_expression(args[0], args[2], args[3])
                    if lh_bounded_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
                        rh_evaluated_expression = self.get_evaluated_expression(args[1], args[2], args[3])
                        if rh_evaluated_expression != GeneralizedListConstant.UNDEFINED_EXPRESSION:
                            args[3].bind(args[0], rh_evaluated_expression)
                        return True
                    elif lh_bounded_expression.is_value():
                        return self.unify(args[1], lh_bounded_expression.as_value(), args[2], args[3])
                    elif lh_bounded_expression.is_generalized_list():
                        return self.unify(args[1], lh_bounded_expression.as_generalizes_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], GeneralizedList):
                    lh_bounded_expression = self.get_bounded_expression(args[0], args[2], args[3])
                    if lh_bounded_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
                        args[3].bind(args[0], GLExpression(args[1]))
                        return True
                    elif lh_bounded_expression.is_generalized_list():
                        return self.unify(args[1], lh_bounded_expression.as_generalizes_list(), args[2], args[3])
                    return False

            elif isinstance(args[0], Function):
                if isinstance(args[1], Value):
                    lh_evaluated_expression = self.get_evaluated_expression(args[0], args[2], args[3])
                    if lh_evaluated_expression.is_value():
                        return self.unify(lh_evaluated_expression.as_value(), args[1])
                    elif lh_evaluated_expression.is_variable():
                        return self.unify(lh_evaluated_expression.as_variable(), args[1], args[2], args[3])
                    elif lh_evaluated_expression.is_function():
                        return self.unify(lh_evaluated_expression.as_function(), args[1], args[2], args[3])
                    return False
                elif isinstance(args[1], Function):
                    lh_evaluated_expression = self.get_evaluated_expression(args[0], args[2], args[3])
                    if lh_evaluated_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION:
                        rh_evaluated_expression = self.get_evaluated_expression(args[1], args[2], args[3])
                        return rh_evaluated_expression == GeneralizedListConstant.UNDEFINED_EXPRESSION
                    if lh_evaluated_expression.is_value():
                        return self.unify(args[1], lh_evaluated_expression.as_value(), args[2], args[3])
                    elif lh_evaluated_expression.is_variable():
                        return self.unify(lh_evaluated_expression.as_variable(), args[1], args[2], args[3])
                    elif lh_evaluated_expression.is_function():
                        return self.unify(lh_evaluated_expression.as_function(), args[1], args[2], args[3])
                    elif lh_evaluated_expression.is_generalized_list():
                        return self.unify(args[1], lh_evaluated_expression.as_generalized_list(), args[2], args[3])
                    return False
                elif isinstance(args[1], GeneralizedList):
                    lh_evaluated_expression = self.get_evaluated_expression(args[0], args[2], args[3])
                    if lh_evaluated_expression.is_value():
                        return self.unify(lh_evaluated_expression.as_value(), args[1], args[2], args[3])
                    elif lh_evaluated_expression.is_function():
                        return self.unify(lh_evaluated_expression.as_function(), args[1], args[2], args[3])
                    elif lh_evaluated_expression.is_generalized_list():
                        return self.unify(lh_evaluated_expression.as_generalizes_list(), args[1], args[2], args[3])
                    return False

            elif isinstance(args[0], GeneralizedList):
                temp_binding = binding.Binding().copy(args[2]).copy(args[3])
                temp_unifier = args[0].unify(args[1], temp_binding)
                if temp_unifier is not None:
                    args[3].copy(temp_unifier)
                    return True
                return False

        elif args.__len__() == 2:

            if isinstance(args[0], GeneralizedList):
                if self.name != args[0].get_name():
                    return None
                if self.get_expression_size() != args[0].get_expression_size():
                    return None
                unifier = binding.Binding()
                for i in range(self.expressions.__len__()):
                    if self.unify(self.expressions[i], args[0].get_expression(i), args[1], unifier) is False:
                        return None
                # for line in traceback.format_stack():
                #     print(line.strip())
                return unifier

            elif isinstance(args[0], Value) and isinstance(args[1], Value):
                return args[0].equals(args[1])

    def __str__(self):
        string = "(%s" % self.name
        for expression in self.expressions:
            string += " %s" % str(expression)
        string += ")"
        return string
