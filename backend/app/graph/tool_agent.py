from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.llm.openai_client import llm
from app.tools.registry import READ_ONLY_TOOLS


llm_with_tools = llm.bind_tools(READ_ONLY_TOOLS)



async def agent_node(state: MessagesState):

    system_message = SystemMessage(
        content=(
            "You are an AI assistant for a fictional courtroom system. "
            "Use available tools to retrieve case information, evidence, "
            "witness details, and trial history. "
            "Never invent database records or evidence. "
            "Clearly distinguish retrieved facts from assumptions."
        )
    )

    response = await llm_with_tools.ainvoke(
        [system_message] + state["messages"]
    )

    return {"messages": [response]}


tool_node = ToolNode(READ_ONLY_TOOLS)


builder = StateGraph(MessagesState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge("tools", "agent")

tool_agent = builder.compile()