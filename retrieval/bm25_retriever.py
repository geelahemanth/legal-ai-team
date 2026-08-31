from langchain_community.retrievers import BM25Retriever
from retrieval.bm25_store import load_bm25_retriever
from knowledge.vector_store import get_vector_store



def create_bm25_retriever(documents):
    """Create a BM25 retriever from a list of documents."""
    
    retriever = BM25Retriever.from_documents(documents)
    retriever.k = 5

    return retriever

