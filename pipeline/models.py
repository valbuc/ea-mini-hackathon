from typing import List, Literal

from pydantic import BaseModel, Field

CauseArea = Literal[
    "ai_governance",
    "existential_catastrophic_risk",
    "global_catastrophic_risks",
    "animal_welfare",
    "global_health_development",
    "climate_change_mitigation",
    "meta_ea_infrastructure",
    "mental_health_wellbeing",
    "longtermism",
    "other",
]

DIMENSION_NAMES = ("scope", "reversibility", "tractability", "urgency", "counterfactual")


class DimensionScore(BaseModel):
    score: int = Field(ge=1, le=5)
    note: str


class Dimensions(BaseModel):
    scope: DimensionScore
    reversibility: DimensionScore
    tractability: DimensionScore
    urgency: DimensionScore
    counterfactual: DimensionScore


class LLMScore(BaseModel):
    """Schema for what we ask Claude to return per consultation.

    `impact_score` is intentionally not part of the LLM output — we compute it
    deterministically as the average of the five dimension scores.
    """

    cause_areas: List[CauseArea]
    rationale: str
    dimensions: Dimensions
