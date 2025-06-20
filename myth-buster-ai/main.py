from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from dotenv import load_dotenv
from pydantic import BaseModel
from logger import logger
from ai import run_graph, Configuration, get_graph_as_png
load_dotenv()

app = FastAPI(title="MythBusterAI", version="0.1")

# --------- ENDPOINTS ---------

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)


class AnalyzeRequest(BaseModel):
    input: str

class AnalyzeResponse(BaseModel):
    answer: str  

configuration = Configuration(
    extract_claims_model="gpt-4o-mini",
    verify_claims_model="gpt-4o-mini",
    extract_biases_model="gpt-4o-mini",
    answer_model="gpt-4o",
    segmentation_mode="recursive",
    claim_verification_source="llm"
)

@app.get("/analyze", description="Visualize the agent graph")
async def visualize_deep_search_graph():
    return Response(content=get_graph_as_png(), media_type="image/png")


@app.post("/analyze", response_model=dict)
async def execute_deep_search(payload: AnalyzeRequest):
    logger.debug(f"Received input: {payload.input}")
    response = await run_graph(payload.input, configuration)
    logger.debug(f"Deep search response: {response}")
    return response