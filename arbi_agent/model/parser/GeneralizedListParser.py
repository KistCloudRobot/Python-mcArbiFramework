# Generated from /home/uosai/project/Python-mcArbiFramework/arbi_agent/model/parser/GeneralizedList.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,10,39,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,0,1,0,1,0,1,1,5,1,19,8,1,10,1,12,1,22,9,1,1,2,1,2,1,2,1,2,3,
        2,28,8,2,1,3,1,3,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,0,0,6,0,2,4,6,8,
        10,0,1,2,0,5,6,9,10,36,0,12,1,0,0,0,2,20,1,0,0,0,4,27,1,0,0,0,6,
        29,1,0,0,0,8,31,1,0,0,0,10,33,1,0,0,0,12,13,5,1,0,0,13,14,5,7,0,
        0,14,15,3,2,1,0,15,16,5,2,0,0,16,1,1,0,0,0,17,19,3,4,2,0,18,17,1,
        0,0,0,19,22,1,0,0,0,20,18,1,0,0,0,20,21,1,0,0,0,21,3,1,0,0,0,22,
        20,1,0,0,0,23,28,3,6,3,0,24,28,3,8,4,0,25,28,3,10,5,0,26,28,3,0,
        0,0,27,23,1,0,0,0,27,24,1,0,0,0,27,25,1,0,0,0,27,26,1,0,0,0,28,5,
        1,0,0,0,29,30,7,0,0,0,30,7,1,0,0,0,31,32,5,8,0,0,32,9,1,0,0,0,33,
        34,5,3,0,0,34,35,5,7,0,0,35,36,3,2,1,0,36,37,5,2,0,0,37,11,1,0,0,
        0,2,20,27
    ]

class GeneralizedListParser ( Parser ):

    grammarFileName = "GeneralizedList.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'#('" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "WS", "INTEGER", "FLOAT", "IDENTIFIER", "VARIABLE", 
                      "SPECIAL_KEYWORD", "STRING" ]

    RULE_generalized_list = 0
    RULE_expression_list = 1
    RULE_expression = 2
    RULE_value = 3
    RULE_variable = 4
    RULE_function = 5

    ruleNames =  [ "generalized_list", "expression_list", "expression", 
                   "value", "variable", "function" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    WS=4
    INTEGER=5
    FLOAT=6
    IDENTIFIER=7
    VARIABLE=8
    SPECIAL_KEYWORD=9
    STRING=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Generalized_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.identifier = None # Token
            self.exp_list = None # Expression_listContext

        def IDENTIFIER(self):
            return self.getToken(GeneralizedListParser.IDENTIFIER, 0)

        def expression_list(self):
            return self.getTypedRuleContext(GeneralizedListParser.Expression_listContext,0)


        def getRuleIndex(self):
            return GeneralizedListParser.RULE_generalized_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneralized_list" ):
                return visitor.visitGeneralized_list(self)
            else:
                return visitor.visitChildren(self)




    def generalized_list(self):

        localctx = GeneralizedListParser.Generalized_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_generalized_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(GeneralizedListParser.T__0)
            self.state = 13
            localctx.identifier = self.match(GeneralizedListParser.IDENTIFIER)
            self.state = 14
            localctx.exp_list = self.expression_list()
            self.state = 15
            self.match(GeneralizedListParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.exp = None # ExpressionContext

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GeneralizedListParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(GeneralizedListParser.ExpressionContext,i)


        def getRuleIndex(self):
            return GeneralizedListParser.RULE_expression_list

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression_list" ):
                return visitor.visitExpression_list(self)
            else:
                return visitor.visitChildren(self)




    def expression_list(self):

        localctx = GeneralizedListParser.Expression_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expression_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GeneralizedListParser.T__0) | (1 << GeneralizedListParser.T__2) | (1 << GeneralizedListParser.INTEGER) | (1 << GeneralizedListParser.FLOAT) | (1 << GeneralizedListParser.VARIABLE) | (1 << GeneralizedListParser.SPECIAL_KEYWORD) | (1 << GeneralizedListParser.STRING))) != 0):
                self.state = 17
                localctx.exp = self.expression()
                self.state = 22
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None # ValueContext
            self.var = None # VariableContext
            self.func = None # FunctionContext
            self.gl = None # Generalized_listContext

        def value(self):
            return self.getTypedRuleContext(GeneralizedListParser.ValueContext,0)


        def variable(self):
            return self.getTypedRuleContext(GeneralizedListParser.VariableContext,0)


        def function(self):
            return self.getTypedRuleContext(GeneralizedListParser.FunctionContext,0)


        def generalized_list(self):
            return self.getTypedRuleContext(GeneralizedListParser.Generalized_listContext,0)


        def getRuleIndex(self):
            return GeneralizedListParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = GeneralizedListParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expression)
        try:
            self.state = 27
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GeneralizedListParser.INTEGER, GeneralizedListParser.FLOAT, GeneralizedListParser.SPECIAL_KEYWORD, GeneralizedListParser.STRING]:
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                localctx.val = self.value()
                pass
            elif token in [GeneralizedListParser.VARIABLE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                localctx.var = self.variable()
                pass
            elif token in [GeneralizedListParser.T__2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 25
                localctx.func = self.function()
                pass
            elif token in [GeneralizedListParser.T__0]:
                self.enterOuterAlt(localctx, 4)
                self.state = 26
                localctx.gl = self.generalized_list()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.identifier = None # Token

        def INTEGER(self):
            return self.getToken(GeneralizedListParser.INTEGER, 0)

        def FLOAT(self):
            return self.getToken(GeneralizedListParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(GeneralizedListParser.STRING, 0)

        def SPECIAL_KEYWORD(self):
            return self.getToken(GeneralizedListParser.SPECIAL_KEYWORD, 0)

        def getRuleIndex(self):
            return GeneralizedListParser.RULE_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = GeneralizedListParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            localctx.identifier = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GeneralizedListParser.INTEGER) | (1 << GeneralizedListParser.FLOAT) | (1 << GeneralizedListParser.SPECIAL_KEYWORD) | (1 << GeneralizedListParser.STRING))) != 0)):
                localctx.identifier = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.identifier = None # Token

        def VARIABLE(self):
            return self.getToken(GeneralizedListParser.VARIABLE, 0)

        def getRuleIndex(self):
            return GeneralizedListParser.RULE_variable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)




    def variable(self):

        localctx = GeneralizedListParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            localctx.identifier = self.match(GeneralizedListParser.VARIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.identifier = None # Token
            self.exp_list = None # Expression_listContext

        def IDENTIFIER(self):
            return self.getToken(GeneralizedListParser.IDENTIFIER, 0)

        def expression_list(self):
            return self.getTypedRuleContext(GeneralizedListParser.Expression_listContext,0)


        def getRuleIndex(self):
            return GeneralizedListParser.RULE_function

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)




    def function(self):

        localctx = GeneralizedListParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_function)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.match(GeneralizedListParser.T__2)
            self.state = 34
            localctx.identifier = self.match(GeneralizedListParser.IDENTIFIER)
            self.state = 35
            localctx.exp_list = self.expression_list()
            self.state = 36
            self.match(GeneralizedListParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





