from app.tools.registry import get_agent_tools


def test_all_agents_have_tools():

    agents = [
        "prosecutor",
        "defense",
        "evidence_analyst",
        "witness",
        "judge"
    ]

    for agent in agents:
        assert len(get_agent_tools(agent)) > 0


def test_witness_has_only_witness_details():

    tools = get_agent_tools("witness")

    tool_names = [tool.name for tool in tools]

    assert tool_names == ["get_witness_details"]


def test_agents_do_not_have_write_tools():

    agents = [
        "prosecutor",
        "defense",
        "evidence_analyst",
        "witness",
        "judge"
    ]

    for agent in agents:

        tools = get_agent_tools(agent)

        tool_names = [tool.name for tool in tools]

        assert "submit_new_evidence" not in tool_names


def test_unknown_agent_raises_error():

    try:
        get_agent_tools("unknown_agent")
        assert False, "Expected ValueError"

    except ValueError:
        assert True