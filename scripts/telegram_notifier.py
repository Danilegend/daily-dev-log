#!/usr/bin/env python3

import os
import sys
import requests


TELEGRAM_API = "https://api.telegram.org"


def get_required_environment(name):
    """Return a required environment variable or stop with a clear error."""
    value = os.getenv(name)

    if not value:
        print(f"❌ Missing required environment variable: {name}")
        sys.exit(1)

    return value


def send_telegram_message(text):
    """Send a text message to the configured Telegram chat."""

    bot_token = get_required_environment("TELEGRAM_BOT_TOKEN")
    chat_id = get_required_environment("TELEGRAM_CHAT_ID")

    url = f"{TELEGRAM_API}/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }

    print("=== TELEGRAM NOTIFIER ===")
    print("Endpoint: Telegram Bot API")
    print("Bot token: [REDACTED]")
    print(f"Chat ID: {chat_id}")
    print()

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as error:
        print(f"❌ Telegram request failed: {error}")
        return False

    print(f"HTTP status: {response.status_code}")

    if response.status_code == 200:
        print("✅ TELEGRAM MESSAGE SENT SUCCESSFULLY!")
        return True

    print("❌ TELEGRAM MESSAGE FAILED")

    try:
        print(response.json())
    except Exception:
        print(response.text)

    return False


if __name__ == "__main__":
    test_message = (
        "🤖 Amharic News Bot — Telegram test\n\n"
        "Telegram notifications are connected successfully! ✅\n\n"
        "This is a controlled test message."
    )

    success = send_telegram_message(test_message)

    if not success:
        sys.exit(1)
