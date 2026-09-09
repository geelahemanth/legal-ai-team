from graph.workflow import build_graph

from guardrails.input_guard import validate_user_input
from security.semantic_input_detector import detect_semantic_attack


def main():
    print("=" * 80)
    print("LEGAL AI ASSISTANT")
    print("=" * 80)

    question = input("\nEnter your legal question: ").strip()

    # =========================================================
    # LAYER 1 — BASIC / RULE-BASED INPUT SECURITY
    # =========================================================

    is_valid, reason = validate_user_input(question)

    if not is_valid:
        print("\n" + "=" * 80)
        print("INPUT BLOCKED")
        print("=" * 80)
        print(f"\nReason: {reason}")
        return

    # =========================================================
    # LAYER 2 — SEMANTIC SECURITY DETECTION
    # =========================================================

    security_result = detect_semantic_attack(question)

    if security_result["is_attack"]:
        print("\n" + "=" * 80)
        print("SECURITY BLOCKED")
        print("=" * 80)

        print(f"\nAttack Type: {security_result['attack_type']}")
        print(f"Reason: {security_result['reason']}")
        return

    # =========================================================
    # SAFE INPUT → START AGENT WORKFLOW
    # =========================================================

    graph = build_graph()

    print("\nProcessing your question...\n")

    initial_state = {
        "question": question,
        "owner_id": "user_999",
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