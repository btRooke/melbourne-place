# The symbols in the light language grammar

from re import match
from symbol import Symbol

class PING(Symbol):
    pattern = lambda token: token == "ping"

class LBRACKET(Symbol):
    pattern = lambda token: token == "("

class RBRACKET(Symbol):
    pattern = lambda token: token == ")"

class LBRACE(Symbol):
    pattern = lambda token: token == "{"

class RBRACE(Symbol):
    pattern = lambda token: token == "}"

class COMMA(Symbol):
    pattern = lambda token: token == ","

class ID(Symbol):
    pattern = lambda token: (
        match(r"^[a-zA-Z][a-zA-Z|0-9|_]*$", token) is not None and
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

class NUM(Symbol):
    pattern = lambda token: match(r"^[0-9]+$", token) is not None

class INTOP(Symbol):
    pattern = lambda token: match(r"^[+\-\*/%]$", token) is not None

class BOOLOP(Symbol):
    pattern = lambda token: match(r"^&&|\|\|$", token) is not None

class COND(Symbol):
    pattern = lambda token: match(r"^[=!<>]=?$", token) is not None

class ASSIGN(Symbol):
    pattern = lambda token: match(r"^[+\-\*/]?=$", token) is not None

class NOT(Symbol):
    pattern = lambda token: token == "!"

class TRUE(Symbol):
    pattern = lambda token: token == "true"

class FALSE(Symbol):
    pattern = lambda token: token == "false"

class WAIT(Symbol):
    pattern = lambda token: token == "wait"

class SAVE(Symbol):
    pattern = lambda token: token == "save"

class PASS(Symbol):
    pattern = lambda token: token == "pass"

class WHILE(Symbol):
    pattern = lambda token: token == "while"

class IF(Symbol):
    pattern = lambda token: token == "if"

class ELSE(Symbol):
    pattern = lambda token: token == "else"

class FOR(Symbol):
    pattern = lambda token: token == "for"

class IN(Symbol):
    pattern = lambda token: token == "in"

class RANGE(Symbol):
    pattern = lambda token: token == "range"

class RANDOM(Symbol):
    pattern = lambda token: token == "random"