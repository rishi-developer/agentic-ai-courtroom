from typing import Literal
from pydantic import BaseModel, Field


class AgentArgument(BaseModel):
    agent: Literal["prosecutor", "defense"]
    action: str
    argument: str
    supporting_evidence: list[str] = Field(default_factory=list)
    challenged_argument: str | None = None
    reasoning: str
    requires_response: bool



class EvidenceFinding(BaseModel):
    finding: str
    evidence_ids: list[str] = Field(default_factory=list)
    status: Literal[
        "supported",
        "unsupported",
        "contradicted",
        "uncertain"
    ]


class EvidenceAnalysis(BaseModel):
    findings: list[EvidenceFinding] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class WitnessResponse(BaseModel):
    witness_id: int
    question: str
    response: str
    knowledge_status: Literal[
        "known",
        "unknown",
        "uncertain"
    ]
    supporting_evidence: list[str] = Field(default_factory=list)
    contradicts_previous_statement: bool = False


class JudgeEvaluation(BaseModel):
    decision: Literal[
        "continue_trial",
        "request_clarification",
        "request_investigation",
        "request_another_round",
        "conclude_trial"
    ]
    target_agent: str | None = None
    question: str | None = None
    reasoning: str
    trial_complete: bool


class FinalVerdict(BaseModel):
    outcome: Literal["guilty", "not_proven"]
    accused: str
    prosecution_assessment: str
    defense_assessment: str
    evidence_considered: list[str] = Field(default_factory=list)
    reasoning: str
    unresolved_questions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)