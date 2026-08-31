from datetime import datetime
from knowledge.retriever import retrieve_documents
from agents.planner import planner_agent
from agents.research_agent import research_agent
from agents.contract_analyst import contract_analyst_agent
from agents.report_generator import report_generator_agent
import time
from guardrails.research_guard import validate_search_query
from guardrails.contract_guard import validate_contract_analysis
from guardrails.output_guard import validate_final_report


def planner_node(state):
    print("\n======== Planner Agent ========")

    result = planner_agent(state["question"])
    print(result)

    return {
        "analysis_type": result["analysis_type"],
        "search_query": result["search_query"],
        "requires_research": result["requires_research"]
    }



def retriever_node(state):
    """Retrieve and rerank relevant document chunks."""

    print("\n======== Retriever Agent ========")

    search_query = state["search_query"]

    results = retrieve_documents(
        query=search_query,
        retrieval_k=15,
        final_k=5,
    )

    print(f"Final retrieved documents: {len(results)}")

    for rank, document in enumerate(results, start=1):

        print(f"\n--- Rank {rank} ---")
        print(f"Page: {document.metadata.get('page_label')}")
        print(f"Content: {document.page_content[:500]}")

    return {
        "retrieved_chunks": results
    }


def research_node(state):
    """ Research the web for relevant information."""
    print("\n======== Research Agent ========")
    search_query = state["search_query"]
    # validate the search query using guardrails
    is_valid, error = validate_search_query(search_query)
    if not is_valid:
        print(f"Research Guard: {error}")
        return {
            "legal_references": ""
        }
    references = research_agent(state["search_query"])

    return {
        "legal_references": references
    }

def contract_analyst_node(state):

    print("\n========== Contract Agent ==========")

    print("\nRetrieved chunks passed to Contract Analyst:")
    print("=" * 80)

    for rank, doc in enumerate(
        state["retrieved_chunks"],
        start=1
    ):
        print(f"\nContext Rank: {rank}")
        print(f"Page: {doc.metadata.get('page_label')}")
        print(doc.page_content[:1000])

    contract_context = "\n\n".join(
        doc.page_content
        for doc in state["retrieved_chunks"]
    )

    print("\n" + "=" * 80)
    print("Sending retrieved context to Contract Analyst...")
    print("=" * 80)

    analysis = contract_analyst_agent(
        question=state["question"],
        analysis_type=state["analysis_type"],
        contract_context=contract_context,
        legal_references=state.get(
            "legal_references",
            "No external legal references were required."
        ),
    )

    is_valid, error_message = validate_contract_analysis(analysis)

    if not is_valid:
        print(f"Contract Guard: {error_message}")

        analysis = (
            "Unable to generate a reliable contract analysis. "
            "Please refine your question or provide more contract context."
        )

    return {
        "contract_analysis": analysis
    }



def report_node(state):
    """ Generate a simple report."""
    print("\n========== Report Agent ==========")
    final_report = ""

    for chunk in report_generator_agent(
        question = state["question"],
        analysis_type = state["analysis_type"],
        analysis = state["contract_analysis"],
    ):
        
        print(chunk, end ="", flush=True)
        final_report += chunk

    is_valid, error_message = validate_final_report(final_report)
    if not is_valid:
        print(f"Report Guard: {error_message}")
        final_report = (
            "Unable to generate a reliable report. "
            "Please refine your question or provide more contract context."
        )

    return {
        "final_report": final_report
    }