from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Talk2Tasks", version="0.1")

# --------- MODELES ---------

class Task(BaseModel):
    tâche: str
    responsable: Optional[str] = None
    priorité: Optional[str] = None
    échéance: Optional[str] = None

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Texte brut issu d'une réunion, discussion, ou brief.")

class AnalyzeResponse(BaseModel):
    résumé: str
    plan_d_action: List[Task]


# --------- ENDPOINTS ---------

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest):
    # MOCK : remplacer par appel LLM / LangGraph plus tard
    mock_résumé = "La réunion porte sur la refonte mobile, un blocage juridique, et un décalage d’intégration technique."

    mock_tasks = [
        Task(
            tâche="Finaliser les maquettes mobile",
            responsable="UX",
            priorité="haute",
            échéance="mardi"
        ),
        Task(
            tâche="Relancer le service juridique",
            responsable="PO",
            priorité="moyenne"
        ),
        Task(
            tâche="Replanifier l'intégration backend",
            responsable="Tech lead",
            priorité="moyenne"
        )
    ]

    return AnalyzeResponse(résumé=mock_résumé, plan_d_action=mock_tasks)