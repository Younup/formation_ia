import os

from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langgraph.graph import START, END

from ai.state import State
from ai.configuration import Configuration
from ai.nodes import (
    preprocess,
    detect_biases,
    extract_claims,
    verify_claims,
    aggregate_verdict,
    export_report
)
load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")

def continue_to_verify_claims(state: State):
    if len(state["claims"]) == 0:
        return 'no_claims'
    if state["configuration"].claim_verification_source == "web":
        return 'web_verification'
    return 'llm_verification'




# Create our Agent Graph
builder = StateGraph(State, config_schema=Configuration)

# Define the nodes we will cycle between
builder.add_node("preprocess", preprocess)
builder.add_node("detect_biases", detect_biases)
builder.add_node("extract_claims", extract_claims)
builder.add_node("verify_claims", verify_claims)
builder.add_node("aggregate_verdict", aggregate_verdict)
builder.add_node("export_report", export_report)

builder.add_edge(START, "preprocess")

builder.add_edge("preprocess", "detect_biases")
builder.add_edge("preprocess", "extract_claims")
builder.add_edge("extract_claims", "verify_claims")


builder.add_edge("detect_biases", "aggregate_verdict")
builder.add_edge("verify_claims", "aggregate_verdict")

builder.add_edge("aggregate_verdict", "export_report")

# Finalize the answer
builder.add_edge("export_report", END)

graph = builder.compile(name="myth-buster-ai")

async def run_graph(input: str, configuration: Configuration):
    """Run the graph with the given input and configuration."""
    response = await graph.ainvoke({
        "original_content": input,
        "configuration": configuration,
    })
    return response

def get_graph_as_png():
    return graph.get_graph().draw_mermaid_png()