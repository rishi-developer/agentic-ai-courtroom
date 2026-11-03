import json

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from app.llm.openai_client import llm
from app.schemas.agent_outputs import WitnessResponse
from app.tools.registry import get_agent_tools

from app.tools.witness_tools import get_witness_details

WITNESS_TOOLS = get_agent_tools("witness")

llm_with_tools = llm.bind_tools(WITNESS_TOOLS)

structured_llm = llm.with_structured_output(WitnessResponse)


SYSTEM_PROMPT = """
You are a Witness Agent in a fictional courtroom simulation.

Your responsibility is to simulate a specific witness.

Rules:

1. Answer only using the witness's knowledge profile,
   original statement, and supplied previous testimony.

2. Never invent events, observations, conversations,
   or personal knowledge.

3. If you do not know something, clearly say so.

4. Distinguish between what you personally observed
   and what you assume or believe.

5. Do not change your original statement just to satisfy
   the prosecutor or defense.

6. If a question contains an incorrect assumption,
   politely correct that assumption.

7. If a question asks about something outside your
   knowledge, return knowledge_status as "unknown".

8. If the information is incomplete or ambiguous,
   return knowledge_status as "uncertain".

9. Identify whether your response contradicts
   previous testimony.

10. Do not favor either the prosecution or defense.

Return your final response using the WitnessResponse schema.
"""


async def witness_agent(
    witness_id: int,
    question: str,
    previous_testimony: str | None = None
) -> WitnessResponse:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            Witness ID: {witness_id}

            Question:
            {question}

            Previous testimony:
            {previous_testimony or "No previous testimony provided."}

            Retrieve your witness profile and answer the question
            strictly according to your available knowledge.
            """
        )
    ]

    tool_map = {
        tool.name: tool for tool in WITNESS_TOOLS
    }

    # Retrieve witness information.
    for _ in range(3):

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
            "Witness Agent exceeded the maximum tool-calling rounds."
        )

    result = await structured_llm.ainvoke(messages)

    # Ensure the returned response belongs to the requested witness.
    if result.witness_id != witness_id:
        raise ValueError("Witness ID mismatch in agent response.")

    return result