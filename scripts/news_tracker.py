#!/usr/bin/env python3

import json
import os


TRACKER_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "published_news.json",
)


def load_tracker():
    """Load the published-news tracker."""

    if not os.path.exists(TRACKER_FILE):
        return {"published": []}

    with open(TRACKER_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if "published" not in data:
        data["published"] = []

    return data


def save_tracker(data):
    """Save the published-news tracker."""

    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)

    with open(TRACKER_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def is_published(url):
    """Return True if the article URL has already been published."""

    data = load_tracker()

    return url in data["published"]


def mark_published(url):
    """Record an article URL as published."""

    data = load_tracker()

    if url not in data["published"]:
        data["published"].append(url)
        save_tracker(data)


if __name__ == "__main__":
    print("=== NEWS TRACKER TEST ===")
    print(f"Tracker: {TRACKER_FILE}")
    print()

    test_url = "https://www.meseretmedia.org/p/test"

    print(f"Initially published? {is_published(test_url)}")

    mark_published(test_url)

    print(f"After marking published? {is_published(test_url)}")

    print()
    print("=== TRACKER CONTENT ===")

    data = load_tracker()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Clean up the test entry so this test does not
    # permanently mark a fake article as published.
    data["published"].remove(test_url)
    save_tracker(data)

    print()
    print("✅ Tracker test completed")
    print("✅ Test entry removed")
