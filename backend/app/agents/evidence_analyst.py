from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from app.llm.openai_client import llm
from app.schemas.agent_outputs import EvidenceAnalysis
from app.tools.registry import get_agent_tools

from app.tools.case_tools import get_case_details
from app.tools.evidence_tools import (
    get_case_evidence,
    search_case_evidence
)
from app.tools.witness_tools import (
    get_case_witnesses,
    get_witness_details
)

EVIDENCE_TOOLS = get_agent_tools("evidence_analyst")


llm_with_tools = llm.bind_tools(EVIDENCE_TOOLS)

structured_llm = llm.with_structured_output(EvidenceAnalysis)


SYSTEM_PROMPT = """
You are the Evidence Analyst Agent in a fictional courtroom simulation.

Your responsibility is to objectively analyze evidence.

Your tasks:
1. Examine available case evidence.
2. Compare evidence with witness statements.
3. Identify contradictions and inconsistencies.
4. Identify missing information.
5. Classify findings as supported, unsupported,
   contradicted, or uncertain.
6. Recommend further investigation when necessary.

Rules:
1. Remain completely neutral.
2. Never favor the prosecution or defense.
3. Never invent evidence or witness statements.
4. Use database tools to retrieve case information.
5. Reference evidence using actual evidence codes.
6. Distinguish facts from assumptions and inferences.
7. Do not claim that evidence is authentic or legally admissible.
8. Do not modify case records.
9. If information is insufficient, explicitly state uncertainty.

Return your final response using the EvidenceAnalysis schema.
"""


async def evidence_analyst_agent(
    case_id: int,
    analysis_request: str = "Analyze all available case evidence."
) -> EvidenceAnalysis:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            Case ID: {case_id}

            Analysis request:
            {analysis_request}

            Retrieve the relevant evidence and witness information.
            Analyze it objectively and return your findings.
            """
        )
    ]

    tool_map = {
        tool.name: tool for tool in EVIDENCE_TOOLS
    }

    # Retrieve information through database tools.
    for _ in range(5):

        response = await llm_with_tools.ainvoke(messages)

        messages.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:

            selected_tool = tool_map.get(tool_call["name"])

            if selected_tool is None:
                raise ValueError(
                    f"Unknown tool: {tool_call['name']}"
                )

            tool_result = await selected_tool.ainvoke(
                tool_call["args"]
            )

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

    else:
        raise RuntimeError(
            "Evidence Analyst exceeded the maximum tool-calling rounds."
        )

    # Generate structured evidence analysis.
    result = await structured_llm.ainvoke(messages)

    return result