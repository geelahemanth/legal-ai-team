MIN_QUERY_LENGTH = 10

def validate_search_query(search_query: str):
    """ Validate the search query before making an internet search."""

    # -------- Rule 1 ------------
    if not search_query:
        return False, "Search query is empty."
    
    search_query = search_query.strip()

    # -------- Rule 2 ------------
    if len(search_query) < MIN_QUERY_LENGTH:
        return False, "search query is too short."

    # -------- Rule 3 ------------
    if not any(char.isalnum() for char in search_query):
        return False, "search query must contain at least one alphanumeric character."
    return True, "Valid search query."