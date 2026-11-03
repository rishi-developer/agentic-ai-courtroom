from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

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


PROSECUTOR_TOOLS = get_agent_tools("prosecutor")

llm_with_tools = llm.bind_tools(PROSECUTOR_TOOLS)

structured_llm = llm.with_structured_output(AgentArgument)


SYSTEM_PROMPT = """
You are the Prosecutor Agent in a fictional courtroom simulation.

Your responsibilities:
1. Build arguments supporting the prosecution.
2. Examine case details, suspects, evidence and witnesses.
3. Identify evidence that supports the prosecution.
4. Challenge arguments made by the defense when relevant.
5. Explain the reasoning behind every argument.

Rules:
1. Never invent evidence, witness statements or facts.
2. Use database tools to retrieve case information.
3. Cite evidence using its actual evidence code.
4. Distinguish established facts from assumptions and inferences.
5. Do not claim that circumstantial evidence proves something
   it does not actually establish.
6. If evidence is insufficient, acknowledge its limitations.
7. Do not modify case records.

Return your final response using the AgentArgument schema.
"""


async def prosecutor_agent(
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

            Argument to challenge:
            {challenged_argument or "None"}

            Examine the relevant case information and prepare
            the prosecution's response.
            """
        )
    ]

    tool_map = {
        tool.name: tool for tool in PROSECUTOR_TOOLS
    }

    # Allow the LLM to retrieve information using tools.
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
            "Prosecutor exceeded the maximum tool-calling rounds."
        )

    # Convert the gathered information into structured output.
    result = await structured_llm.ainvoke(messages)

    return result