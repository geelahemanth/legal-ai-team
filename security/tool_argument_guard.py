from pydantic import ValidationError

from models.web_search_args import WebSearchArguments


def validate_web_search_arguments(arguments: dict):
    """
    Validate arguments before executing the web search tool.
    """

    try:

        validated = WebSearchArguments.model_validate(
            arguments
        )

        return validated

    except ValidationError as error:

        raise ValueError(
            f"Invalid web search arguments: {error}"
        )