from ai.state import State
from ai.schemas import Claims
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate







prompt = PromptTemplate.from_template("""
Tu es un assistant chargé d'extraire les affirmations factuelles explicites contenues dans un texte.

Une affirmation factuelle :
- est une déclaration pouvant être vérifiée comme vraie ou fausse,
- est formulée de manière affirmative,
- n’est pas une simple opinion, une question ou un commentaire flou.

Tu vas recevoir une liste de segments. Pour chacun, décide s’il contient une affirmation factuelle, et si oui, extrait-la telle quelle (ou reformule-la légèrement si nécessaire pour qu’elle soit autonome et compréhensible hors contexte).

Renvoie uniquement la liste des affirmations factuelles détectées, sous forme de tableau JSON.

Exemple attendu :
[
  "Le vaccin X a été responsable de 400 effets secondaires en 2022.",
  "La température moyenne a augmenté de 1,1°C depuis 1900.",
  "L’article 15 du RGPD impose un droit d’accès aux données personnelles."
]

Segments:
{segments}
""")

async def extract_claims(state: State):
    model = state["configuration"].extract_claims_model
    llm = init_chat_model(model, model_provider="openai").with_structured_output(Claims)
    formated_segments = ("\n").join( [f"id: {segment.id} - content: {segment.content}" for segment in state["segments"]])
    response = prompt.pipe(llm).invoke({"segments": formated_segments}) 
    claims = Claims.model_validate(response)  # Validate the response against the Claims schema

    
    return {"claims": claims.items}  # Return the claims in the expected format