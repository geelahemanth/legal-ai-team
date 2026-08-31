from typing import TypedDict, List
from langchain_core.documents import Document

class LegalState(TypedDict):
    """Shared State across all the LangGraph nodes."""


    question: str
    analysis_type: str
    search_query: str
    retrieved_chunks: List[Document]
    legal_references: str
    requires_research: bool
    contract_analysis: str
    final_report: str
