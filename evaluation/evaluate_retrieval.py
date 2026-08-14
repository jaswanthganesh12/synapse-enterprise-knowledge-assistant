import argparse
import json

from app.db.session import SessionLocal
from app.services.hybrid_search_service import hybrid_search


def calculate_recall_at_k(results, expected_document_id, k):
    top_k = results[:k]

    return int(
        any(
            result["document_id"] == expected_document_id
            for result in top_k
        )
    )


def calculate_mrr(results, expected_document_id):
    for rank, result in enumerate(results, start=1):
        if result["document_id"] == expected_document_id:
            return 1 / rank

    return 0.0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--user-id",
        type=int,
        required=True,
    )

    args = parser.parse_args()

    with open(
        "evaluation/dataset.json",
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    db = SessionLocal()

    try:
        recall_scores = []
        mrr_scores = []

        for item in dataset:
            question = item["question"]
            expected_document_id = item[
                "expected_document_id"
            ]

            results = hybrid_search(
                db=db,
                query=question,
                user_id=args.user_id,
                limit=5,
            )

            recall = calculate_recall_at_k(
                results,
                expected_document_id,
                5,
            )

            mrr = calculate_mrr(
                results,
                expected_document_id,
            )

            recall_scores.append(recall)
            mrr_scores.append(mrr)

            print()
            print(f"Question: {question}")
            print(
                f"Expected document: "
                f"{expected_document_id}"
            )
            print(
                "Retrieved documents:",
                [
                    result["document_id"]
                    for result in results
                ],
            )
            print(f"Recall@5: {recall}")
            print(f"MRR: {mrr:.3f}")

        print("\n===== Evaluation Summary =====")

        print(
            f"Recall@5: "
            f"{sum(recall_scores) / len(recall_scores):.3f}"
        )

        print(
            f"MRR: "
            f"{sum(mrr_scores) / len(mrr_scores):.3f}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()