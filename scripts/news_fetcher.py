#!/usr/bin/env python3

import sys
import time
import requests
import xml.etree.ElementTree as ET


RSS_URL = "https://meseretmedia.substack.com/feed"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "application/rss+xml, "
        "application/xml;q=0.9, "
        "text/xml;q=0.8, "
        "*/*;q=0.7"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
}


def fetch_news(limit=3):
    """Fetch the latest articles from the Meseret Media RSS feed."""

    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)

    last_error = None

    for attempt in range(1, 4):
        try:
            print(
                f"Fetching RSS feed "
                f"(attempt {attempt}/3)..."
            )

            response = session.get(
                RSS_URL,
                timeout=30,
                allow_redirects=True,
            )

            print(f"RSS HTTP status: {response.status_code}")

            response.raise_for_status()

            root = ET.fromstring(response.content)

            channel = root.find("channel")

            if channel is None:
                raise RuntimeError(
                    "RSS feed does not contain a channel element"
                )

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

        except requests.RequestException as error:
            last_error = error

            print(
                f"⚠️ RSS request failed on attempt "
                f"{attempt}/3: {error}"
            )

            if attempt < 3:
                time.sleep(2)

        except ET.ParseError as error:
            raise RuntimeError(
                f"RSS XML parsing failed: {error}"
            ) from error

    raise RuntimeError(
        f"Unable to fetch RSS feed after 3 attempts: {last_error}"
    )


if __name__ == "__main__":
    print("=== MESERET MEDIA NEWS FETCHER ===")
    print(f"RSS: {RSS_URL}")
    print()

    try:
        articles = fetch_news(limit=3)

        if not articles:
            print("❌ No articles found")
            sys.exit(1)

        print()
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
