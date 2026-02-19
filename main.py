from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from fastapi import HTTPException


from services.prompt_analisis_service import promptAnalysis

app = FastAPI(title="Artefact AI Gen Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IARequest(BaseModel):
    prompt: str
    model: Optional[str] = None


@app.post("/ia")
async def analyze_userInput(data: IARequest):
    prompt = data.prompt.strip()
    model = data.model

    if not prompt:
        return {"error": "Prompt vazio"}

    try:
        result = promptAnalysis(prompt, model)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Não foi possível analisar o prompt recebido.")


@app.get("/test")
async def test():
    return {"status": "API is running."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)