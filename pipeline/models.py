from typing import List, Literal

from pydantic import BaseModel, Field

CauseArea = Literal["ai_governance", "animal_welfare", "other"]


class DimensionNotes(BaseModel):
    scope: str
    reversibility: str
    tractability: str
    urgency: str
    counterfactual: str


class Score(BaseModel):
    cause_areas: List[CauseArea]
    impact_score: int = Field(ge=1, le=5)
    rationale: str
    dimension_notes: DimensionNotes
