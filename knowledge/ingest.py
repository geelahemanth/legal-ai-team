import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge.vector_store import get_vector_store
from retrieval.bm25_retriever import create_bm25_retriever
from retrieval.bm25_store import save_bm25_retriever
from security.document_registry import (
    check_document_version,
    register_trusted_document,
)

ALLOWED_FILE_EXTENSIONS = {".pdf"}


def validate_document_source(pdf_path: str):
    """
    Basic source validation.

    For our learning project:
    - file must exist
    - only PDF files are allowed
    """

    if not os.path.exists(pdf_path):
        return False, "Document does not exist."

    extension = os.path.splitext(pdf_path)[1].lower()

    if extension not in ALLOWED_FILE_EXTENSIONS:
        return False, f"Unsupported file type: {extension}"

    return True, "Valid document source."


def calculate_file_hash(file_path: str):
    """
    Generate SHA-256 fingerprint for the document.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def ingest_pdf(
    pdf_path: str,
    document_id: str,
    owner_id: str,
    version: int = 1,
):
    """
    Load a PDF, validate it, calculate its hash,
    attach provenance metadata, split into chunks,
    and index it in BM25 + Chroma.
    """

    # =========================================================
    # 1. SOURCE VALIDATION
    # =========================================================

    is_valid, reason = validate_document_source(pdf_path)

    if not is_valid:
        raise ValueError(reason)

    print("Document source validation: PASSED")

    # =========================================================
    # 2. DOCUMENT HASH
    # =========================================================

    document_hash = calculate_file_hash(pdf_path)

    print("Document SHA-256:")
    print(document_hash)

    # =========================================================
# DOCUMENT INTEGRITY / VERSION CHECK
# =========================================================

    version_check = check_document_version(
        document_id=document_id,
        document_hash=document_hash,
    )

    status = version_check["status"]
    version = version_check["version"]

    print("\n========== DOCUMENT VERSION CHECK ==========")
    print(f"Status  : {status}")
    print(f"Version : {version}")

    if status == "SAME":

        print("\nDocument already exists with the same hash.")
        print("No re-indexing required.")

        return


    if status == "CHANGED":

        print("\n⚠ DOCUMENT CHANGE DETECTED")
        print("Previous hash:", version_check["previous_hash"])
        print("New hash:", document_hash)
        print(f"Proposed new version: {version}")

        approval = input(
            f"\nApprove document version {version}? [y/N]: "
        ).strip().lower()

        if approval != "y":
            print("\nDocument update REJECTED.")
            print("Existing trusted version remains unchanged.")
            return

        print(f"\nDocument version {version} APPROVED.")
        print("Continuing with ingestion...")


    # =========================================================
    # 3. LOAD PDF
    # =========================================================

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("======================================")
    print(f"Loaded {len(documents)} pages.")

    # =========================================================
    # 4. PROVENANCE + ACCESS CONTROL METADATA
    # =========================================================

    file_name = os.path.basename(pdf_path)

    for document in documents:

        document.metadata.update(
            {
                "document_id": document_id,
                "document_hash": document_hash,
                "version": version,
                "owner_id": owner_id,
                "source_file": file_name,
                "trusted_source": True,
            }
        )

    # =========================================================
    # 5. SPLIT INTO CHUNKS
    # =========================================================

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    print(
        f"Splitting {len(documents)} documents into chunks..."
    )

    chunks = splitter.split_documents(documents)

    # Metadata is automatically copied from page Document
    # into the resulting chunks.

    # =========================================================
    # 6. BM25 INDEX
    # =========================================================

    bm25 = create_bm25_retriever(chunks)

    save_bm25_retriever(bm25)

    print(
        "Number of chunks indexed in BM25:",
        len(bm25.docs),
    )

    # =========================================================
    # 7. CHROMA INDEX
    # =========================================================

    vector_store = get_vector_store()

    # Current learning architecture:
    # keep one active contract
    vector_store.reset_collection()

    vector_store.add_documents(chunks)

    register_trusted_document(
    document_id=document_id,
    document_hash=document_hash,
    version=version,
    owner_id=owner_id,
    )

    print(
        f"Successfully ingested {len(chunks)} chunks "
        f"from {pdf_path}."
    )

    print("\nDocument Security Metadata:")
    print(f"Document ID : {document_id}")
    print(f"Owner ID    : {owner_id}")
    print(f"Version     : {version}")
    print(f"SHA-256     : {document_hash}")





if __name__ == "__main__":
    ingest_pdf(
        pdf_path="data/contracts/sample_contract.pdf",
        document_id="contract_001",
        owner_id="user_001",
    )