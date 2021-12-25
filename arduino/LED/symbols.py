# The symbols in the light language grammar

from re import match
from symbol import Symbol

class LiteralSymbol(Symbol):
    literal = ""
    literal = literal

class RegexSymbol(Symbol):
    regex = ""
    pattern = lambda token: match(regex, token) is not None


class PING(LiteralSymbol):
    literal = "ping"

class LBRACKET(LiteralSymbol):
    literal = "("

class RBRACKET(LiteralSymbol):
    literal = ")"

class LBRACE(LiteralSymbol):
    literal = "{"

class RBRACE(LiteralSymbol):
    literal = "}"

class COMMA(LiteralSymbol):
    literal = ","

class NOT(LiteralSymbol):
    literal = "!"

class TRUE(LiteralSymbol):
    literal = "true"

class FALSE(LiteralSymbol):
    literal = "false"

class WAIT(LiteralSymbol):
    literal = "wait"

class SAVE(LiteralSymbol):
    literal = "save"

class PASS(LiteralSymbol):
    literal = "pass"

class WHILE(LiteralSymbol):
    literal = "while"

class IF(LiteralSymbol):
    literal = "if"

class ELSE(LiteralSymbol):
    literal = "else"

class FOR(LiteralSymbol):
    literal = "for"

class IN(LiteralSymbol):
    literal = "in"

class RANGE(LiteralSymbol):
    literal = "range"

class RANDOM(LiteralSymbol):
    literal = "random"

class NUM(RegexSymbol):
    regex = r"^[0-9]+$"

class INTOP(RegexSymbol):
    regex = r"^[+\-\*/%]$"

class BOOLOP(RegexSymbol):
    regex = r"^&&|\|\|$"

class COND(RegexSymbol):
    regex = r"^[=!<>]=?$"

class ASSIGN(RegexSymbol):
    regex = r"^[+\-\*/]?=$"

class ID(RegexSymbol):
    regex = r"^[a-zA-Z][a-zA-Z|0-9|_]*$"
    pattern = lambda token: (
        match(regex, token) is not None and
        # Prevent conflicting matches with keywords 
        not PING.match(token) and
        not TRUE.match(token) and
        not FALSE.match(token) and 
        not WAIT.match(token) and
        not SAVE.match(token) and
        not PASS.match(token) and
        not WHILE.match(token) and
        not IF.match(token) and
        not ELSE.match(token) and
        not FOR.match(token) and
        not IN.match(token) and
        not RANGE.match(token) and
        not RANDOM.match(token))