#!/usr/bin/env python3
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime
from ollama import chat
import json
import psutil
import os
import re
from enum import Enum

app = FastAPI(title="Artefact IA Gen tool")

class LabelEnum(str, Enum):
    IS_MATH_OPERATION = "IS_MATH_OPERATION"
    NOT_MATH = "NOT_MATH_OPERATION"
    
# ----------------- Schemas -----------------
class DetectMathOperation(BaseModel):
    isMathOperation: LabelEnum


def isMathOperation(prompt):
    response = chat(
        messages=[
            {
                "role": "system",
                "content": "You are a specialized math agent. Return if the user is asking for a mathematical operation"
            },
            {"role": "user", "content": prompt}
        ],
        model="llama3:latest",
        format=DetectMathOperation.model_json_schema(),
        stream=False
    )

    content = (response.message.content or "").strip()
    print("🧠 Raw Ollama response:", content)

    return content

# ----------------- Endpoint principal -----------------
@app.post("/ia")
async def analyze_userInput(request: Request):
    data = await request.json()
    print("📥 Recebido:", data)

    try:
        # Construir prompt
        prompt = data["prompt"]

        # Medir tokens (simples contagem de palavras)
        token_count = len(prompt.split())
        print(f"📥 Prompt length: {len(prompt)} chars")
        print(f"🔢 Token count (approx): {token_count}")

        # ---------- Envio ao modelo Ollama ----------
        response = isMathOperation(prompt)
        print(response)
        # Parsing seguro
        # try:
        #     result = DosAnalysis.model_validate_json(content)
        # except Exception:
        #     match = re.search(r"\{[\s\S]*\}", content)
        #     if not match:
        #         raise ValueError("Não foi possível encontrar JSON válido na resposta do modelo.")
        #     result = DosAnalysis.model_validate_json(match.group(0))

        # results_by_id[exec_id] = result
        # print("✅ Parsed result:", result)

        # # Métricas
        # metrics = measure_resources(start_time)

        # # Salvar log
        # log_data = {
        #     "id": exec_id,
        #     "datetime": start_time.isoformat(),
        #     "requestTokens": token_count,
        #     "requestChars": len(prompt),
        #     "request": data,
        #     "response": result.dict(),
        #     **metrics
        # }
        # append_requests_log(log_data)

    #     return {"exec_id": exec_id, "result": result}

    except Exception as e:
        print(e)
    #     append_requests_log({
    #         "id": exec_id,
    #         "datetime": datetime.now().isoformat(),
    #         "error": str(e),
    #         "request": data
    #     })
    #     print("❌ Erro ao processar a requisição:", e)
    #     raise HTTPException(status_code=500, detail="Erro interno ao processar a solicitação.")



# ----------------- Test endpoint -----------------
@app.get("/test")
async def test():
    return {"status": "API is running. Use POST /ia with packet data to analyze."}

# ----------------- Inicialização -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
