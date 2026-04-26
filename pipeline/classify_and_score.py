"""Classify and score consultations using Claude.

Reads data/consultations.json (or data/sample_consultations.json as fallback),
calls Claude per consultation with a cached system prompt, and writes the
scored output to data/scored.json.

Usage:
    python -m pipeline.classify_and_score
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from pipeline.models import Score
from pipeline.prompt import SCORING_SYSTEM_PROMPT

load_dotenv()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL = "claude-opus-4-7"

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY missing — copy .env.example to .env and fill it in.")

client = Anthropic()


def score_consultation(consultation: dict) -> dict:
    user_text = (
        f"Title: {consultation.get('title', '(no title)')}\n\n"
        f"Summary: {consultation.get('summary', '(no summary)')}\n\n"
        f"Deadline: {consultation.get('deadline', 'unknown')}\n\n"
        f"Source: {consultation.get('source', 'EU Have Your Say')}\n"
        f"Link: {consultation.get('link', '(no link)')}"
    )

    response = client.messages.parse(
        model=MODEL,
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": SCORING_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_text}],
        output_format=Score,
    )

    cached = response.usage.cache_read_input_tokens
    written = response.usage.cache_creation_input_tokens
    print(f"  tokens: in={response.usage.input_tokens} cache_read={cached} cache_write={written}")

    parsed: Score = response.parsed_output
    return {
        **consultation,
        "cause_areas": parsed.cause_areas,
        "impact_score": parsed.impact_score,
        "rationale": parsed.rationale,
        "dimension_notes": parsed.dimension_notes.model_dump(),
    }


def main() -> None:
    src = DATA_DIR / "consultations.json"
    raw = json.loads(src.read_text()) if src.exists() else []
    if not raw:
        fallback = DATA_DIR / "sample_consultations.json"
        print(f"{src.name} is empty; falling back to {fallback.name}.")
        raw = json.loads(fallback.read_text())

    print(f"Scoring {len(raw)} consultations with {MODEL}.")

    scored: list[dict] = []
    for i, c in enumerate(raw, 1):
        title = (c.get("title") or "(no title)")[:80]
        print(f"[{i}/{len(raw)}] {title}")
        try:
            scored.append(score_consultation(c))
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")

    out = DATA_DIR / "scored.json"
    out.write_text(json.dumps(scored, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(scored)} scored consultations to {out}")


if __name__ == "__main__":
    main()
