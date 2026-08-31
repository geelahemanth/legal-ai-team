from tracemalloc import start
from graph.workflow import build_graph
import time
from guardrails.input_guard import validate_user_input
from knowledge.ingest import ingest_pdf



def main():
    print("=" * 80)
    print("LEGAL AI ASSISTANT")
    print("=" * 80)

    question = input("\nEnter your legal question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    # Build the LangGraph workflow
    graph = build_graph()

    print("\nProcessing your question...\n")

    initial_state = {
        "question": question,
    }

    try:
        result = graph.invoke(initial_state)

        print("\n" + "=" * 80)
        print("FINAL LEGAL RESPONSE")
        print("=" * 80)

        final_report = result.get("final_report")

        if final_report:
            print("\n" + final_report)
        else:
            print("\nNo final report was generated.")

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)

        print(f"\n{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()

