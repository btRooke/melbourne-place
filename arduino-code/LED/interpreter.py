import re

# Compiled regex
THEN = re.compile("then")
WHILE = re.compile("while (.*)$")
IF = re.compile("if (.*)$")
REPEAT = re.compile("repeat (\d+)$")
SAVE = re.compile("save$")
SET = re.compile("set ([rgb]) (\d+)$")
ADD = re.compile("add ([rgb]) (\d+)$")
SUB = re.compile("sub ([rgb]) (\d+)$")
MUL = re.compile("mul ([rgb]) (\d+)$")
DIV = re.compile("div ([rgb]) (\d+)$")
WAIT = re.compile("wait (\d+)$")

def interpret(line, tabs):
    # Ignore empty lines
    if re.match("^\s*$", line):
        return ("", tabs)

    # 'then' means the current loop has ended, reduce indentation
    if THEN.match(line):
        tabs -= 1

    prefix = "\t" * tabs

    success = WHILE.match(line)
    if success:
        return (f"{prefix}while eval({success.groups(1)}):", tabs + 1)

    success = IF.match(line)
    if success:
        return (f"{prefix}if eval({success.groups(1)}):", tabs + 1)

    success = REPEAT.match(line)
    if success:
        return (f"{prefix}for i in range({success.group(1)}):",  tabs + 1)

    success = SAVE.match(line)
    if success:
        return (f"{prefix}led[0] = [r, g, b]", tabs)

    success = SET.match(line)
    if success:
        return (f"{prefix}{success.group(1)} = {success.group(2)}", tabs)

    success = ADD.match(line)
    if success:
        return (
            f"{prefix}{success.group(1)} += {success.group(2)}\n" +
            f"{prefix}{success.group(1)} %= 256", 
            tabs)

    success = SUB.match(line)
    if success:
        return (
            f"{prefix}{success.group(1)} -= {success.group(2)}\n" +
            f"{prefix}{success.group(1)} %= 256", 
            tabs)

    success = MUL.match(line)
    if success:
        return (
            f"{prefix}{success.group(1)} *= {success.group(2)}\n" +
            f"{prefix}{success.group(1)} %= 256", 
            tabs)

    success = DIV.match(line)
    if success:
        if int(success.group(2)) > 0:
            return (
                f"{prefix}{success.group(1)} /= {success.group(2)}\n" +
                f"{prefix}{success.group(1)} %= 256", 
                tabs)
        raise ZeroDivisionError("Caught attempt to divide by zero")

    success = WAIT.match(line)
    if success:
        if int(success.group(2)) >= 10:
            return (f"{prefix}await uasyncio.sleep_ms({success.group(1)})", tabs)
        raise ValueError("Wait interval is too short, must be at least 50ms")

    raise ValueError(f"Could not match line '{line}' to a known command")
    