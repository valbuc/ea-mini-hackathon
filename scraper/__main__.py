"""Fetch EU "Have Your Say" public consultations with open feedback.

One-shot CLI:
    python -m scraper

Writes data/consultations.json in the shape consumed by pipeline/.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

BASE = "https://ec.europa.eu/info/law/better-regulation/brpapi"
SEARCH_URL = f"{BASE}/searchInitiatives"
DETAIL_URL = f"{BASE}/groupInitiatives/{{id}}"

PAGE_SIZE = 40
MAX_PAGES = 1
REQUEST_TIMEOUT = 30
SLEEP_BETWEEN_DETAILS = 0.1

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "data" / "consultations.json"


def _get_json(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _iter_search_hits():
    for page in range(MAX_PAGES):
        params = {
            "frontEndStage": "OPC_LAUNCHED",
            "receivingFeedbackStatus": "OPEN",
            "language": "EN",
            "page": page,
            "size": PAGE_SIZE,
        }
        _log(f"[search] page {page} (size={PAGE_SIZE})…")
        data = _get_json(SEARCH_URL, params=params)
        page_obj = data.get("initiativeResultDtoPage") or {}
        hits = page_obj.get("content") or []
        total_pages = page_obj.get("totalPages")
        total_elements = page_obj.get("totalElements")
        _log(
            f"[search] page {page}: {len(hits)} hits "
            f"(totalPages={total_pages}, totalElements={total_elements})"
        )
        if not hits:
            return
        for hit in hits:
            yield hit
        if isinstance(total_pages, int) and page + 1 >= total_pages:
            return


def _pick_publication(detail: dict[str, Any]) -> dict[str, Any] | None:
    for pub in detail.get("publications") or []:
        if (
            pub.get("frontEndStage") == "OPC_LAUNCHED"
            and pub.get("receivingFeedbackStatus") == "OPEN"
        ):
            return pub
    return None


def _normalize_date(raw: str | None) -> str | None:
    if not raw:
        return None
    # API format: "2026/07/16 23:59:59"
    head = raw.split(" ", 1)[0]
    return head.replace("/", "-") or None


def _html_to_text(raw: str | None) -> str:
    if not raw:
        return ""
    return BeautifulSoup(raw, "html.parser").get_text(separator=" ", strip=True)


def _build_record(hit: dict[str, Any], pub: dict[str, Any]) -> dict[str, Any]:
    initiative_id = str(int(hit["id"]))
    title = pub.get("title") or hit.get("shortTitle") or ""
    summary = _html_to_text(pub.get("consultationObjective"))
    deadline = _normalize_date(pub.get("endDate"))
    if not deadline:
        statuses = hit.get("currentStatuses") or []
        if statuses:
            deadline = _normalize_date(statuses[0].get("feedbackEndDate"))
    return {
        "id": initiative_id,
        "title": title,
        "summary": summary,
        "deadline": deadline,
        "source": "EU Have Your Say",
        "link": f"https://have-your-say.ec.europa.eu/initiatives/{initiative_id}",
    }


def main() -> int:
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    skipped_no_pub = 0
    skipped_error = 0

    processed = 0
    for hit in _iter_search_hits():
        raw_id = hit.get("id")
        if raw_id is None:
            continue
        initiative_id = str(int(raw_id))
        if initiative_id in seen_ids:
            _log(f"[skip] {initiative_id}: duplicate")
            continue
        processed += 1
        short = (hit.get("shortTitle") or "").strip()
        preview = short[:70] + ("…" if len(short) > 70 else "")
        _log(f"[detail {processed}] id={initiative_id} {preview!r}")

        try:
            detail = _get_json(DETAIL_URL.format(id=initiative_id))
        except requests.RequestException as exc:
            _log(f"[warn] detail fetch failed for {initiative_id}: {exc}")
            skipped_error += 1
            continue

        pub = _pick_publication(detail)
        if pub is None:
            _log(f"[skip] {initiative_id}: no OPC_LAUNCHED+OPEN publication")
            skipped_no_pub += 1
            continue

        record = _build_record(hit, pub)
        records.append(record)
        seen_ids.add(initiative_id)
        _log(f"[ok]   {initiative_id} deadline={record['deadline']}")
        time.sleep(SLEEP_BETWEEN_DETAILS)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")

    print(
        f"Wrote {len(records)} consultations to {OUTPUT_PATH.relative_to(REPO_ROOT)} "
        f"(skipped: {skipped_no_pub} no-matching-publication, {skipped_error} errors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
