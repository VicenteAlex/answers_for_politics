#!/usr/bin/env python3
"""Download Congreso de los Diputados open data (votes per plenary day, deputies, initiatives) into raw/congreso/.

Usage: .venv/Scripts/python tools/congreso_download.py [--leg XIV XV]
Files already downloaded are skipped, so the script can be re-run to resume or to add new sessions.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw" / "congreso"
SITE = "https://www.congreso.es"
UA = {"User-Agent": "Mozilla/5.0 (kb-ingest)"}
PAGE = SITE + "/es/opendata/votaciones?p_p_id=votaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&targetLegislatura={leg}{date}"


def get(url: str, tries: int = 4) -> bytes:
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"  retry ({e}) {url}", file=sys.stderr)
            time.sleep(5 * (i + 1))


def voting_days(leg: str) -> list[str]:
    html = get(PAGE.format(leg=leg, date="")).decode("utf-8", "replace")
    m = re.search(r"var diasVotaciones = \[([^\]]*)\]", html)
    return sorted(set(re.findall(r"\d{8}", m.group(1)))) if m else []


def download_leg(leg: str):
    days = voting_days(leg)
    print(f"{leg}: {len(days)} voting days", file=sys.stderr)
    for n, day in enumerate(days, 1):
        marker = RAW / "votaciones" / leg / day / ".done"
        if marker.exists():
            continue
        date = f"&targetDate={day[6:]}/{day[4:6]}/{day[:4]}"
        html = get(PAGE.format(leg=leg, date=date)).decode("utf-8", "replace")
        links = sorted(set(re.findall(r'/webpublica/opendata/votaciones/[^"]+?\.json', html)))
        for link in links:
            dest = RAW / "votaciones" / leg / day / Path(link).parent.name / Path(link).name
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(get(SITE + link))
                time.sleep(0.15)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(str(len(links)))
        if n % 20 == 0:
            print(f"  {leg}: {n}/{len(days)} days", file=sys.stderr)


def download_lists():
    for page in ("diputados", "iniciativas"):
        html = get(f"{SITE}/es/opendata/{page}").decode("utf-8", "replace")
        for link in sorted(set(re.findall(r'/webpublica/opendata/[^"]+?\.json', html))):
            name = re.sub(r"__\d+", "", Path(link).name)  # drop timestamp
            dest = RAW / page / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(get(SITE + link))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", nargs="+", default=["XIV", "XV"])
    args = ap.parse_args()
    download_lists()
    for leg in args.leg:
        download_leg(leg)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
