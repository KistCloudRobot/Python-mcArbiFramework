from antlr4 import InputStream, CommonTokenStream
from arbi_agent.model.parser.GeneralizedListLexer import GeneralizedListLexer
from arbi_agent.model.parser.GeneralizedListParser import GeneralizedListParser
from arbi_agent.model.parser.GeneralizedListVisitor import GeneralizedListVisitor

from arbi_agent.model.generalized_list import GeneralizedList

from arbi_agent.model.expression.expression_function import FunctionExpression
from arbi_agent.model.expression.expression_generalized_list import GLExpression
from arbi_agent.model.expression.expression_list import ExpressionList
from arbi_agent.model.expression.expression_value import ValueExpression
from arbi_agent.model.expression.expression_variable import VariableExpression

from arbi_agent.model.variable import Variable

import arbi_agent.model.generalized_list_factory as GLFactory


def parse_generalized_list(gl):
    stream = InputStream(gl)
    lexer = GeneralizedListLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = GeneralizedListParser(stream)

    parse_tree = parser.generalized_list()

    visitor = GeneralizedListBuilder()

    return visitor.visit(parse_tree)


class GeneralizedListBuilder(GeneralizedListVisitor):

    def visitGeneralized_list(self, ctx: GeneralizedListParser.Generalized_listContext):
        id = str(ctx.IDENTIFIER())
        expression_list = self.visit(ctx.exp_list)
        return GLFactory.new_generalized_list(id, *expression_list)

    def visitExpression_list(self, ctx: GeneralizedListParser.Expression_listContext):

        return_expression_list = []

        for expression in ctx.expression():
            return_expression_list.append(self.visit(expression))

        return return_expression_list

    def visitExpression(self, ctx: GeneralizedListParser.ExpressionContext):

        if ctx.val != None:
            value = self.visit(ctx.val)
            return ValueExpression(value)
        elif ctx.var != None:
            variable = self.visit(ctx.var)
            return VariableExpression(variable)
        elif ctx.func != None:
            function = self.visit(ctx.func)
            return FunctionExpression(function)
        elif ctx.gl != None:
            gl = self.visit(ctx.gl)
            return GLExpression(gl)

    def visitValue(self, ctx: GeneralizedListParser.ValueContext):

        if ctx.FLOAT() != None:
            return GLFactory.float_value(float(str(ctx.FLOAT())))
        elif ctx.INTEGER() != None:
            return GLFactory.int_value(int(str(ctx.INTEGER())))
        elif ctx.STRING() != None:
            return GLFactory.string_value(str(ctx.STRING()))
        elif ctx.SPECIAL_KEYWORD() != None:
            return GLFactory.string_value(str(ctx.SPECIAL_KEYWORD()))

    def visitVariable(self, ctx: GeneralizedListParser.VariableContext):
        return Variable(str(ctx.VARIABLE()))

    def visitFunction(self, ctx: GeneralizedListParser.FunctionContext):
        id = str(ctx.IDENTIFIER())
        expression_list = self.visit(ctx.exp_list)

        return GLFactory.new_function(id, *expression_list)


if __name__ == "__main__":
    gl_string = '(testgl "test"  17.25 (innergl $variable) )'
    gl = parse_generalized_list(gl_string)

    print(gl.get_name())
    print(gl.get_expression_size())
    print(gl.get_expression(0).as_value().string_value())
    print(gl.get_expression(1))
    print(gl.get_expression(2))

    print(gl.get_expression(2).as_generalized_list().get_name())
    print(gl.get_expression(2).as_generalized_list().get_expression_size())
    print(gl.get_expression(2).as_generalized_list().get_expression(0).is_variable())
    print(gl.get_expression(2).as_generalized_list().get_expression(0).as_variable())

    # wrong_gl = '("wrong")'
    # parse_generalized_list(wrong_gl)
