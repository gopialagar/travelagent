from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserPreference(BaseModel):
    destination_keywords: List[str] = Field(default_factory=list, description="Keywords related to destination (e.g., 'beach', 'Europe')")
    budget_max: Optional[float] = Field(None, description="Maximum budget for the trip")
    start_date: Optional[datetime] = Field(None, description="Preferred start date")
    duration_days: Optional[int] = Field(None, description="Preferred duration in days")

class TripOption(BaseModel):
    id: str
    destination: str
    cost: float
    duration_days: int
    description: str
    score: Optional[float] = Field(None, description="Relevance score based on preferences")

class Recommendation(BaseModel):
    top_option: TripOption
    alternatives: List[TripOption]
    reasoning: str
