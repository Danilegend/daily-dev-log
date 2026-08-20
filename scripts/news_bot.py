#!/usr/bin/env python3

import os
import sys

from news_fetcher import fetch_news
from news_formatter import format_news
from news_tracker import is_published, mark_published
from linkedin_publisher import publish_to_linkedin
from telegram_notifier import send_telegram_message


def get_new_articles(articles):
    """Return articles that have not been published yet."""

    return [
        article
        for article in articles
        if not is_published(article["link"])
    ]


def main():
    print("=== AMHARIC NEWS BOT ===")
    print()

    publish_enabled = os.getenv(
        "NEWS_BOT_PUBLISH",
        "false"
    ).lower() == "true"

    print(f"Publishing enabled: {publish_enabled}")
    print()

    try:
        articles = fetch_news(limit=3)

        if not articles:
            print("❌ No articles found")
            return 1

        print(f"Fetched articles: {len(articles)}")

        new_articles = get_new_articles(articles)

        print(f"New articles: {len(new_articles)}")
        print()

        if not new_articles:
            print("ℹ️ All fetched articles have already been published.")
            print("Nothing to do.")
            return 0

        print("=== NEW ARTICLES ===")

        for index, article in enumerate(new_articles, start=1):
            print(f"{index}. {article['title']}")
            print(f"   {article['link']}")

        print()

        post = format_news(new_articles)

        print("=== GENERATED LINKEDIN POST ===")
        print()
        print(post)
        print()

        if not publish_enabled:
            print("=== DRY RUN ===")
            print("⚠️ LinkedIn publishing is disabled.")
            print("Nothing was published.")
            return 0

        print("=== LINKEDIN PUBLISH ===")

        result = publish_to_linkedin(post)

        if not result["success"]:
            print("❌ LinkedIn publishing failed.")
            print("⚠️ Article was NOT marked as published.")
            return 1

        print()
        print("=== MARKING ARTICLES AS PUBLISHED ===")

        for article in new_articles:
            mark_published(article["link"])
            print(f"✅ {article['link']}")

        print()
        print("=== TELEGRAM NOTIFICATION ===")

        telegram_message = (
            "📰 Amharic News Bot\\n\\n"
            "✅ LinkedIn publication successful\\n\\n"
            f"{len(new_articles)} new article(s) published.\\n\\n"
        )

        for index, article in enumerate(new_articles, start=1):
            telegram_message += (
                f"{index}️⃣ {article['title']}\\n"
                f"🔗 {article['link']}\\n\\n"
            )

        telegram_message += (
            "📌 ምንጭ: መሠረት ሚድያ\\n\\n"
            "#ኢትዮጵያ #ዜና #AmharicNews #Ethiopia"
        )

        telegram_success = send_telegram_message(telegram_message)

        if telegram_success:
            print("✅ Telegram notification sent.")
        else:
            print("⚠️ Telegram notification failed.")
            print("ℹ️ LinkedIn publication was successful.")

        print()
        print("🎉 NEWS BOT COMPLETED SUCCESSFULLY")

        return 0

    except Exception as error:
        print(f"❌ News bot failed: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
