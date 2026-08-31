from langchain_community.tools import DuckDuckGoSearchResults

search_tool = DuckDuckGoSearchResults(max_results = 5)

def research_agent(search_query:str):

    print(f"Searching Web:{search_query}")
    results = search_tool.invoke(search_query)

    print("Response from Google :", results)

    return results