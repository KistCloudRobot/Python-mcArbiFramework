grammar GeneralizedList;

options {
    language = Python3;
}

generalized_list : '(' identifier = IDENTIFIER exp_list = expression_list ')' ;

expression_list : (exp = expression)* ;

expression : val = value | var = variable | func = function | gl = generalized_list;

value : identifier = (INTEGER | FLOAT | STRING | SPECIAL_KEYWORD);

variable : identifier =  VARIABLE;

function : '#(' identifier = IDENTIFIER exp_list = expression_list ')' ;

WS : [ \t\n\r\f]+ -> skip ;

fragment LETTER : ([_a-zA-Z]) ;
fragment DIGIT : [0-9] ;
fragment SIGN : [+-];
fragment EXP : [eE] (SIGN)? (DIGIT)+ ;
fragment COLON : ':' ;
fragment SPECIAL_CHARACTER : [/.#] ;

INTEGER : (SIGN)? (DIGIT)+ ;
FLOAT : ( (SIGN)? (DIGIT)+ '.' (DIGIT)* (EXP)? | (SIGN)? '.' (DIGIT)+ (EXP)? ) ;
IDENTIFIER : [_a-zA-Z] (LETTER | DIGIT | COLON | SPECIAL_CHARACTER)* ;
VARIABLE : '$' (LETTER | DIGIT | '.' )* ;
SPECIAL_KEYWORD : ( '-->' ) ;

// https://github.com/antlr/antlr4/blob/master/doc/lexer-rules.md 참조, antlr string parser
// LQUOTE : '"' -> more, mode(STR) ;

// mode STR ;
// STRING : '"' -> mode(DEFAULT_MODE);
// TEXT : . -> more ;

STRING : '"' ~('"')* '"' ;