from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from typing import Annotated, Literal, Any
from typing_extensions import TypedDict
from uuid import uuid4, UUID
load_dotenv()

app = FastAPI(title="Talk2Tasks", version="0.1")

# --------- MODELES ---------

class Task(BaseModel):
    tâche: str
    responsable: Optional[str] = None
    priorité: Optional[str] = None
    échéance: Optional[str] = None

class AnalyzeRequest(BaseModel):
    items: list[str] = Field(..., description="Texte brut issu d'une réunion, discussion, ou brief.")

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

    items = [ProcessedItem(id=uuid4(), original_content=item, cleaned_content=None, typologie=None, summary=None, insights=None, meta=None) for item in payload.items]



    return AnalyzeResponse(résumé=mock_résumé, plan_d_action=mock_tasks)

from langgraph.graph import StateGraph, START



class ProcessedItem(BaseModel):
    id: UUID = Field(..., description="Identifiant unique de l'item traité")
    original_content: str = Field(..., description="Texte brut de l'item")
    cleaned_content: Optional[str] = Field(None,  description="Texte nettoyé et formaté pour l'analyse")
    typologie: Optional[Literal["email", "notes","transcript", "other"]] = Field(None,  description="Type de l'item traité")
    summary: Optional[str] = Field(None, description="Résumé généré par le modèle")
    insights: Optional[List[str]] = Field(None, description="Insights ou points clés extraits du texte")
    meta: Optional[dict[str, Any]] = None  # Ex : score de confiance, logs, etc.

def item_reducer(existing: list[ProcessedItem], new: list[ProcessedItem]):
    """Merge a list of existing items with new items, updating by ID."""
    new_by_id = {item.id: item for item in new}
    updated: list[ProcessedItem] = []
    for item in existing:
        updated.append(new_by_id.pop(item.id, item))
    updated.extend(new_by_id.values())
    return updated

class GraphState(TypedDict):
    input: str
    items: Annotated[list[ProcessedItem], item_reducer]
    output: str


def preprocess(state: GraphState):
    return {}

def summarize(state: GraphState):
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = PromptTemplate.from_template(""""
Tu es un assistant intelligent chargé de résumer des comptes-rendus de réunion internes dans un format concis et clair.

Ton objectif est de produire un court résumé de 3 à 5 phrases qui synthétise :
- les sujets abordés,
- les points de friction ou blocages,
- les décisions prises ou propositions importantes.

Ne reformule pas tout mot à mot. Concentre-toi uniquement sur l’essentiel.

N’invente rien. Si une information n’est pas clairement présente, ignore-la.

Texte à résumer :
{ input }

Résumé :
""")
    model =ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    response = prompt.pipe(model).invoke({input: state['input']})
    return {"summary": response.content}

def extract_tasks(state: GraphState):
    return {}


def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node(preprocess)
    builder.add_node(summarize)
    builder.add_node(extract_tasks)
    pass

def run_graph():
    # Placeholder for graph execution logic
    pass

