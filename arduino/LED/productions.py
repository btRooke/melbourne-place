# The productions in the light language grammar

from production import Production
from symbols import (
    ASSIGN, BOOLOP, COMMA, COND, ELSE, FALSE, FOR, 
    ID, IF, IN, INTOP, LBRACE, LBRACKET, NOT, NUM, 
    PASS, PING, RANDOM, RANGE, RBRACE, RBRACKET, 
    SAVE, TRUE, WAIT, WHILE)

class Script(Production):
    pass

class Block(Production):
    pass
    
class Statement(Production):
    pass

class Expr(Production):
    pass

class ExprExt(Production):
    pass

class ElseClause(Production):
    pass

class Range(Production):
    pass

class RangeList(Production):
    pass

class Op(Production):
    pass


Script.create_rules([
    [PING],
    [Block]
])


Block.create_rules([
    [(Statement, "+")]
])


Statement.create_rules([
    [ID, ASSIGN, Expr],
    [WAIT, Expr],
    [SAVE],
    [PASS],
    [WHILE, LBRACKET, Expr, RBRACKET, LBRACE, Block, RBRACE],
    [IF, LBRACKET, Expr, RBRACKET, LBRACE, Block, RBRACE, (ElseClause, "?")],
    [FOR, LBRACKET, ID, Range, RBRACKET, LBRACE, Block, RBRACE]    
])


Expr.create_rules([
    [NUM, (ExprExt, "?")],
    [ID, (ExprExt, "?")],
    [RANDOM, Range, (ExprExt, "?")],
    [TRUE, (ExprExt, "?")],
    [FALSE, (ExprExt, "?")],
    [NOT, Expr, (ExprExt, "?")],
    [LBRACKET, Expr, RBRACKET]
])


ExprExt.create_rules([
    [Op, Expr]
])


ElseClause.create_rules([
    [ELSE, LBRACE, Block, RBRACE]
])


Range.create_rules([
    [IN, RANGE, LBRACKET, Expr, (RangeList, "?"), (RangeList, "?"), RBRACKET]
])


RangeList.create_rules([
    [COMMA, Expr]
])


Op.create_rules([
    [INTOP],
    [BOOLOP],
    [COND]
])