from security.dangerous_tool_guard import validate_tool_action


def test_safe_action():

    print("\n========== SAFE ACTION TEST ==========")

    try:
        validate_tool_action(
            tool_name="document_tool",
            action="read",
        )

        print("ALLOWED: document_tool → read")

    except PermissionError as error:
        print("BLOCKED:", error)


def test_dangerous_action():

    print("\n========== DANGEROUS ACTION TEST ==========")

    try:
        validate_tool_action(
            tool_name="document_tool",
            action="delete",
        )

        print("ALLOWED: document_tool → delete")

    except PermissionError as error:
        print("BLOCKED:", error)


if __name__ == "__main__":

    test_safe_action()
    test_dangerous_action()