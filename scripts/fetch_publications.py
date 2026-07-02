#!/usr/bin/env python3
"""Fetch publications from Google Scholar and write data/publications.json.

Uses the `scholarly` library routed through free public proxies so it works from
GitHub Actions runners, whose datacenter IPs Google Scholar otherwise blocks.

Retries with fresh proxies a few times. If every attempt fails (or no
publications come back), it exits non-zero WITHOUT writing, so a blocked run
never clobbers the existing publications list.
"""

import json
import os
import sys
import time

from scholarly import ProxyGenerator, scholarly

SCHOLAR_ID = "sLSmk9AAAAAJ"
MAX_ATTEMPTS = 4
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "publications.json",
)


def to_year(value):
    try:
        return int(str(value)[:4])
    except (TypeError, ValueError):
        return None


def normalize(pub):
    bib = pub.get("bib", {}) or {}
    year = to_year(bib.get("pub_year"))
    authors = bib.get("author") or "T Mahajan"
    author_list = [a.strip() for a in authors.replace(" and ", ",").split(",") if a.strip()]
    pub_id = pub.get("author_pub_id", "")
    link = (
        f"https://scholar.google.com/citations?view_op=view_citation"
        f"&hl=en&user={SCHOLAR_ID}&citation_for_view={pub_id}"
        if pub_id
        else pub.get("pub_url", "")
    )
    return {
        "title": (bib.get("title") or "").strip(),
        "date": [year] if year else [],
        "link": link,
        "authors": author_list,
        "journal": (bib.get("venue") or "").strip(),
        "citations": int(pub.get("num_citations") or 0),
    }


def fetch_publications():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS}: setting up free proxy...")
        try:
            pg = ProxyGenerator()
            if not pg.FreeProxies():
                raise RuntimeError("no free proxy available")
            scholarly.use_proxy(pg)

            author = scholarly.search_author_id(SCHOLAR_ID)
            author = scholarly.fill(author, sections=["publications"])
            pubs = author.get("publications", [])
            if pubs:
                print(f"Fetched {len(pubs)} publications.")
                return pubs
            print("No publications returned; retrying.")
        except Exception as exc:  # noqa: BLE001 - proxies fail in many ways
            print(f"Attempt {attempt} failed: {exc}")
        time.sleep(5)
    return []


def main():
    pubs = fetch_publications()
    if not pubs:
        sys.exit("Could not fetch publications after retries; leaving file unchanged")

    publications = [normalize(p) for p in pubs]
    publications = [p for p in publications if p["title"]]
    publications.sort(key=lambda p: (p["date"][0] if p["date"] else 0), reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(publications)} publications to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
