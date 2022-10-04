# Generated from C:/Users/1208d/Documents/project/Python-mcArbiFramework/arbi_agent/model/parser\GeneralizedList.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GeneralizedListParser import GeneralizedListParser
else:
    from GeneralizedListParser import GeneralizedListParser

# This class defines a complete generic visitor for a parse tree produced by GeneralizedListParser.

class GeneralizedListVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GeneralizedListParser#generalized_list.
    def visitGeneralized_list(self, ctx:GeneralizedListParser.Generalized_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GeneralizedListParser#expression_list.
    def visitExpression_list(self, ctx:GeneralizedListParser.Expression_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GeneralizedListParser#expression.
    def visitExpression(self, ctx:GeneralizedListParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GeneralizedListParser#value.
    def visitValue(self, ctx:GeneralizedListParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GeneralizedListParser#variable.
    def visitVariable(self, ctx:GeneralizedListParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GeneralizedListParser#function.
    def visitFunction(self, ctx:GeneralizedListParser.FunctionContext):
        return self.visitChildren(ctx)



del GeneralizedListParser