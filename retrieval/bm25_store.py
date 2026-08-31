import os
import pickle

BM25_STORE_PATH = "data/bm25_index.pkl"

def save_bm25_retriever(bm25):
    """Save the BM25 retriever to disk."""

    os.makedirs(
        os.path.dirname(BM25_STORE_PATH),
        exist_ok=True,
    )

    with open(BM25_STORE_PATH, "wb") as file:
        pickle.dump(bm25, file)
    print(f"BM25 index saved to {BM25_STORE_PATH}")


def load_bm25_retriever():
    """Load the BM25 retriever from disk."""

    if not os.path.exists(BM25_STORE_PATH):
        raise FileNotFoundError(
            f"BM25 index not found at {BM25_STORE_PATH}. "
            "Please ingest the contract first."
        )

    with open(BM25_STORE_PATH, "rb") as file:
        bm25 = pickle.load(file)

    return bm25