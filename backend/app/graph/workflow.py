from langgraph.graph import StateGraph, START, END

from app.graph.state import CourtroomState

from app.graph.nodes import (
    initialize_trial,
    analyze_evidence,
    check_evidence,
    prepare_arguments,
    conduct_investigation
)


workflow = StateGraph(CourtroomState)

# Register nodes
workflow.add_node("initialize_trial", initialize_trial)
workflow.add_node("analyze_evidence", analyze_evidence)
workflow.add_node("prepare_arguments", prepare_arguments)
workflow.add_node("conduct_investigation", conduct_investigation)

# Normal edges
workflow.add_edge(START, "initialize_trial")
workflow.add_edge("initialize_trial", "analyze_evidence")

# Conditional routing
workflow.add_conditional_edges(
    "analyze_evidence",
    check_evidence,
    {
        "sufficient": "prepare_arguments",
        "insufficient": "conduct_investigation"
    }
)

# Endpoints
workflow.add_edge("prepare_arguments", END)
workflow.add_edge("conduct_investigation", END)

app = workflow.compile()