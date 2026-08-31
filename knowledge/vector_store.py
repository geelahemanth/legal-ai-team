from langchain_chroma import Chroma
from config.openai_client import embeddings

def get_vector_store():

    vector_store = Chroma(
        collection_name="legal_documents",
        embedding_function=embeddings,
        persist_directory="data/chroma_db",
    )
    return vector_store