from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    case_type: str = Field(min_length=3, max_length=100)


class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    case_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)