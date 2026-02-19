import re
from enum import Enum
from pydantic import BaseModel
from services.llm_service import call_llm

class MathOperation(BaseModel):
    operandos: list[float]
    operador: str


class LabelEnum(str, Enum):
    IS_MATH_OPERATION = "IS_MATH_OPERATION"
    NOT_MATH_OPERATION = "NOT_MATH_OPERATION"

class DetectMathOperation(BaseModel):
    isMathOperation: LabelEnum

def parse_math_operation(prompt: str, model=None) -> MathOperation:
    """
    Usa o LLM para transformar uma frase em operação matemática em JSON estruturado.
    Retorna um objeto MathOperation.
    """

    system_prompt = """
    Você é um parser de operações matemáticas em português.
    Receba frases como 'vinte vezes dez' ou 'trinta mais cinco'.
    Retorne **apenas JSON** com:
    - operandos: lista de 2 números
    - operador: '+', '-', '*', '/', '**'
    Se a frase não for operação matemática, retorne {"operandos": [], "operador": ""}.
    """

    response_content = call_llm(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        format=MathOperation.model_json_schema(),
        stream=False,
    )

    try:
        return MathOperation.model_validate_json(response_content)
    except Exception:
        return MathOperation(operandos=[], operador="")


def extract_expression(text: str):
    """
    Converte linguagem natural e símbolos em expressão Python.
    """
    text = text.lower()

    replacements = {
        "ao quadrado": "**2",
        "raiz de": "**0.5",
        "elevado a": "**",
        "elevado": "**",
        "vezes": "*",
        "mais": "+",
        "menos": "-",
        "dividido por": "/"
    }

    for word, operator in replacements.items():
        text = text.replace(word, operator)

    match = re.findall(r"[0-9\+\-\*/\.\(\)\s\^]+", text)

    expr = None
    if match:
        expr = "".join(match).strip()
        expr = expr.replace("^", "**")
        return expr

    return None

