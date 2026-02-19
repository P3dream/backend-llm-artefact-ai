from services.classifier_service import extract_expression, parse_math_operation
from services.math_service import safe_eval, safe_calc, is_valid_expr
from services.llm_service import call_llm
from services.exchange_service import get_usd_brl_rate


def promptAnalysis(prompt: str, model: str | None = None):
    """
    Decide se deve usar ferramenta matemática ou LLM.
    Fluxo:
    1. Tenta extrair expressão direta (regex)
    2. Tenta parse estruturado via LLM
    3. Fallback para LLM normal
    """

    prompt_lower = prompt.lower()

    # 0️⃣ Verificar cotação do dólar
    if (
        ("dólar" in prompt_lower or "dolar" in prompt_lower)
        and any(word in prompt_lower for word in ["quanto", "cotação", "vale", "está", "hoje"])
    ):
        try:
            rate = get_usd_brl_rate()
            return {
                "source": "exchange_api",
                "result": f"O dólar está cotado a R$ {rate:.2f}"
            }
        except Exception:
            return {
                "source": "exchange_api",
                "result": "Não foi possível consultar a cotação no momento."
            }

# 1️⃣ Regex + AST
    expr = extract_expression(prompt)
    if expr and is_valid_expr(expr):
        result = safe_eval(expr)
        return {
            "source": "calculator_regex",
            "result": result
        }

    # 2️⃣ Parser estruturado via LLM
    parsed = parse_math_operation(prompt, model)
    if parsed and parsed.operandos and parsed.operador:
        operandos = [float(x) for x in parsed.operandos]
        result = safe_calc(operandos, parsed.operador)
        return {
            "source": "calculator_llm_parser",
            "result": result
        }

    # 3️⃣ Fallback LLM
    result = call_llm(prompt, model=model)
    return {
        "source": "llm_direct",
        "result": result
    }