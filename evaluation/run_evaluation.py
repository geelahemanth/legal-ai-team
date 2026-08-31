import json
import os
from pathlib import Path

from graph.workflow import build_graph


DATASET_PATH = Path("evaluation/dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_contexts(retrieved_chunks):
    """
    Convert the application's retrieved_chunks into
    plain text contexts for RAGAS.
    """

    contexts = []

    for item in retrieved_chunks:

        # Current retrieval pipeline returns:
        # {
        #     "document": Document(...),
        #     "score": ...
        # }

        if isinstance(item, dict):
            document = item["document"]
        else:
            document = item

        contexts.append(document.page_content)

    return contexts


def run_rag(question: str, graph):
    """
    Run the existing Legal AI LangGraph and capture
    the exact contexts and final answer.
    """

    print("\n" + "=" * 80)
    print(f"QUESTION: {question}")
    print("=" * 80)

    initial_state = {
        "question": question,
    }

    result = graph.invoke(initial_state)

    retrieved_chunks = result.get("retrieved_chunks", [])

    contexts = extract_contexts(retrieved_chunks)

    final_answer = result.get("final_report", "")

    print("\nRetrieved contexts:", len(contexts))

    print("\nFinal answer:")
    print(final_answer)

    return {
        "question": question,
        "contexts": contexts,
        "answer": final_answer,
    }


def build_ragas_dataset(dataset):

    graph = build_graph()

    evaluation_rows = []

    for item in dataset:

        question = item["user_input"]
        ground_truth = item["reference"]

        rag_result = run_rag(
            question=question,
            graph=graph,
        )

        evaluation_rows.append(
            {
                "user_input": question,
                "retrieved_contexts": rag_result["contexts"],
                "response": rag_result["answer"],
                "reference": ground_truth,
            }
        )

    return evaluation_rows


def save_rag_results(rows):
    """
    Save the raw RAG outputs before RAGAS evaluation.

    This is extremely useful for debugging retrieval failures.
    """

    output_path = Path("evaluation/rag_results.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            rows,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nRaw RAG results saved to: {output_path}"
    )


def main():

    print("=" * 80)
    print("RAGAS EVALUATION")
    print("=" * 80)

    dataset = load_dataset()

    print(
        f"\nLoaded {len(dataset)} evaluation questions."
    )

    rows = build_ragas_dataset(dataset)

    save_rag_results(rows)

    print("\n" + "=" * 80)
    print("RAG DATA COLLECTION COMPLETE")
    print("=" * 80)

    for index, row in enumerate(rows, start=1):

        print(f"\nEvaluation {index}")

        print(
            f"Question: {row['user_input']}"
        )

        print(
            f"Contexts: {len(row['retrieved_contexts'])}"
        )

        print(
            f"Answer length: {len(row['response'])}"
        )

        print(
            f"Ground truth: {row['reference']}"
        )


if __name__ == "__main__":
    main()