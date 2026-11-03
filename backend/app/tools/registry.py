from app.tools.case_tools import (
    get_case_details,
    get_case_suspects
)

from app.tools.evidence_tools import (
    search_case_evidence,
    get_evidence_details,
    get_case_evidence
)

from app.tools.witness_tools import (
    get_case_witnesses,
    get_witness_details
)


from app.tools.trial_tools import (
    get_trial_arguments,
    get_trial_testimonies
)

from app.tools.evidence_submission_tools import (
    submit_new_evidence
)


# Read-only tools
READ_ONLY_TOOLS = [
    get_case_details,
    get_case_suspects,
    get_case_evidence,
    search_case_evidence,
    get_evidence_details,
    get_case_witnesses,
    get_witness_details,
    get_trial_arguments,
    get_trial_testimonies
]

# Tools that modify database records
WRITE_TOOLS = [
    submit_new_evidence
]

# All registered tools
ALL_TOOLS = READ_ONLY_TOOLS + WRITE_TOOLS


AGENT_TOOLS = {
    "prosecutor": [
        get_case_details,
        get_case_suspects,
        get_case_evidence,
        search_case_evidence,
        get_case_witnesses,
        get_witness_details
    ],

    "defense": [
        get_case_details,
        get_case_suspects,
        get_case_evidence,
        search_case_evidence,
        get_case_witnesses,
        get_witness_details
    ],

    "evidence_analyst": [
        get_case_details,
        get_case_evidence,
        search_case_evidence,
        get_case_witnesses,
        get_witness_details
    ],

    "witness": [
        get_witness_details
    ],

    "judge": [
        get_case_details,
        get_case_suspects,
        get_case_evidence,
        search_case_evidence,
        get_case_witnesses,
        get_witness_details
    ]
}


def get_agent_tools(agent_name: str):
    tools = AGENT_TOOLS.get(agent_name)

    if tools is None:
        raise ValueError(
            f"Unknown agent: {agent_name}"
        )

    return tools