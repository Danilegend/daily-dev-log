#!/usr/bin/env python3

import sys
import requests
import xml.etree.ElementTree as ET


RSS_URL = "https://meseretmedia.substack.com/feed"


def fetch_news(limit=3):
    """Fetch the latest articles from the Meseret Media RSS feed."""

    response = requests.get(
        RSS_URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0 (Amharic-News-Bot/1.0)"
        },
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    channel = root.find("channel")

    if channel is None:
        raise RuntimeError("RSS feed does not contain a channel element")

    articles = []

    for item in channel.findall("item")[:limit]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()

        if not title or not link:
            continue

        articles.append(
            {
                "title": title,
                "link": link,
                "published": pub_date,
            }
        )

    return articles


if __name__ == "__main__":
    print("=== MESERET MEDIA NEWS FETCHER ===")
    print(f"RSS: {RSS_URL}")
    print()

    try:
        articles = fetch_news(limit=3)

        if not articles:
            print("❌ No articles found")
            sys.exit(1)

        print(f"✅ Found {len(articles)} article(s)")
        print()

        for index, article in enumerate(articles, start=1):
            print(f"--- ARTICLE {index} ---")
            print(f"Title: {article['title']}")
            print(f"Published: {article['published']}")
            print(f"Link: {article['link']}")
            print()

    except Exception as error:
        print(f"❌ News fetch failed: {error}")
        sys.exit(1)
