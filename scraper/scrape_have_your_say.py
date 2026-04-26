"""Scraper for EU "Have Your Say" public consultations.

Plan A: hit the portal and parse open consultations into the schema below.
Plan B: if the portal fights you within ~15 minutes, hand-curate ~10 real
        open consultations into data/consultations.json directly, following
        the schema in data/sample_consultations.json.

Either way, this script writes data/consultations.json. If scraping yields
nothing, the file is left as `[]` and classify_and_score.py will fall back
to data/sample_consultations.json.

Schema for each consultation entry (must stay in sync with pipeline/):
    {
        "id":       str,   # any stable unique identifier
        "title":    str,
        "summary":  str,   # 1-3 sentence plain-language summary
        "deadline": str,   # ISO date "YYYY-MM-DD" or "unknown"
        "source":   str,   # e.g. "EU Have Your Say"
        "link":     str,   # full URL back to the consultation
    }
"""
from __future__ import annotations

import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT = DATA_DIR / "consultations.json"

# TODO(person-a): find the actual listing URL or underlying JSON endpoint.
# The portal renders a lot client-side; check Network tab in devtools for an
# XHR/JSON endpoint that returns the open-consultations list — that's much
# easier to parse than the rendered HTML.
HAVE_YOUR_SAY_URL = "https://have-your-say.ec.europa.eu/"


def scrape() -> list[dict]:
    print(f"GET {HAVE_YOUR_SAY_URL}")
    resp = requests.get(
        HAVE_YOUR_SAY_URL,
        timeout=15,
        headers={"User-Agent": "ImpactFeed/0.1 (hackathon prototype)"},
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # TODO(person-a): replace the placeholder below with real selectors once
    # you've inspected the page. Each consultation must produce a dict that
    # matches the schema in this file's docstring.
    consultations: list[dict] = []
    _ = soup  # silence "unused" warning until selectors are written

    print(f"Parsed {len(consultations)} consultations from {len(resp.text)} bytes.")
    return consultations


def main() -> None:
    try:
        consultations = scrape()
    except Exception as e:
        print(f"Scrape failed: {e}")
        consultations = []

    if not consultations:
        print(
            "No consultations scraped. classify_and_score.py will fall back to "
            "data/sample_consultations.json. To proceed with real data, hand-curate "
            "entries into data/consultations.json following the schema in this file."
        )
        return

    OUT.write_text(json.dumps(consultations, indent=2, ensure_ascii=False))
    print(f"Wrote {len(consultations)} consultations to {OUT}")


if __name__ == "__main__":
    main()
