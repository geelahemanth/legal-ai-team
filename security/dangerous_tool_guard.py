# security/dangerous_tool_guard.py


TOOL_ACTION_POLICIES = {

    "web_search": {
        "allowed_actions": {
            "search",
        }
    },

    "document_tool": {
        "allowed_actions": {
            "read",
        }
    },

}


def validate_tool_action(
    tool_name: str,
    action: str,
):
    """
    Validate whether an action is allowed for a tool.
    """

    policy = TOOL_ACTION_POLICIES.get(tool_name)

    # Unknown tool
    if policy is None:
        raise PermissionError(
            f"No security policy exists for tool '{tool_name}'."
        )

    allowed_actions = policy["allowed_actions"]

    # Dangerous / unsupported operation
    if action not in allowed_actions:
        raise PermissionError(
            f"Action '{action}' is not allowed "
            f"for tool '{tool_name}'."
        )

    return True