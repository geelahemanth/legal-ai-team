from langchain_community.tools import DuckDuckGoSearchResults
from security.tool_permissions import check_tool_permission
from security.dangerous_tool_guard import validate_tool_action
from security.tool_argument_guard import (
    validate_web_search_arguments
)

search_tool = DuckDuckGoSearchResults(max_results = 5)

def research_agent(search_query:str):

    # SECURITY CHECK
    check_tool_permission(
        agent_name="research_agent",
        tool_name="web_search",
    )

    validate_tool_action(
    tool_name="web_search",
    action="search",
)
    
        # 3. Build tool arguments ourselves
    arguments = {
        "query": search_query,
    }

    # 4. Validate arguments
    validated_arguments = validate_web_search_arguments(
        arguments
    )
    print(f"Validated arguments: {validated_arguments}")

    print(f"Searching Web:{validated_arguments.query}")
    results = search_tool.invoke(validated_arguments.query)

    print("Response from Google :", results)

    return results
