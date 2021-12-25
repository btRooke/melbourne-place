# Terminal and non-terminal symbol definitions

class Symbol:
    pattern = lambda x: False

    @classmethod
    def match(cls, token: str) -> bool:
        return cls.pattern(token)

class Lexeme:
    def __init__(self, symbol, modifier: str = ""):
        self.symbol = symbol
        self.canBeOmitted = False
        self.canBeMany = False

        if modifier not in ["", "?", "+", "*"]:
            raise RuntimeError("Unrecognised modifier " + modifier)

        if modifier == "?" or modifier == "*":
            self.canBeOmitted = True

        if modifier == "+" or modifier == "*":
            self.canBeMany = True


    def match(self, tokens: list, index: int) -> tuple:
        return None, tokens, index


class Terminal(Lexeme):
    def __init__(self, symbol, modifier: str = ""):
        super().__init__(symbol, modifier)

    def match(self, tokens: list, index: int) -> tuple:
        # Consume the token if it matches the terminal symbol
        if self.symbol.match(tokens[index]):
            return tokens[index], tokens, index + 1
        else:
            return None, tokens, index


class NonTerminal(Lexeme):
    def __init__(self, symbol, modifier: str = ""):
        super().__init__(symbol, modifier)

    def match(self, tokens: list, index: int) -> tuple:
        # Attempt to replace the non-terminal with the appropriate production
        result, tokens, index = self.symbol.match(tokens, index)

        if result:
            return result, tokens, index
        else:
            return None, tokens, index