from re import sub, split
from symbols import WHILE, IF, FOR, WAIT, SAVE, PASS, PING, ASSIGN, ID, NUM, RANDOM, TRUE, FALSE, NOT, LBRACKET, INTOP, BOOLOP, COND
from productions import Script, Block, Statement, Expr, ExprExt, ElseClause, Range, RangeList, Op

def generate_tokens(text: str) -> list:
    # Ensure operators and other special characters have leading and trailing spaces
    text = sub(COND.regex, r" \\0 ", text)
    text = sub(ASSIGN.regex, r" \\0 ", text)
    text = sub(INTOP.regex, r" \\0 ", text)
    text = sub(BOOLOP.regex, r" \\0 ", text)
    text = sub(r"[\(\){}!,]", r" \\0 ", text)

    # Split on any whitespace
    return split(r"\s+", text)


def parse(tokens: list) -> str:
    result, tokens, _ = Script().match(tokens, 0)

    if result is None:
        raise RuntimeError("Failed to parse script")

    script = enter_block(result)

    if len(script) > 0:
        script = "async def __script(vars, led, lookup, rng):\n" + script

    return script


def enter_script(result: dict) -> str:
    # Pings are denoted by an empty string
    if PING in result:
        return ""

    if Block in result:
        return enter_block(result[Block][0])


def enter_block(result: dict) -> str:
    block = ""

    for s in result[Statement]:
        statement = enter_statement(s)
        statement = statement.replace("\n", "\n\t")

        block += "\t" + statement + "\n"

    return block


def enter_statement(result: dict) -> str:
    statement = ""

    if WHILE in result:
        statement += "while " + enter_expr(result[Expr][0]) + ":\n"

    if IF in result:
        statement += "if " + enter_expr(result[Expr][0]) + ":\n"

    if FOR in result:
        statement += "for " + enter_expr(result[Expr][0]) + " in " + enter_range(result[Range][0]) + ":\n"

    if Block in result:
        statement += enter_block(result[Block][0])

        if ElseClause in result:
            statement += enter_elseclause(result[ElseClause][0])

    elif ASSIGN in result:
        statement += "vars[" + result[ID][0] + "] " + result[ASSIGN][0] + " " + enter_expr(result[Expr][0])

    elif WAIT in result:
        statement += "await uasyncio.sleep_ms(" + enter_expr(result[Expr][0]) + ")"

    elif SAVE in result:
        statement += "led[0].duty(lookup[vars[r]])\n"
        statement += "led[1].duty(lookup[vars[g]])\n"
        statement += "led[2].duty(lookup[vars[b]])"

    elif PASS in result:
        statement += "pass"

    return statement

    
def enter_expr(result: dict) -> str:
    expr = ""
    
    if ID in result:
        expr = result[ID][0]

    if NUM in result:
        expr = result[NUM][0]

    elif RANDOM in result:
        expr = "rng(" + enter_range(result[Range][0]) + ")"

    elif TRUE in result:
        expr = result[TRUE][0]

    elif FALSE in result:
        expr = result[FALSE][0]

    elif NOT in result:
        expr = "not " + enter_expr(result[Expr][0])

    elif LBRACKET in result:
        expr = "(" + enter_expr(result[Expr][0]) + ")"

    if ExprExt in result:
        expr += enter_exprext(result[ExprExt][0])

    return expr


def enter_exprext(result: dict) -> str:
    return " " + enter_op(result[Op][0]) + " " + enter_expr(result[Expr][0])


def enter_elseclause(result: dict) -> str:
    return "else:\n" + enter_block(result[Block][0])


def enter_range(result: dict) -> str:
    text = "range(" + enter_expr(result[Expr][0])

    for rangelist in result[RangeList]:
        text += enter_rangelist(rangelist)

    return text + ")"


def enter_rangelist(result: dict) -> str:
    return ", " + enter_expr(result[Expr][0])


def enter_op(result: dict) -> str:
    if INTOP in result:
        return result[INTOP][0]

    elif BOOLOP in result:
        return result[BOOLOP][0]

    elif COND in result:
        return result[COND][0]