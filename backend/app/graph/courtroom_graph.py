
from langgraph.graph import StateGraph, START, END

from app.graph.state import CourtroomState

from app.graph.nodes import (
    initialize_trial,
    evidence_analysis,
    additional_evidence_analysis,
    prosecutor_opening,
    defense_opening,
    select_witness,
    prosecutor_question,
    witness_response,
    defense_question,
    advance_witness,
    prosecutor_argument,
    defense_argument,
    judge_evaluation,
    clarification,
    increment_debate_round,
    final_verdict,
    route_after_judgment,
    route_after_witness_selection,
    route_after_prosecutor_question,
    route_after_defense_question,
    route_after_witness_response
)

builder = StateGraph(CourtroomState)

# Register nodes
builder.add_node("initialize_trial", initialize_trial)
builder.add_node("evidence_analysis", evidence_analysis)

builder.add_node("prosecutor_opening", prosecutor_opening)
builder.add_node("defense_opening", defense_opening)

builder.add_node("select_witness", select_witness)
builder.add_node("prosecutor_question", prosecutor_question)
builder.add_node("witness_response", witness_response)
builder.add_node("defense_question", defense_question)
builder.add_node("advance_witness", advance_witness)

builder.add_node("prosecutor_argument", prosecutor_argument)
builder.add_node("defense_argument", defense_argument)

builder.add_node("judge_evaluation", judge_evaluation)
builder.add_node("clarification", clarification)
builder.add_node("increment_debate_round", increment_debate_round)

builder.add_node(
    "additional_evidence_analysis",
    additional_evidence_analysis
)

builder.add_node("final_verdict", final_verdict)


# Initial workflow
builder.add_edge(START, "initialize_trial")
builder.add_edge("initialize_trial", "evidence_analysis")
builder.add_edge("evidence_analysis", "prosecutor_opening")
builder.add_edge("prosecutor_opening", "defense_opening")

# Witness selection
builder.add_edge("defense_opening", "select_witness")

builder.add_conditional_edges(
    "select_witness",
    route_after_witness_selection,
    {
        "prosecutor_question": "prosecutor_question",
        "witnesses_completed": "prosecutor_argument"
    }
)

# Prosecutor examination
builder.add_conditional_edges(
    "prosecutor_question",
    route_after_prosecutor_question,
    {
        "witness_response": "witness_response",
        "defense_question": "defense_question"
    }
)

# Witness response routing
builder.add_conditional_edges(
    "witness_response",
    route_after_witness_response,
    {
        "defense_question": "defense_question",
        "advance_witness": "advance_witness"
    }
)

# Defense cross-examination
builder.add_conditional_edges(
    "defense_question",
    route_after_defense_question,
    {
        "witness_response": "witness_response",
        "advance_witness": "advance_witness"
    }
)

# Move to next witness
builder.add_edge("advance_witness", "select_witness")


# Arguments and judge evaluation
builder.add_edge("prosecutor_argument", "defense_argument")
builder.add_edge("defense_argument", "judge_evaluation")


# Judge's decisions
builder.add_conditional_edges(
    "judge_evaluation",
    route_after_judgment,
    {
        "prosecutor_argument": "increment_debate_round",
        "clarification": "clarification",
        "additional_evidence_analysis": "additional_evidence_analysis",
        "final_verdict": "final_verdict"
    }
)

builder.add_edge("increment_debate_round", "prosecutor_argument")
builder.add_edge("clarification", "judge_evaluation")
builder.add_edge("additional_evidence_analysis", "prosecutor_argument")

# Complete trial
builder.add_edge("final_verdict", END)

courtroom_graph = builder.compile()
