import operator
from typing import Annotated, TypedDict
class CourtroomState(TypedDict):
    # Identifiers
    case_id: int
    trial_id: int
    # Case information
    case_details: dict
    suspects: list
    evidence: list
    witnesses: list
    # Workflow information
    current_stage: str
    trial_status: str
    # Debate information
    current_round: int
    debate_count: int
    # Agent outputs
    arguments: Annotated[list, operator.add]
    testimonies: Annotated[list, operator.add]
    evidence_findings: Annotated[list, operator.add]
    # Judge
    judge_evaluation: dict | None
    # Witness examination
    selected_witness_id: int | None
    witness_index: int
    questions_for_current_witness: int
    current_questioner: str | None
    # User interaction
    user_input: dict | None
    pending_user_action: str | None
    # Investigation
    investigation_count: int
    # Final result
    verdict: dict | None
    error: str | None
    current_question: str | None
    prosecutor_questions: int
    defense_questions: int