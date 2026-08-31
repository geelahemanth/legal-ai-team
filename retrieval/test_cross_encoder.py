from knowledge.retriever import retrieve_documents


def main():

    query = "What is the termination notice period?"

    print("\n" + "=" * 80)
    print("FINAL RETRIEVAL TEST")
    print("=" * 80)

    results = retrieve_documents(
        query=query,
        retrieval_k=15,
        final_k=5,
    )

    print(f"\nFinal results: {len(results)}")

    for rank, item in enumerate(results, start=1):

        print("\n" + "-" * 80)
        print(f"Rank {rank}")

        # If result is a dictionary
        if isinstance(item, dict):

            document = item["document"]

            print(
                "CrossEncoder Score:",
                item.get("cross_encoder_score"),
            )

            print(
                "RRF Score:",
                item.get("rrf_score"),
            )

        # If result is a LangChain Document
        else:

            document = item

        print(
            "Page:",
            document.metadata.get("page_label")
        )

        print("Content:")
        print(document.page_content[:1000])


if __name__ == "__main__":
    main()