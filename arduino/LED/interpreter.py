import re, collections

# Compiled regex
RE_NUMBER = re.compile(r"(\d+)")
RE_COLOUR = re.compile(r"([rgb])")


def interpret(script):
    # Replace all whitespace with single spaces
    script = re.sub(r"\s+", ' ', script)

    # Get token stream
    words = script.split()
    tokens = collections.deque((), len(words))

    for i in words:
        tokens.append(i)

    result = "async def __script(r, g, b, led, lookup):\n"
    tabs = 1

    while len(tokens) > 0:
        token = tokens.popleft()
        print(token)

        if token == "then":
            tabs -= 1

        elif token == "while" or token == "if":
            result, tokens = addLoop(result, token, tokens, tabs)
            tabs += 1

        elif token == "repeat":
            result, tokens = addFor(result, tokens, tabs)
            tabs += 1

        elif token == "save":
            result = addSave(result, tabs)

        elif token == "wait":
            result, tokens = addWait(result, tokens, tabs)

        elif RE_COLOUR.search(token):
            result, tokens = addOp(result, token, tokens, tabs)

        else:
            raise ValueError("Could not match token '{0}' to a known command".format(tokens[i]))

    return result


def addLoop(result, token, tokens, tabs):
    condition = tokens.popleft()

    if condition == "random":
        condition, tokens = addRandom(tokens)
    
    elif RE_COLOUR.search(condition):
        op = tokens.popleft()

        if op == "<" or op == "<=" or op == "==" or op == ">=" or op == ">":
            value = tokens.popleft()

            if value == "random":
                value, tokens = addRandom(tokens)
            else:
                checkValue(value, True, True)

            condition = "{0} {1} {2}".format(condition, op, value)

        else:
            raise ValueError("Unrecognised operator '{0}'".format(op))

    line = "{0} eval('{1}', {{}}, {{'r': r, 'b': b, 'g': g}}):".format(token, condition)
    return (addLine(result, line, tabs), tokens)


def addFor(result, tokens, tabs):
    iterations = tokens.popleft()

    if iterations == "random":
        iterations, tokens = addRandom(tokens)
    else:
        checkValue(iterations, True, True)

    line = "for i in range({0}):".format(iterations)
    return (addLine(result, line, tabs), tokens)


def addSave(result, tabs):
    result = addLine(result, "led[0].duty(lookup[r])", tabs)
    result = addLine(result, "led[1].duty(lookup[g])", tabs)
    return addLine(result, "led[2].duty(lookup[b])", tabs)


def addWait(result, tokens, tabs):
    value = tokens.popleft()

    if value == "random":
        minimum = tokens.popleft()
        maximum = tokens.popleft()

        checkValue(minimum, True, True)
        checkValue(maximum, True, True)

        if int(minimum) < 10:
            raise ValueError("Wait interval is too short, must be at least 10ms")
        
        if int(minimum) > int(maximum):
            raise ValueError("Random value's minimum cannot be greater than its maximum")
        
        value = "random.randint({0}, {1})".format(minimum, maximum)
    
    else:
        checkValue(value, True, True)
        if int(value) < 10:
            raise ValueError("Wait interval is too short, must be at least 10ms")

    line = "await uasyncio.sleep_ms({0})".format(value)
    return (addLine(result, line, tabs), tokens)


def addOp(result, colour, tokens, tabs):
    checkValue(colour, False, True)
    op = tokens.popleft()

    value = tokens.popleft()
    if value == "random":
        value, tokens = addRandom(tokens)
    else:
        checkValue(value, True, True)

    if op == "=" or op == "+=" or op == "-=" or op == "*=" or op == "/=":
        line = "{0} {1} {2}".format(colour, op, value)
        return (addLine(result, line, tabs), tokens)

    raise ValueError("Unrecognised operator '{0}'".format(op))


def addRandom(tokens):
    minimum = tokens.popleft()
    maximum = tokens.popleft()

    checkValue(minimum, True, True)
    checkValue(maximum, True, True)

    if (minimum > maximum):
        raise ValueError("Random value's minimum cannot be greater than its maximum")

    line = "int(round(((random.getrandbits(10) / 1023) * ({0} - {1})) + {1}))".format(maximum, minimum)
    return (line, tokens)


def addLine(program, line, tabs):
    return program + ("\t" * tabs) + line + "\n"


def checkValue(value, canBeNumber, canBeColour):
    if canBeNumber and RE_NUMBER.search(value):
        return
    
    if canBeColour and RE_COLOUR.search(value):
        return

    raise ValueError("Expected value '{0}' to be a number or colour variable".format(value)) 