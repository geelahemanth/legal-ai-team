from knowledge.vector_store import get_vector_store
from retrieval.bm25_store import load_bm25_retriever
from retrieval.cross_encoder_reranker import rerank_documents

def retrieve_dense_documents(query: str, k: int = 5):
    """Retrieve documents using dense vector similarity."""

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k,
    )

    return results


def retrieve_sparse_documents(query: str, k: int = 5):
    """Retrieve documents using BM25 sparse retrieval."""

    bm25 = load_bm25_retriever()

    results = bm25.invoke(query)

    return results[:k]


def reciprocal_rank_fusion(
    dense_results,
    sparse_results,
    k: int = 5,
    rrf_constant: int = 60,
):
    """Combine dense and sparse results using Reciprocal Rank Fusion."""

    scores = {}
    documents = {}

    # Dense results
    for rank, document in enumerate(dense_results, start=1):

        key = (
            document.page_content,
            tuple(sorted(document.metadata.items())),
        )

        score = 1 / (rrf_constant + rank)

        scores[key] = scores.get(key, 0) + score
        documents[key] = document

    # Sparse results
    for rank, document in enumerate(sparse_results, start=1):

        key = (
            document.page_content,
            tuple(sorted(document.metadata.items())),
        )

        score = 1 / (rrf_constant + rank)

        scores[key] = scores.get(key, 0) + score
        documents[key] = document

    # Sort by RRF score
    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    final_results = []

    for key, score in ranked_results[:k]:

        document = documents[key]

        final_results.append({
            "document": document,
            "score": score,
        })

    return final_results

def retrieve_documents(
    query: str,
    retrieval_k: int = 15,
    final_k: int = 5,
):
    """
    Perform hybrid retrieval followed by CrossEncoder reranking.

    Dense Retrieval
        +
    Sparse/BM25 Retrieval
        ↓
    Reciprocal Rank Fusion
        ↓
    CrossEncoder Reranking
        ↓
    Final Documents
    """

    # ---------------------------------------------------------
    # 1. Dense retrieval
    # ---------------------------------------------------------

    dense_results = retrieve_dense_documents(
        query=query,
        k=retrieval_k,
    )

    # ---------------------------------------------------------
    # 2. Sparse retrieval
    # ---------------------------------------------------------

    sparse_results = retrieve_sparse_documents(
        query=query,
        k=retrieval_k,
    )

    # ---------------------------------------------------------
    # 3. Reciprocal Rank Fusion
    # ---------------------------------------------------------

    rrf_results = reciprocal_rank_fusion(
        dense_results=dense_results,
        sparse_results=sparse_results,
        k=retrieval_k,
    )

    print(f"RRF retrieved {len(rrf_results)} documents.")

    # ---------------------------------------------------------
    # 4. CrossEncoder reranking
    # ---------------------------------------------------------

    reranked_documents = rerank_documents(
        query=query,
        documents=rrf_results,
        top_k=final_k,
    )

    print(
        f"CrossEncoder reranked to "
        f"{len(reranked_documents)} documents."
    )

    # ---------------------------------------------------------
    # 5. Return pure LangChain Documents
    # ---------------------------------------------------------

    return reranked_documents