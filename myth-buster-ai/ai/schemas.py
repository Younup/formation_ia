from pydantic import BaseModel, Field


class Segment(BaseModel):
    content: str = Field(..., description="Le contenu textuel du segment")
    id: int = Field(..., description="Un identifiant unique pour le segment")


class Claim(BaseModel):
    content: str = Field(..., description="L'affirmation factuelle extraite du texte")
    segment_id: int = Field(..., description="Identifiant du segment d'où l'affirmation a été extraite")

class Claims(BaseModel):
    items: list[Claim] = Field(..., description="Liste des affirmations extraites du texte")

class Bias(BaseModel):
    content: str = Field(..., description="Le biais détecté dans le texte")
    segment_id: int = Field(..., description="Identifiant du segment d'où le biais a été extrait")
    bias_type: str = Field(..., description="Le type de biais détecté (émotionnel, idéologique, exagération, omission, autre...)")
    explanation: str = Field(..., description="Justification brève du biais détecté")
    
class Biases(BaseModel):
    items: list[Bias] = Field(..., description="Liste des biais détectés dans le texte")