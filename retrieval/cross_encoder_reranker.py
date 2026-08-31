from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


print("Loading CrossEncoder model...", flush=True)

model = CrossEncoder(
    MODEL_NAME,
    max_length=512,
)

print("CrossEncoder model loaded.", flush=True)


def rerank_documents(
    query: str,
    documents: list,
    top_k: int = 5,
):
    """
    Rerank RRF documents using a CrossEncoder.

    Args:
        query: User/search query.
        documents: RRF results containing Document objects.
        top_k: Number of final documents to return.

    Returns:
        List of LangChain Document objects ordered by
        CrossEncoder relevance.
    """

    if not documents:
        return []

    # ---------------------------------------------
    # Extract Documents from RRF results
    # ---------------------------------------------

    clean_documents = []

    for item in documents:

        if isinstance(item, dict):
            document = item["document"]
        else:
            document = item

        clean_documents.append(document)

    # ---------------------------------------------
    # Create query-document pairs
    # ---------------------------------------------

    pairs = [
        (query, document.page_content)
        for document in clean_documents
    ]

    # ---------------------------------------------
    # CrossEncoder scoring
    # ---------------------------------------------

    scores = model.predict(pairs)

    # ---------------------------------------------
    # Combine documents + scores
    # ---------------------------------------------

    scored_documents = list(
        zip(clean_documents, scores)
    )

    # Highest score first
    scored_documents.sort(
        key=lambda item: float(item[1]),
        reverse=True,
    )

    # ---------------------------------------------
    # Return only Documents
    # ---------------------------------------------

    reranked_documents = [
        document
        for document, score in scored_documents[:top_k]
    ]

    return reranked_documents