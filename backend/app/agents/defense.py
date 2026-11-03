from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from app.llm.openai_client import llm
from app.schemas.agent_outputs import AgentArgument
from app.tools.registry import get_agent_tools

from app.tools.case_tools import (
    get_case_details,
    get_case_suspects
)

from app.tools.evidence_tools import (
    get_case_evidence,
    search_case_evidence
)

from app.tools.witness_tools import get_case_witnesses


DEFENSE_TOOLS = get_agent_tools("defense")


llm_with_tools = llm.bind_tools(DEFENSE_TOOLS)

structured_llm = llm.with_structured_output(AgentArgument)


SYSTEM_PROMPT = """
You are the Defense Attorney Agent in a fictional courtroom simulation.

Your responsibilities:
1. Defend the accused using available case information.
2. Examine prosecution arguments and identify weaknesses.
3. Identify gaps and contradictions in the evidence.
4. Present reasonable alternative explanations.
5. Challenge unsupported prosecution claims.
6. Explain the reasoning behind every defense argument.

Rules:
1. Never invent evidence, witness statements or facts.
2. Use database tools to retrieve relevant case information.
3. Cite evidence using its actual evidence code.
4. Distinguish established facts from assumptions and inferences.
5. Do not claim that the accused is innocent merely because
   the prosecution has not established its case.
6. Acknowledge evidence that genuinely supports the prosecution.
7. Do not modify case records.

Return your final response using the AgentArgument schema.
"""


async def defense_agent(
    case_id: int,
    action: str = "opening_argument",
    challenged_argument: str | None = None
) -> AgentArgument:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            Case ID: {case_id}

            Required action: {action}

            Prosecution argument to challenge:
            {challenged_argument or "None"}

            Examine the relevant case information and prepare
            the defense response.
            """
        )
    ]

    tool_map = {
        tool.name: tool for tool in DEFENSE_TOOLS
    }

    # Retrieve relevant information through tools.
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
            "Defense Agent exceeded the maximum tool-calling rounds."
        )

    # Generate the final structured defense argument.
    result = await structured_llm.ainvoke(messages)

    return result