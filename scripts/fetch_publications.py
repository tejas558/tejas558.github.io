#!/usr/bin/env python3
"""Fetch publications from Google Scholar via SerpAPI and write data/publications.json.

Requires the SERPAPI_KEY environment variable. Exits non-zero without writing if
the API call fails or returns no articles, so a bad response never clobbers the
existing publications list.
"""

import json
import os
import sys
import urllib.parse
import urllib.request

SCHOLAR_ID = "sLSmk9AAAAAJ"
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "publications.json",
)


def fetch_articles(api_key):
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "num": 100,
        "sort": "pubdate",
        "hl": "en",
        "api_key": api_key,
    }
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.load(resp)

    if payload.get("error"):
        raise RuntimeError(f"SerpAPI error: {payload['error']}")

    return payload.get("articles", [])


def to_year(value):
    try:
        return int(str(value)[:4])
    except (TypeError, ValueError):
        return None


def normalize(article):
    authors = article.get("authors", "")
    author_list = [a.strip() for a in authors.split(",") if a.strip()] if authors else []
    year = to_year(article.get("year"))
    cited_by = article.get("cited_by", {}) or {}
    return {
        "title": article.get("title", "").strip(),
        "date": [year] if year else [],
        "link": article.get("link", ""),
        "authors": author_list,
        "journal": (article.get("publication") or "").strip(),
        "citations": int(cited_by.get("value") or 0),
    }


def main():
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        sys.exit("SERPAPI_KEY environment variable is not set")

    articles = fetch_articles(api_key)
    if not articles:
        sys.exit("No articles returned from SerpAPI; leaving existing file unchanged")

    publications = [normalize(a) for a in articles if a.get("title")]
    publications.sort(key=lambda p: (p["date"][0] if p["date"] else 0), reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(publications)} publications to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
