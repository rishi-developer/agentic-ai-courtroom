from typing import TypedDict, Annotated
import operator


class CourtroomState(TypedDict):

    case_id: int

    evidence: list

    arguments: Annotated[list, operator.add]

    testimonies: Annotated[list, operator.add]

    evidence_findings: Annotated[list, operator.add]

    current_stage: str

    verdict: str | None

    evidence_sufficient: bool