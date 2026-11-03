import pytest
import json
from app.agents.prosecutor import prosecutor_agent
from app.tools.evidence_tools import get_case_evidence
from app.agents.witness import witness_agent
from app.agents.judge import judge_evaluation_agent
from app.schemas.agent_outputs import AgentArgument
from pydantic import ValidationError


@pytest.mark.asyncio(loop_scope="session")
async def test_prosecutor_uses_real_evidence():

    result = await prosecutor_agent(
        case_id=1,
        action="opening_argument"
    )

    evidence_result = await get_case_evidence.ainvoke({
        "case_id": 1
    })

    evidence_data = json.loads(evidence_result)

    assert evidence_data["success"] is True

    valid_codes = {
        item["evidence_code"]
        for item in evidence_data["data"]["evidence"]
    }

    for evidence_code in result.supporting_evidence:
        assert evidence_code in valid_codes

@pytest.mark.asyncio(loop_scope="session")
async def test_witness_admits_unknown_information():

    result = await witness_agent(
        witness_id=1,
        question="What was inside Alex's bag?"
    )

    assert result.knowledge_status in [
        "unknown",
        "uncertain"
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_judge_returns_valid_decision():

    result = await judge_evaluation_agent(
        case_id=1,
        trial_context="""
        Prosecutor: Alex entered the server room.
        Defense: There is no direct evidence of laptop removal.
        Witness: David saw Alex carrying a black bag.
        """
    )

    assert result.decision in [
        "continue_trial",
        "request_clarification",
        "request_investigation",
        "request_another_round",
        "conclude_trial"
    ]


def test_invalid_agent_argument_is_rejected():

    with pytest.raises(ValidationError):

        AgentArgument(
            agent="judge",
            action="opening",
            argument="Alex is guilty.",
            supporting_evidence=[],
            reasoning="Invalid agent type.",
            requires_response=False
        )