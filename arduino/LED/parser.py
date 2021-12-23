from re import sub, split
from symbols import WHILE, IF, FOR, WAIT, SAVE, PASS, ASSIGN, ID, NUM, RANDOM, TRUE, FALSE, NOT, LBRACKET, INTOP, BOOLOP, COND
from productions import Script, Statement, Expr, ExprExt, ElseClause, Range, RangeList, Op

def generate_tokens(text: str) -> list:
    # Ensure special characters have leading and trailing spaces
    text = sub(r"\(", " ( ", text)
    text = sub(r"\)", " ) ", text)
    text = sub(r"{", " { ", text)
    text = sub(r"}", " } ", text)
    text = sub(r"!", " ! ", text)

    # Split on any whitespace
    return split(r"\s+", text)


def parse(tokens: list):
    result, tokens, _ = Script().match(tokens, 0)

    if result is None:
        raise RuntimeError("Failed to parse script")

    return "async def __script(vars, led, lookup, rng):\n" + enter_script(result)


def enter_script(result: dict) -> str:
    print("Entering script:", result)
    script = ""

    for s in result[Statement]:
        statement = enter_statement(s)
        statement = statement.replace("\n", "\n\t")

        script += "\t" + statement + "\n"

    return script


def enter_statement(result: dict) -> str:
    print("Entering statement:", result)
    statement = ""

    if WHILE in result:
        statement += "while " + enter_expr(result[Expr][0]) + ":\n"

    if IF in result:
        statement += "if " + enter_expr(result[Expr][0]) + ":\n"

    if FOR in result:
        statement += "for " + enter_expr(result[Expr][0]) + " in " + enter_range(result[Range][0]) + ":\n"

    if Script in result:
        statement += enter_script(result[Script][0])

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
    print("Entering expr:", result)
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
    print("Entering expr extension:", result)
    return " " + enter_op(result[Op][0]) + " " + enter_expr(result[Expr][0])


def enter_elseclause(result: dict) -> str:
    print("Entering else:", result)
    return "else:\n" + enter_script(result[Script][0])


def enter_range(result: dict) -> str:
    print("Entering range:", result)
    text = "range(" + enter_expr(result[Expr][0])

    for rangelist in result[RangeList]:
        text += enter_rangelist(rangelist)

    return text + ")"


def enter_rangelist(result: dict) -> str:
    print("Entering range args:", result)
    return ", " + enter_expr(result[Expr][0])


def enter_op(result: dict) -> str:
    print("Entering op:", result)
    if INTOP in result:
        return result[INTOP][0]

    elif BOOLOP in result:
        return result[BOOLOP][0]

    elif COND in result:
        return result[COND][0]