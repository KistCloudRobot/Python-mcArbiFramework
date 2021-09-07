# Generated from C:/Users/1208d/Documents/project/Python-mcArbiFramework/arbi_agent/model/parser\GeneralizedList.g4 by ANTLR 4.9.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write(")\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\3\7\3\25\n\3\f\3\16\3\30\13\3\3\4\3")
        buf.write("\4\3\4\3\4\5\4\36\n\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\2\2\b\2\4\6\b\n\f\2\3\4\2\7\b\13\f\2&\2\16\3")
        buf.write("\2\2\2\4\26\3\2\2\2\6\35\3\2\2\2\b\37\3\2\2\2\n!\3\2\2")
        buf.write("\2\f#\3\2\2\2\16\17\7\3\2\2\17\20\7\t\2\2\20\21\5\4\3")
        buf.write("\2\21\22\7\4\2\2\22\3\3\2\2\2\23\25\5\6\4\2\24\23\3\2")
        buf.write("\2\2\25\30\3\2\2\2\26\24\3\2\2\2\26\27\3\2\2\2\27\5\3")
        buf.write("\2\2\2\30\26\3\2\2\2\31\36\5\b\5\2\32\36\5\n\6\2\33\36")
        buf.write("\5\f\7\2\34\36\5\2\2\2\35\31\3\2\2\2\35\32\3\2\2\2\35")
        buf.write("\33\3\2\2\2\35\34\3\2\2\2\36\7\3\2\2\2\37 \t\2\2\2 \t")
        buf.write("\3\2\2\2!\"\7\n\2\2\"\13\3\2\2\2#$\7\5\2\2$%\7\t\2\2%")
        buf.write("&\5\4\3\2&\'\7\4\2\2\'\r\3\2\2\2\4\26\35")
        return buf.getvalue()


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
        self.checkVersion("4.9.1")
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





