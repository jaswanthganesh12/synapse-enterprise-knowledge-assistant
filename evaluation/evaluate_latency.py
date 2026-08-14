import argparse
import json
import statistics
import time

import requests

from app.db.session import SessionLocal
from app.services.hybrid_search_service import hybrid_search


def evaluate_retrieval(dataset, user_id):
    db = SessionLocal()
    latencies = []

    try:
        for item in dataset:
            start = time.perf_counter()

            hybrid_search(
                db=db,
                query=item["question"],
                user_id=user_id,
                limit=5,
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            latencies.append(elapsed)

            print(
                f"Retrieval: {elapsed:.2f} ms | "
                f"{item['question']}"
            )

    finally:
        db.close()

    return latencies


def evaluate_chat(
    dataset,
    base_url,
    token,
    conversation_id,
):
    latencies = []

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    for item in dataset:
        payload = {
            "query": item["question"],
            "conversation_id": conversation_id,
        }

        start = time.perf_counter()

        response = requests.post(
            f"{base_url}/chat/",
            headers=headers,
            json=payload,
            timeout=60,
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        response.raise_for_status()

        latencies.append(elapsed)

        print(
            f"Chat: {elapsed:.2f} ms | "
            f"{item['question']}"
        )

    return latencies


def summarize(name, latencies):
    print()
    print(f"===== {name} =====")

    print(
        f"Average: "
        f"{statistics.mean(latencies):.2f} ms"
    )

    print(
        f"Median:  "
        f"{statistics.median(latencies):.2f} ms"
    )

    print(
        f"Min:     "
        f"{min(latencies):.2f} ms"
    )

    print(
        f"Max:     "
        f"{max(latencies):.2f} ms"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--user-id",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--token",
        required=True,
    )

    parser.add_argument(
        "--conversation-id",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
    )

    args = parser.parse_args()

    with open(
        "evaluation/dataset.json",
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    print("Starting retrieval evaluation...")
    retrieval_latencies = evaluate_retrieval(
        dataset,
        args.user_id,
    )

    summarize(
        "Retrieval Latency",
        retrieval_latencies,
    )

    print()
    print("Starting end-to-end chat evaluation...")

    chat_latencies = evaluate_chat(
        dataset,
        args.base_url,
        args.token,
        args.conversation_id,
    )

    summarize(
        "End-to-End Chat Latency",
        chat_latencies,
    )


if __name__ == "__main__":
    main()