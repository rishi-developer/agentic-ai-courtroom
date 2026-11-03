from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from app.llm.openai_client import llm
from app.tools.registry import get_agent_tools

from app.schemas.agent_outputs import (
    JudgeEvaluation,
    FinalVerdict
)

from app.tools.case_tools import get_case_details

from app.tools.evidence_tools import (
    get_case_evidence,
    search_case_evidence
)

from app.tools.witness_tools import get_case_witnesses


JUDGE_TOOLS = get_agent_tools("judge")


llm_with_tools = llm.bind_tools(JUDGE_TOOLS)

evaluation_llm = llm.with_structured_output(JudgeEvaluation)

verdict_llm = llm.with_structured_output(FinalVerdict)


JUDGE_SYSTEM_PROMPT = """
You are the Judge Agent in a fictional courtroom simulation.

Your responsibilities:
1. Evaluate prosecution and defense arguments objectively.
2. Examine available evidence and witness testimony.
3. Identify unsupported claims and unresolved questions.
4. Ensure both sides receive fair consideration.
5. Decide what should happen next in the trial.

Possible decisions:
- continue_trial
- request_clarification
- request_investigation
- request_another_round
- conclude_trial

Rules:
1. Remain neutral.
2. Never invent facts, evidence or testimony.
3. Do not automatically accept an agent's claims.
4. Distinguish facts from assumptions and inferences.
5. Consider arguments from both sides.
6. Do not conclude guilt merely because the defense
   has failed to provide evidence.
7. Request further investigation when important
   information is missing.
8. Do not modify case records.

Return your decision using the JudgeEvaluation schema.
"""


VERDICT_SYSTEM_PROMPT = """
You are the Judge Agent responsible for producing the
final verdict in a fictional courtroom simulation.

Evaluate the complete trial fairly and objectively.

Your responsibilities:
1. Evaluate the prosecution's arguments.
2. Evaluate the defense's arguments.
3. Examine all relevant evidence.
4. Consider witness testimonies.
5. Explain the reasoning behind your verdict.
6. Identify unresolved questions and limitations.

Possible outcomes:
- guilty
- not_proven

Rules:
1. Never invent evidence or testimony.
2. Never favor either side.
3. Consider both supporting and contradictory evidence.
4. Do not declare guilt merely because the defense
   failed to establish an alternative explanation.
5. If the evidence is insufficient to establish guilt,
   return not_proven.
6. Explain uncertainty and limitations clearly.
7. This is a fictional educational simulation,
   not a real legal judgment.

Return your final response using the FinalVerdict schema.
"""


async def _run_judge_tools(messages: list):

    tool_map = {
        tool.name: tool for tool in JUDGE_TOOLS
    }

    for _ in range(5):

        response = await llm_with_tools.ainvoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return messages

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

    raise RuntimeError(
        "Judge exceeded the maximum tool-calling rounds."
    )


async def judge_evaluation_agent(
    case_id: int,
    trial_context: str
) -> JudgeEvaluation:

    messages = [
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            Case ID: {case_id}

            Current trial information:
            {trial_context}

            Retrieve relevant case information, evidence and witnesses.

            Evaluate the current trial and decide what should happen next.
            """
        )
    ]

    messages = await _run_judge_tools(messages)

    result = await evaluation_llm.ainvoke(messages)

    return result


async def generate_final_verdict(
    case_id: int,
    accused: str,
    trial_context: str
) -> FinalVerdict:

    messages = [
        SystemMessage(content=VERDICT_SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            Case ID: {case_id}

            Accused:
            {accused}

            Complete trial information:
            {trial_context}

            Retrieve the relevant case information and evidence.

            Evaluate both sides and produce the final verdict.
            """
        )
    ]

    messages = await _run_judge_tools(messages)

    result = await verdict_llm.ainvoke(messages)

    return result