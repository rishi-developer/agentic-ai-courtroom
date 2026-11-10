from app.graph.state import CourtroomState

from app.agents.prosecutor import prosecutor_agent
from app.agents.defense import defense_agent
from app.agents.evidence_analyst import evidence_analyst_agent

from app.tools.case_tools import (
    get_case_details,
    get_case_suspects
)

from app.tools.evidence_tools import get_case_evidence

from app.tools.witness_tools import get_case_witnesses


from app.agents.witness import witness_agent
from app.agents.judge import judge_evaluation_agent

from app.graph.limits import MAX_QUESTIONS_PER_SIDE

from app.graph.limits import (
    MAX_DEBATE_ROUNDS,
    MAX_INVESTIGATION_CYCLES
)

from app.agents.judge import (
    judge_evaluation_agent,
    generate_final_verdict
)


def can_start_another_round(state: CourtroomState) -> bool:
    return state["current_round"] < MAX_DEBATE_ROUNDS


def can_investigate(state: CourtroomState) -> bool:
    return state["investigation_count"] < MAX_INVESTIGATION_CYCLES


async def initialize_trial(state: CourtroomState):

    case_id = state["case_id"]

    case_result = await get_case_details.ainvoke({
        "case_id": case_id
    })

    suspects_result = await get_case_suspects.ainvoke({
        "case_id": case_id
    })

    evidence_result = await get_case_evidence.ainvoke({
        "case_id": case_id
    })

    witnesses_result = await get_case_witnesses.ainvoke({
        "case_id": case_id
    })

    import json

    case_data = json.loads(case_result)
    suspects_data = json.loads(suspects_result)
    evidence_data = json.loads(evidence_result)
    witnesses_data = json.loads(witnesses_result)

    if not case_data["success"]:
        raise ValueError("Unable to retrieve case details")

    if not suspects_data["success"]:
        raise ValueError("Unable to retrieve suspects")

    if not evidence_data["success"]:
        raise ValueError("Unable to retrieve evidence")

    if not witnesses_data["success"]:
        raise ValueError("Unable to retrieve witnesses")

    return {
        "case_details": case_data["data"],
        "suspects": suspects_data["data"]["suspects"],
        "evidence": evidence_data["data"]["evidence"],
        "witnesses": witnesses_data["data"]["witnesses"],
        "current_stage": "initialization",
        "trial_status": "in_progress"
    }   


# def analyze_evidence(state: CourtroomState):

#     print("Analyzing evidence...")

#     evidence_count = len(state["evidence"])

#     return {
#         "current_stage": "evidence_analysis",
#         "arguments": [
#             f"Total evidence items available: {evidence_count}"
#         ]
#     }

async def evidence_analysis(state: CourtroomState):

    result = await evidence_analyst_agent(
        case_id=state["case_id"],
        analysis_request="Analyze the available case evidence and identify contradictions."
    )

    return {
        "evidence_findings": [result.model_dump()],
        "investigation_count": state["investigation_count"] + 1,
        "current_stage": "evidence_analysis"
    }

async def prosecutor_opening(state: CourtroomState):
    result = await prosecutor_agent(
        case_id=state["case_id"],
        action="opening_argument"
    )

    return {
        "arguments": [result.model_dump()],
        "current_stage": "prosecutor_opening"
    }


async def defense_opening(state: CourtroomState):
    result = await defense_agent(
        case_id=state["case_id"],
        action="opening_argument"
    )

    return {
        "arguments": [result.model_dump()],
        "current_stage": "defense_opening"
    }

def check_evidence(state: CourtroomState):

    if state["evidence_sufficient"]:
        return "sufficient"

    return "insufficient"


def prepare_arguments(state: CourtroomState):

    print("Preparing arguments...")

    return {
        "current_stage": "arguments"
    }


def conduct_investigation(state: CourtroomState):

    print("Conducting additional investigation...")

    return {
        "current_stage": "investigation"
    }

async def witness_response(state: CourtroomState):

    witness_id = state["selected_witness_id"]
    question = state["current_question"]
    questioner = state["current_questioner"]

    if not witness_id:
        raise ValueError("No witness selected")

    if not question:
        raise ValueError("No question provided")

    previous_testimony = None

    for testimony in reversed(state["testimonies"]):
        if testimony["witness_id"] == witness_id:
            previous_testimony = testimony["response"]
            break

    result = await witness_agent(
        witness_id=witness_id,
        question=question,
        previous_testimony=previous_testimony
    )

    updates = {
        "testimonies": [result.model_dump()],
        "questions_for_current_witness": (
            state["questions_for_current_witness"] + 1
        ),
        "current_stage": "witness_response"
    }

    if questioner == "prosecutor":
        updates["prosecutor_questions"] = (
            state["prosecutor_questions"] + 1
        )

    elif questioner == "defense":
        updates["defense_questions"] = (
            state["defense_questions"] + 1
        )

    return updates

async def judge_evaluation(state: CourtroomState):
    trial_context = {
        "case_details": state["case_details"],
        "evidence": state["evidence"],
        "evidence_findings": state["evidence_findings"],
        "arguments": state["arguments"],
        "testimonies": state["testimonies"],
        "current_round": state["current_round"]
    }

    result = await judge_evaluation_agent(
        case_id=state["case_id"],
        trial_context=str(trial_context)
    )

    return {
        "judge_evaluation": result.model_dump(),
        "current_stage": "judge_evaluation"
    }




async def prosecutor_question(state: CourtroomState):

    if state["prosecutor_questions"] >= MAX_QUESTIONS_PER_SIDE:
        return {
            "current_question": None,
            "current_questioner": None,
            "current_stage": "prosecutor_questions_completed"
        }

    question = (
        "Ask one relevant question to establish the prosecution's position. "
        f"Case context: {state['case_details']}"
    )

    return {
        "current_question": question,
        "current_questioner": "prosecutor",
        "current_stage": "prosecutor_question"
    }

async def defense_question(state: CourtroomState):

    if state["defense_questions"] >= MAX_QUESTIONS_PER_SIDE:
        return {
            "current_question": None,
            "current_questioner": None,
            "current_stage": "defense_questions_completed"
        }

    question = (
        "Ask one relevant cross-examination question that tests the "
        "reliability or accuracy of the witness's statement. "
        f"Previous testimony: {state['testimonies']}"
    )

    return {
        "current_question": question,
        "current_questioner": "defense",
        "current_stage": "defense_question"
    }


async def select_witness(state: CourtroomState):

    witnesses = state["witnesses"]
    index = state["witness_index"]

    if index >= len(witnesses):
        return {
            "selected_witness_id": None,
            "current_stage": "witnesses_completed"
        }

    witness = witnesses[index]

    return {
        "selected_witness_id": witness["id"],
        "questions_for_current_witness": 0,
        "prosecutor_questions": 0,
        "defense_questions": 0,
        "current_stage": "witness_selected"
    }

async def prosecutor_argument(state: CourtroomState):
    trial_context = {
        "evidence": state["evidence"],
        "evidence_findings": state["evidence_findings"],
        "testimonies": state["testimonies"],
        "previous_arguments": state["arguments"],
        "current_round": state["current_round"]
    }

    result = await prosecutor_agent(
        case_id=state["case_id"],
        action="present_argument",
        challenged_argument=str(trial_context)
    )

    return {
        "arguments": [result.model_dump()],
        "current_stage": "prosecutor_argument"
    }

async def defense_argument(state: CourtroomState):
    trial_context = {
        "evidence": state["evidence"],
        "evidence_findings": state["evidence_findings"],
        "testimonies": state["testimonies"],
        "previous_arguments": state["arguments"],
        "current_round": state["current_round"]
    }

    result = await defense_agent(
        case_id=state["case_id"],
        action="challenge_prosecution",
        challenged_argument=str(trial_context)
    )

    return {
        "arguments": [result.model_dump()],
        "current_stage": "defense_argument"
    }

def route_after_judgment(state: CourtroomState):

    evaluation = state["judge_evaluation"]

    if not evaluation:
        raise ValueError("Judge evaluation is missing")

    decision = evaluation["decision"]

    if decision in ["continue_trial", "request_another_round"]:
        if can_start_another_round(state):
            return "prosecutor_argument"

        return "final_verdict"

    if decision == "request_clarification":
        return "clarification"

    if decision == "request_investigation":
        if can_investigate(state):
            return "additional_evidence_analysis"

        if can_start_another_round(state):
            return "prosecutor_argument"

        return "final_verdict"

    if decision == "conclude_trial":
        return "final_verdict"

    raise ValueError(f"Invalid judge decision: {decision}")

async def clarification(state: CourtroomState):

    evaluation = state["judge_evaluation"]

    target_agent = evaluation.get("target_agent")
    question = evaluation.get("question")

    if not target_agent or not question:
        raise ValueError(
            "Judge must provide target_agent and question for clarification"
        )

    if target_agent == "prosecutor":
        result = await prosecutor_agent(
            case_id=state["case_id"],
            action="clarification",
            challenged_argument=question
        )

    elif target_agent == "defense":
        result = await defense_agent(
            case_id=state["case_id"],
            action="clarification",
            challenged_argument=question
        )

    else:
        raise ValueError(f"Invalid clarification target: {target_agent}")

    return {
        "arguments": [result.model_dump()],
        "current_stage": "clarification"
    }

async def increment_debate_round(state: CourtroomState):

    return {
        "current_round": state["current_round"] + 1,
        "debate_count": state["debate_count"] + 1,
        "current_stage": "new_debate_round"
    }

async def final_verdict(state: CourtroomState):

    accused = (
        state["suspects"][0]["name"]
        if state["suspects"]
        else "Unknown"
    )

    trial_context = {
        "case_details": state["case_details"],
        "evidence": state["evidence"],
        "evidence_findings": state["evidence_findings"],
        "arguments": state["arguments"],
        "testimonies": state["testimonies"],
        "current_round": state["current_round"],
        "investigation_count": state["investigation_count"]
    }

    result = await generate_final_verdict(
        case_id=state["case_id"],
        accused=accused,
        trial_context=str(trial_context)
    )

    return {
        "verdict": result.model_dump(),
        "trial_status": "completed",
        "current_stage": "trial_completed"
    }

def advance_witness(state: CourtroomState):
    return {
        "witness_index": state["witness_index"] + 1,
        "selected_witness_id": None,
        "current_question": None,
        "current_questioner": None,
        "current_stage": "advance_witness"
    }

def route_after_witness_selection(state: CourtroomState):
    if state["selected_witness_id"]:
        return "prosecutor_question"

    return "witnesses_completed"


def route_after_prosecutor_question(state: CourtroomState):
    if state["current_question"]:
        return "witness_response"

    return "defense_question"


def route_after_defense_question(state: CourtroomState):
    if state["current_question"]:
        return "witness_response"

    return "advance_witness"


def route_after_witness_response(state: CourtroomState):
    if state["current_questioner"] == "prosecutor":
        return "defense_question"

    return "advance_witness"

async def additional_evidence_analysis(state: CourtroomState):

    result = await evidence_analyst_agent(
        case_id=state["case_id"],
        analysis_request=(
            "Re-evaluate the case evidence, considering the "
            "current arguments and testimonies. Identify "
            "contradictions and unresolved issues."
        )
    )

    return {
        "evidence_findings": [result.model_dump()],
        "investigation_count": state["investigation_count"] + 1,
        "current_stage": "additional_evidence_analysis"
    }



