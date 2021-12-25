# Production definition

from symbol import Symbol, Terminal, NonTerminal

class Production:
    # Generate Terminal and NonTerminal lexemes from the rule arrays
    @classmethod
    def create_rules(cls, rules):
        cls.rules = []
        
        for rule in rules:
            # Evaluate each lexeme in the rule
            for i in range(len(rule)):
                lexeme = None
                modifier = ""

                # Check if (symbol, modifier) are given in a tuple
                if isinstance(rule[i], tuple):
                    symbol = rule[i][0]
                    modifier = rule[i][1]

                    # Modified terminal
                    if issubclass(symbol, Symbol): 
                        lexeme = Terminal(symbol, modifier)

                    # Modified non-terminal
                    elif issubclass(symbol, Production):
                        lexeme = NonTerminal(symbol, modifier)

                # Single terminal
                elif issubclass(rule[i], Symbol):
                    lexeme = Terminal(rule[i])

                # Single non-terminal
                else:
                    lexeme = NonTerminal(rule[i])

                # Bad type given
                if lexeme is None:
                    raise RuntimeError("Invalid lexeme type: expected <class 'symbols.Symbol'> or <class 'productions.Production'>, got " + lexeme)

                rule[i] = lexeme

            cls.rules.append(rule)


    @classmethod
    def match(cls, tokens: list, index: int) -> tuple:
        for rule in cls.rules:
            result, tokens, index = cls.match_rule(rule, tokens, index)

            # Return the first matching rule in a dict containing the name of the production
            if result is not None:
                return result, tokens, index

        return None, tokens, index


    @classmethod
    def match_rule(cls, rule: list, tokens: list, index: int) -> tuple:
        start_index = index
        i = 0
        found = False
        captured = {}

        # Find the first matching lexeme
        while i < len(rule) and index < len(tokens):
            lexeme = rule[i]
            result, tokens, index = lexeme.match(tokens, index)

            if result is None:
                # Skip for ?,* modifiers, 0 occurrences
                # Skip for +,* modifiers, many occurrences, still tokens to check
                if not lexeme.canBeOmitted and not found:
                    return result, tokens, start_index

            # Add the results of matching symbols
            # Use the symbol's type as the index for easy retrieval in the parser
            else:
                symbol = type(lexeme.symbol) if isinstance(lexeme.symbol, Symbol) else lexeme.symbol

                if symbol in captured:
                    captured[symbol].append(result)
                else:
                    captured[symbol] = [result] 

            found = result is not None

            # Only increment i if the next symbol definitely won't be the same
            if (found and not lexeme.canBeMany) or (not found and (lexeme.canBeOmitted or lexeme.canBeMany)):         
                i += 1

        return captured, tokens, index

    