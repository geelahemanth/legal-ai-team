from security.tool_permissions import check_tool_permission


def test_authorized_tool():

    print("\n========== AUTHORIZED TOOL TEST ==========")

    try:

        check_tool_permission(
            agent_name="research_agent",
            tool_name="web_search",
        )

        print(
            "ALLOWED: research_agent → web_search"
        )

    except PermissionError as error:

        print("BLOCKED:", error)


def test_unauthorized_tool():

    print("\n========== UNAUTHORIZED TOOL TEST ==========")

    try:

        check_tool_permission(
            agent_name="contract_analyst",
            tool_name="web_search",
        )

        print(
            "ALLOWED: contract_analyst → web_search"
        )

    except PermissionError as error:

        print("BLOCKED:", error)


if __name__ == "__main__":

    test_authorized_tool()
    test_unauthorized_tool()