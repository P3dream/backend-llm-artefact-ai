# Artefact AI Gen Tool

![Python](https://img.shields.io/badge/python-3.11+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-API-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Descrição

O **Artefact AI Gen Tool** é uma API inteligente que interpreta prompts em português, identifica operações matemáticas ou consultas financeiras e retorna resultados precisos. A ferramenta combina análise direta de expressões, parsing via LLM (Large Language Model) e integração com APIs externas, como a cotação do dólar.

---

## Funcionalidades

- **Detecção de operações matemáticas em português**  
  Ex: `"vinte vezes dez"`, `"30 mais 5"` → convertido para operação numérica.
- **Conversão de linguagem natural para expressão Python**  
  Suporta `+`, `-`, `*`, `/`, `**` (potência), `%` e negativos.
- **Avaliação segura de expressões**  
  Usa AST para evitar execução de código malicioso.
- **Consulta de cotação USD → BRL**  
  Detecta frases relacionadas ao dólar e retorna cotação atual via API pública.
- **Fallback via LLM**  
  Caso o prompt não seja matemático, gera resposta textual usando LLM.

---

## Arquitetura do fluxo

1. **Regex + AST**  
   - Extrai expressão matemática direta e calcula.
2. **Parser via LLM**  
   - Converte prompt em JSON `{operandos, operador}` e calcula seguro.
3. **Fallback LLM direto**  
   - Retorna resposta textual quando o prompt não é matemático.

**Fluxo resumido:**

```
Prompt recebido
       |
       v
1️⃣ Regex + AST -> resultado? -> sim -> Retorna
       |
       v
2️⃣ LLM Parser -> resultado? -> sim -> Retorna
       |
       v
3️⃣ LLM direto -> Retorna resposta
```

---

## Tecnologias

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- LLM (Ollama Llama3)
- Requests (API cotação dólar)

---

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST   | `/ia`    | Recebe `prompt` e retorna resultado da análise (matemática ou LLM). |
| GET    | `/test`  | Verifica se a API está rodando. |

**Exemplo POST `/ia`:**

```json
{
  "prompt": "quanto é 15 mais 27?",
  "model": "llama3:latest"
}
```

**Exemplo de resposta:**

```json
{
  "source": "calculator_regex",
  "result": 42
}
```

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/artefact-ai-gen-tool.git
cd artefact-ai-gen-tool
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Execute a API:

```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

4. Teste:

```
GET http://localhost:3000/test
```

---

## Estrutura do projeto

```
├── main.py                  # API principal
├── services/
│   ├── llm_service.py       # Chamadas ao LLM
│   ├── math_service.py      # Avaliação segura de expressões
│   ├── classifier_service.py# Extração e parsing de operações
│   ├── exchange_service.py  # Consulta de cotação USD-BRL
│   └── prompt_analisis_service.py # Fluxo de decisão do prompt
├── requirements.txt
└── README.md
```

---

## Exemplo de uso em Python

```python
from services.prompt_analisis_service import promptAnalysis

result = promptAnalysis("quanto é 20 vezes 5?")
print(result)
# Output: {'source': 'calculator_regex', 'result': 100}
```

---

## Licença

MIT License – livre para uso e modificação.

