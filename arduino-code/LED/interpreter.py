import re

# Compiled regex
RE_THEN = re.compile(r"then")
RE_WHILE = re.compile(r"while (.*?)$")
RE_IF = re.compile(r"if (.*?)$")
RE_REPEAT = re.compile(r"repeat (\d+)")
RE_SAVE = re.compile(r"save")
RE_SET = re.compile(r"set ([rgb]) (\d+)")
RE_ADD = re.compile(r"add ([rgb]) (\d+)")
RE_SUB = re.compile(r"sub ([rgb]) (\d+)")
RE_MUL = re.compile(r"mul ([rgb]) (\d+)")
RE_DIV = re.compile(r"div ([rgb]) (\d+)")
RE_WAIT = re.compile(r"wait (\d+)")

def interpret(line, tabs):
    # Ignore empty lines
    if re.match(r"^\s*$", line):
        return ("", tabs)

    # 'then' means the current loop has ended, reduce indentation
    if RE_THEN.search(line):
        tabs -= 1

    prefix = "\t" * tabs

    success = RE_WHILE.search(line)
    if success:
        return ("{0}while eval('{1}', {{}}, {{'r': r, 'b': b, 'g': g}}):".format(prefix, success.group(1)), tabs + 1)

    success = RE_IF.search(line)
    if success:
        return ("{0}if eval('{1}', {{}}, {{'r': r, 'b': b, 'g': g}}):".format(prefix, success.group(1)), tabs + 1)

    success = RE_REPEAT.search(line)
    if success:
        return ("{0}for i in range({1}):".format(prefix, success.group(1)),  tabs + 1)

    success = RE_SAVE.search(line)
    if success:
        return (
            "{0}led[0].duty(lookup[r])\n".format(prefix) +
            "{0}led[1].duty(lookup[g])\n".format(prefix) +
            "{0}led[2].duty(lookup[b])".format(prefix), 
            tabs)

    success = RE_SET.search(line)
    if success:
        return ("{0}{1} = {2}".format(prefix, success.group(1), success.group(2)), tabs)

    success = RE_ADD.search(line)
    if success:
        return (
            "{0}{1} += {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_SUB.search(line)
    if success:
        return (
            "{0}{1} -= {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_MUL.search(line)
    if success:
        return (
            "{0}{1} *= {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_DIV.search(line)
    if success:
        if int(success.group(2)) > 0:
            return (
                "{0}{1} /= {2}\n".format(prefix, success.group(1), success.group(2)) +
                "{0}{1} %= 256".format(prefix, success.group(1)), 
                tabs)
        raise ZeroDivisionError("Caught attempt to divide by zero")

    success = RE_WAIT.search(line)
    if success:
        if int(success.group(1)) >= 10:
            return ("{0}await uasyncio.sleep_ms({1})".format(prefix, success.group(1)), tabs)
        raise ValueError("Wait interval is too short, must be at least 10ms")

    raise ValueError("Could not match line '{0}' to a known command".format(line))
