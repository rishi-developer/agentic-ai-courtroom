from app.graph.state import CourtroomState


def initialize_trial(state: CourtroomState):

    print("Initializing courtroom trial...")

    return {
        "current_stage": "investigation",
        "arguments": [],
        "verdict": None
    }


def analyze_evidence(state: CourtroomState):

    print("Analyzing evidence...")

    evidence_count = len(state["evidence"])

    return {
        "current_stage": "evidence_analysis",
        "arguments": [
            f"Total evidence items available: {evidence_count}"
        ]
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