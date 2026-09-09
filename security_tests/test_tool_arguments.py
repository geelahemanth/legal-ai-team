from security.tool_argument_guard import (
    validate_web_search_arguments
)


def test_valid_arguments():

    print("\n========== VALID ARGUMENT TEST ==========")

    arguments = {
        "query": "California employment termination law"
    }

    try:

        validated = validate_web_search_arguments(
            arguments
        )

        print("ALLOWED:", validated)

    except ValueError as error:

        print("BLOCKED:", error)


def test_manipulated_arguments():

    print("\n========== MANIPULATED ARGUMENT TEST ==========")

    arguments = {
        "query": "California employment termination law",
        "max_results": 10000,
        "admin_mode": True,
    }

    try:

        validated = validate_web_search_arguments(
            arguments
        )

        print("ALLOWED:", validated)

    except ValueError as error:

        print("BLOCKED:", error)


if __name__ == "__main__":

    test_valid_arguments()
    test_manipulated_arguments()