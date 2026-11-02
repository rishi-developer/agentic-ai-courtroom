from pydantic import BaseModel, Field


class EvidenceSubmission(BaseModel):
    case_id: int
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    evidence_type: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=5)