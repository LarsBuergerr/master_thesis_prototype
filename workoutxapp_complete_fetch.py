"""
Fetch every exercise from the WorkoutX API (https://api.workoutxapp.com/v1/exercises)
and store the result as a single JSON-LD document. If the free-plan request
budget still allows it afterwards, also download the animated GIF for each
exercise.

Free plan limits this script respects:
- 500 requests/day total (TOTAL_REQUEST_BUDGET)
- 30 requests/minute       (REQUESTS_PER_MINUTE, throttled with a safety margin)

With PAGE_LIMIT=10 (the API default), listing all exercises takes roughly
140 requests, leaving the rest of the 500/day budget for GIF downloads.

Requires WORKOUT_API_KEY in the environment or in a .env file (python-dotenv).
"""
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("WORKOUT_API_KEY")
if not API_KEY:
    sys.exit("WORKOUT_API_KEY is not set (checked environment and .env).")

BASE_URL = "https://api.workoutxapp.com/v1/exercises"
HEADERS = {"X-WorkoutX-Key": API_KEY}

PAGE_LIMIT = 10
TOTAL_REQUEST_BUDGET = 500
REQUESTS_PER_MINUTE = 30
# Small safety margin below the hard 30/min limit to absorb clock drift.
MIN_REQUEST_INTERVAL = 60 / (REQUESTS_PER_MINUTE - 2)

OUTPUT_DIR = Path(__file__).parent / "data" / "workoutx"
EXERCISES_JSONLD_PATH = OUTPUT_DIR / "exercises.jsonld"
GIF_DIR = OUTPUT_DIR / "gifs"

requests_used = 0
_last_request_ts = 0.0


def _wait_for_slot():
    global _last_request_ts
    elapsed = time.monotonic() - _last_request_ts
    wait = MIN_REQUEST_INTERVAL - elapsed
    if wait > 0:
        time.sleep(wait)


def _throttled_get(url, params=None, stream=False, max_retries=3):
    """GET with rate limiting, request-budget tracking and 429 backoff."""
    global requests_used, _last_request_ts
    if requests_used >= TOTAL_REQUEST_BUDGET:
        raise RuntimeError(
            f"Request budget exhausted ({requests_used}/{TOTAL_REQUEST_BUDGET})."
        )
    for attempt in range(max_retries + 1):
        _wait_for_slot()
        resp = requests.get(url, headers=HEADERS, params=params, stream=stream, timeout=30)
        requests_used += 1
        _last_request_ts = time.monotonic()
        if resp.status_code == 429 and attempt < max_retries:
            retry_after = float(resp.headers.get("Retry-After", 5))
            print(f"[rate-limit] 429 received, backing off {retry_after}s ...")
            time.sleep(retry_after)
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp


def _first_present(d, keys):
    for k in keys:
        if d.get(k):
            return d[k]
    return None


def fetch_all_exercises():
    exercises = []
    offset = 0
    while True:
        print(
            f"[fetch] offset={offset} "
            f"(requests used: {requests_used}/{TOTAL_REQUEST_BUDGET})"
        )
        try:
            resp = _throttled_get(BASE_URL, params={"limit": PAGE_LIMIT, "offset": offset})
        except RuntimeError as e:
            print(f"[fetch] stopping early: {e}")
            break
        page = resp.json()
        items = page if isinstance(page, list) else page.get("data") or page.get("exercises") or []
        if not items:
            break
        exercises.extend(items)
        offset += PAGE_LIMIT
        if len(items) < PAGE_LIMIT:
            break
    return exercises


def to_jsonld(exercises):
    graph = []
    for ex in exercises:
        ex_id = _first_present(ex, ["id", "exerciseId", "_id", "slug"])
        entry = {"@type": "Exercise"}
        if ex_id:
            entry["@id"] = f"urn:workoutx:exercise:{ex_id}"
        entry.update(ex)
        graph.append(entry)
    return {
        "@context": {
            "@vocab": "https://api.workoutxapp.com/vocab#",
            "schema": "https://schema.org/",
            "name": "schema:name",
            "gifUrl": {"@id": "schema:image", "@type": "@id"},
        },
        "@graph": graph,
    }


def save_exercises(exercises):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = to_jsonld(exercises)
    with open(EXERCISES_JSONLD_PATH, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"[save] {len(exercises)} exercises -> {EXERCISES_JSONLD_PATH}")


def download_gifs(exercises):
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    remaining = TOTAL_REQUEST_BUDGET - requests_used
    print(f"[gifs] requests remaining after exercise fetch: {remaining}")
    downloaded, skipped = 0, 0
    for ex in exercises:
        if requests_used >= TOTAL_REQUEST_BUDGET:
            print("[gifs] request budget exhausted, stopping.")
            break
        gif_url = _first_present(ex, ["gifUrl", "gif", "animationUrl", "image"])
        ex_id = _first_present(ex, ["id", "exerciseId", "_id", "slug"])
        if not gif_url or not ex_id:
            skipped += 1
            continue
        dest = GIF_DIR / f"{ex_id}.gif"
        if dest.exists():
            continue
        try:
            resp = _throttled_get(gif_url, stream=True)
        except RuntimeError as e:
            print(f"[gifs] stopping early: {e}")
            break
        except requests.RequestException as e:
            print(f"[gifs] failed for {ex_id}: {e}")
            continue
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        downloaded += 1
    print(f"[gifs] downloaded {downloaded} gifs ({skipped} skipped, no gif/id) -> {GIF_DIR}")


def main():
    exercises = fetch_all_exercises()
    save_exercises(exercises)
    download_gifs(exercises)
    print(f"[done] total requests used: {requests_used}/{TOTAL_REQUEST_BUDGET}")


if __name__ == "__main__":
    main()
