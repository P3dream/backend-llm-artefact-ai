# Artefact AI Gen Tool

![Python](https://img.shields.io/badge/python-3.11+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-API-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Descrição

O **Artefact AI Gen Tool** é uma API inteligente que interpreta prompts em português, identifica operações matemáticas ou consultas financeiras e retorna resultados precisos. A ferramenta combina análise direta de expressões, parsing via LLM (Large Language Model) e integração com APIs externas, como a cotação do dólar.

O projeto utiliza **Ollama como provider dos modelos LLM**, mas a arquitetura foi planejada de forma **modular**, permitindo substituir o provider facilmente. Por exemplo, seria possível integrar APIs pagas ou outros provedores com uma pequena implementação do provider, graças ao design injetável das dependências.

A API possui uma **arquitetura híbrida para solução de problemas matemáticos**: perguntas simples podem ser resolvidas utilizando **regex**, evitando o uso de LLMs, que são caros computacionalmente, poupando recursos. Além de operações matemáticas tradicionais, a API também responde a perguntas utilizando linguagem natural do tipo:
`"Tinha 5 pães, comprei mais dois, quantos pães eu tenho?"` → resultado: `7`, realizando a extração dos operandos e operador através do LLM, com prompt de saída estruturada.

Exemplos de modelos usados: `deepseek-r1:latest` e `llama3:latest`, mas qualquer modelo suportado pelo Ollama pode ser utilizado.


## Funcionalidades

* **Detecção de operações matemáticas em português**
  Ex: `"vinte vezes dez"`, `"30 mais 5"` → convertido para operação numérica.
  (Perguntas simples podem ser resolvidas via **regex**, poupando o uso de LLMs e recursos computacionais.)
* **Conversão de linguagem natural para expressão Python**
  Suporta `+`, `-`, `*`, `/`, `**` (potência), `%` e negativos.
* **Avaliação segura de expressões**
  Usa AST para evitar execução de código malicioso.
* **Consulta de cotação USD → BRL**
  Detecta frases relacionadas ao dólar e retorna cotação atual via API pública.
* **Fallback via LLM**
  Caso o prompt não seja matemático ou seja complexo, gera resposta textual usando LLM.
* **Responde perguntas simples de contagem ou adição em linguagem natural**
  Ex: `"Tinha 5 pães, comprei mais dois, quantos pães eu tenho?"`
  (A extração dos operandos e operador é feita via LLM com prompt de saída estruturada.)
* **Indicação da fonte da resposta**
  O backend informa de qual etapa veio o resultado (`regex`, `parser LLM`, `LLM direto` ou `API de câmbio`), permitindo transparência e rastreabilidade.

## Arquitetura do fluxo

1. **Verificação de consulta de câmbio**

   * Identifica se o prompt é uma pergunta sobre cotação do dólar (USD → BRL).
   * Se for, consulta a API externa e retorna o resultado.
   * Exemplo: `"Quanto está o dólar hoje?"` → Retorna cotação atual.

2. **Regex + AST**

   * Extrai expressões matemáticas diretas e calcula.
   * Perguntas simples podem ser resolvidas aqui, poupando o uso de LLM.
   * Exemplo: `"2 + 2"`, `"2 * 3"`, `"10 vezes 9"` → Retorna o resultado.

3. **Parser via LLM**

   * Converte expressões matemáticas ou linguagem natural simples em JSON `{operandos, operador}` e calcula seguro.
   * Usado para operações matemáticas mais complexas em português.
   * Exemplo: `"Quanto é 2 mais três?"` → Retorna 5.

4. **Fallback LLM direto**

   * Retorna resposta textual para perguntas gerais ou consultas de conhecimento, não matemáticas e não sobre câmbio.
   * Exemplo: `"Quem foi Albert Einstein?"` → Retorna resposta textual informativa.

**Fluxo resumido:**

```
Prompt recebido
       |
       v
1️⃣ Verifica se é consulta de dólar -> sim -> Retorna cotação (ex: "Quanto está o dólar hoje?")
       |
       v
2️⃣ Regex + AST -> resultado? -> sim -> Retorna (ex: "2 + 2", "2 * 3", "10 vezes 9")
       |
       v
3️⃣ LLM Parser -> resultado? -> sim -> Retorna (ex: "Quanto é 2 mais três?")
       |
       v
4️⃣ LLM direto -> Retorna resposta (ex: "Quem foi Albert Einstein?")
```

---



## Tecnologias

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* LLM (Ollama) – `deepseek-r1:latest`, `llama3:latest` (exemplo)
* Requests (API cotação dólar)

---

## Endpoints

| Método | Endpoint | Descrição                                                           |
| ------ | -------- | ------------------------------------------------------------------- |
| POST   | `/ia`    | Recebe `prompt` e retorna resultado da análise (matemática ou LLM). |
| GET    | `/test`  | Verifica se a API está rodando.                                     |

# Exemplos de uso da API `/ia`

**Exemplo POST com operação matemática direta:**

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

**Exemplo POST com linguagem natural simples (contagem ou adição):**

```json
{
  "prompt": "Tinha 5 pães, comprei mais dois, quantos pães eu tenho?",
  "model": "deepseek-r1:latest"
}
```

**Exemplo de resposta:**

```json
{
  "source": "calculator_llm_parser",
  "result": 7
}
```

---

**Exemplo POST com pergunta sobre cotação do dólar:**

```json
{
  "prompt": "Quanto está o dólar hoje?",
  "model": "llama3:latest"
}
```

**Exemplo de resposta:**

```json
{
  "source": "exchange_api",
  "result": "O dólar está cotado a R$ 5.25"
}
```

---

**Exemplo POST com pergunta geral de conhecimento:**

```json
{
  "prompt": "Quem foi Albert Einstein?",
  "model": "llama3:latest"
}
```

**Exemplo de resposta:**

```json
{
  "source": "llm_direct",
  "result": "Albert Einstein foi um físico teórico alemão, famoso por desenvolver a teoria da relatividade e contribuir para a física moderna."
}
```


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

# Baixando modelos no Ollama

Para usar os modelos LLM, você precisa baixá-los no Ollama. Exemplos de modelos utilizados no projeto: `llama3:latest`, `deepseek-r1:latest`.

1. Instale o Ollama CLI seguindo as instruções oficiais: [https://ollama.com/download](https://ollama.com/download)
2. Faça login no Ollama CLI:

```bash
ollama login
```

3. Baixe o modelo desejado:

```bash
ollama pull llama3:latest
ollama pull deepseek-r1:latest
```

4. Verifique os modelos disponíveis:

```bash
ollama list models
```

Depois disso, os modelos estarão disponíveis para uso no backend da API e podem ser referenciados pelo nome ao enviar requests.


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

result = promptAnalysis("quanto é 20 vezes 5?", model="llama3:latest")
print(result)
# Output: {'source': 'calculator_regex', 'result': 100}

result2 = promptAnalysis("Tinha 5 pães, comprei mais dois, quantos pães eu tenho?", model="deepseek-r1:latest")
print(result2)
# Output: {'source': 'calculator_llm_parser', 'result': 7}
```

---


## Licença

MIT License – livre para uso e modificação.
