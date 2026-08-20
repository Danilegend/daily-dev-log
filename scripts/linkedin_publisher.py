#!/usr/bin/env python3

import os
import sys
import requests


LINKEDIN_API_URL = "https://api.linkedin.com/rest/posts"
LINKEDIN_VERSION = "202608"


def get_required_environment(name):
    """Return a required environment variable or stop with a clear error."""
    value = os.getenv(name)

    if not value:
        print(f"❌ Missing required environment variable: {name}")
        sys.exit(1)

    return value


def publish_to_linkedin(text):
    """Publish a text-only post to the authenticated LinkedIn member."""

    access_token = get_required_environment("LINKEDIN_ACCESS_TOKEN")
    person_id = get_required_environment("LINKEDIN_PERSON_ID")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": LINKEDIN_VERSION,
    }

    data = {
        "author": f"urn:li:person:{person_id}",
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED"
        },
        "lifecycleState": "PUBLISHED",
    }

    print("=== LINKEDIN PUBLISHER ===")
    print(f"Endpoint: {LINKEDIN_API_URL}")
    print(f"LinkedIn version: {LINKEDIN_VERSION}")
    print(f"Person ID: {person_id}")
    print("Access token: [REDACTED]")
    print()

    response = requests.post(
        LINKEDIN_API_URL,
        headers=headers,
        json=data,
        timeout=30,
    )

    print(f"HTTP status: {response.status_code}")

    if response.status_code == 201:
        post_id = response.headers.get("x-restli-id")

        print("✅ POST PUBLISHED SUCCESSFULLY!")

        if post_id:
            print(f"LinkedIn post ID: {post_id}")

        return {
            "success": True,
            "post_id": post_id,
            "status_code": response.status_code,
        }

    print("❌ LINKEDIN POST FAILED")

    try:
        error = response.json()
        print(error)
    except Exception:
        print(response.text)

    return {
        "success": False,
        "post_id": None,
        "status_code": response.status_code,
    }


if __name__ == "__main__":
    test_message = (
        "🚀 Amharic News Bot — publisher test\n\n"
        "This is a controlled test from the production publisher module.\n\n"
        "#AmharicNews #Ethiopia #Automation"
    )

    result = publish_to_linkedin(test_message)

    if not result["success"]:
        sys.exit(1)
