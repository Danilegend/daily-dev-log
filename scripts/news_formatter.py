#!/usr/bin/env python3

from news_fetcher import fetch_news


def format_news(articles):
    """Format fetched Amharic news into a LinkedIn-ready post."""

    lines = [
        "📰 የዛሬ ዋና ዋና ዜናዎች",
        "",
    ]

    emojis = ["1️⃣", "2️⃣", "3️⃣"]

    for index, article in enumerate(articles):
        emoji = emojis[index] if index < len(emojis) else "▪️"

        lines.append(f"{emoji} {article['title']}")
        lines.append(f"🔗 {article['link']}")
        lines.append("")

    lines.extend([
        "📌 ምንጭ: መሠረት ሚድያ",
        "",
        "#ኢትዮጵያ #ዜና #AmharicNews #Ethiopia",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    print("=== AMHARIC NEWS FORMATTER ===")
    print()

    articles = fetch_news(limit=3)

    if not articles:
        raise SystemExit("❌ No articles available")

    post = format_news(articles)

    print(post)

    print()
    print("=== FORMATTER CHECK ===")
    print(f"Articles included: {len(articles)}")
    print(f"Characters: {len(post)}")
    print("✅ Formatter completed")
