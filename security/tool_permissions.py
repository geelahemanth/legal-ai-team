# security/tool_permissions.py


AGENT_TOOL_PERMISSIONS = {

    "planner": set(),

    "research_agent": {
        "web_search",
    },

    "contract_analyst": set(),

    "report_agent": set(),
}


def check_tool_permission(
    agent_name: str,
    tool_name: str,
):
    """
    Check whether an agent is authorized to use a tool.
    """

    allowed_tools = AGENT_TOOL_PERMISSIONS.get(
        agent_name,
        set(),
    )

    if tool_name not in allowed_tools:

        raise PermissionError(
            f"Agent '{agent_name}' is not authorized "
            f"to use tool '{tool_name}'."
        )

    return True