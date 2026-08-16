from langchain_core.tools import tool


@tool
def calculator(
    number1: float,
    operator: str,
    number2: float,
) -> float:
    """
    Performs basic arithmetic calculations.
    """

    if operator == "+":
        return number1 + number2

    if operator == "-":
        return number1 - number2

    if operator == "*":
        return number1 * number2

    if operator == "/":
        return number1 / number2

    raise ValueError("Unsupported operator")