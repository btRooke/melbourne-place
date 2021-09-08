import re

# Compiled regex
RE_THEN = re.compile("then")
RE_WHILE = re.compile("while (.*)$")
RE_IF = re.compile("if (.*)$")
RE_REPEAT = re.compile("repeat (\d+)$")
RE_SAVE = re.compile("save$")
RE_SET = re.compile("set ([rgb]) (\d+)$")
RE_ADD = re.compile("add ([rgb]) (\d+)$")
RE_SUB = re.compile("sub ([rgb]) (\d+)$")
RE_MUL = re.compile("mul ([rgb]) (\d+)$")
RE_DIV = re.compile("div ([rgb]) (\d+)$")
RE_WAIT = re.compile("wait (\d+)$")

def interpret(line, tabs):
    # Ignore empty lines
    if re.match("^\s*$", line):
        return ("", tabs)

    # 'then' means the current loop has ended, reduce indentation
    if RE_THEN.match(line):
        tabs -= 1

    prefix = "\t" * tabs

    success = RE_WHILE.match(line)
    if success:
        return ("{0}while eval({1}):".format(prefix, success.group(1)), tabs + 1)

    success = RE_IF.match(line)
    if success:
        return ("{0}if eval({1}):".format(prefix, success.group(1)), tabs + 1)

    success = RE_REPEAT.match(line)
    if success:
        return ("{0}for i in range({1}):".format(prefix, success.group(1)),  tabs + 1)

    success = RE_SAVE.match(line)
    if success:
        return ("{0}led[0] = [r, g, b]".format(prefix), tabs)

    success = RE_SET.match(line)
    if success:
        return ("{0}{1} = {2}}".format(prefix, success.group(1), success.group(2)), tabs)

    success = RE_ADD.match(line)
    if success:
        return (
            "{0}{1} += {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_SUB.match(line)
    if success:
        return (
            "{0}{1} -= {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_MUL.match(line)
    if success:
        return (
            "{0}{1} *= {2}\n".format(prefix, success.group(1), success.group(2)) +
            "{0}{1} %= 256".format(prefix, success.group(1)), 
            tabs)

    success = RE_DIV.match(line)
    if success:
        if int(success.group(2)) > 0:
            return (
                "{0}{1} /= {2}\n".format(prefix, success.group(1), success.group(2)) +
                "{0}{1} %= 256".format(prefix, success.group(1)), 
                tabs)
        raise ZeroDivisionError("Caught attempt to divide by zero")

    success = RE_WAIT.match(line)
    if success:
        if int(success.group(2)) >= 10:
            return ("{0}await uasyncio.sleep_ms({1})".format(prefix, success.group(1)), tabs)
        raise ValueError("Wait interval is too short, must be at least 50ms")

    raise ValueError("Could not match line '{0}' to a known command".format(line))
