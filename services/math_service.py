import re
import ast
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def is_valid_expr(expr: str) -> bool:
    """Verifica se há dois números separados por operador, incluindo '**'."""
    pattern = r"\d+\s*(\*\*|[\+\-\*/])\s*\d+"
    return bool(re.search(pattern, expr))

def safe_eval(expr: str):
    """
    Avalia expressão de forma segura usando AST.
    """
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise TypeError("Operador não permitido")
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in operators:
                raise TypeError("Operador não permitido")
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError("Expressão inválida")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)

from typing import List

def safe_calc(operandos: List[float], operador: str) -> float:
    """
    Calcula de forma segura uma operação entre dois operandos.

    :param operandos: Lista com exatamente dois números [num1, num2]
    :param operador: '+', '-', '*', '/', '**'
    :return: Resultado da operação
    :raises ValueError: Para entradas inválidas
    """

    if not isinstance(operandos, list) or len(operandos) != 2:
        raise ValueError("Operandos inválidos. Devem ser uma lista com dois números.")

    num1, num2 = operandos

    if not all(isinstance(x, (int, float)) for x in operandos):
        raise ValueError("Operandos devem ser numéricos.")

    if operador == "+":
        return num1 + num2

    elif operador == "-":
        return num1 - num2

    elif operador == "*":
        return num1 * num2

    elif operador == "/":
        if num2 == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return num1 / num2

    elif operador == "**":
        return num1 ** num2

    else:
        raise ValueError(f"Operador inválido: {operador}")
