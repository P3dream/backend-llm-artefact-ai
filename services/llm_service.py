import json
from ollama import chat
from typing import Any

def call_llm(
    prompt: str,
    provider: str = "ollama",
    model: str | None = None,
    system_prompt: str | None = None,
    stream: bool = False,
    format: dict | None = None
) -> str:

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    if provider != "ollama":
        raise NotImplementedError(f"Provider {provider} não implementado")

    try:
        response = chat(
            messages=messages,
            model=model or "llama3:latest",
            stream=stream,
            format=format
        )
    except Exception as e:
        raise RuntimeError("Erro ao chamar LLM") from e

    try:
        return response["message"]["content"]
    except (TypeError, KeyError):
        try:
            return response.message.content
        except AttributeError:
            raise RuntimeError("Formato inesperado de resposta do LLM")




def parse_math_nl(prompt: str, provider="ollama", model=None):
    system_prompt = """
    Você é um parser de operações matemáticas em português.
    Retorne APENAS JSON com {"operandos":[...], "operador":"..."}
    """
    response = call_llm(prompt, provider=provider, system_prompt=system_prompt,model=model)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"operandos": [], "operador": ""}

def natural_language_to_expression(prompt: str, provider="ollama", model=None):
    system_prompt = "Converta a frase em linguagem natural para expressão matemática Python. Retorne apenas a expressão."
    response = call_llm(prompt, provider=provider, system_prompt=system_prompt,model=model)
    return response.strip()