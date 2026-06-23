#!/usr/bin/env python3
"""
Blogger Atom feed scraper for phyuniwarpyar.blogspot.com

Paginates through the full feed, parses each post for album metadata,
cover art, download links, and tracklists, then writes albums.json and
albums.xlsx.

Usage:
    python scraper.py                   # scrape everything
    python scraper.py --limit 20        # first 20 posts (quick test)
    python scraper.py --resume          # skip posts already in albums.json
    python scraper.py -v                # print per-entry parse details
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
from pathlib import Path
from xml.etree import ElementTree as ET

# Force UTF-8 output on Windows so Myanmar characters print without crashing
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

FEED_URL = "https://phyuniwarpyar.blogspot.com/feeds/posts/default"
OUTPUT_JSON = Path("albums.json")
OUTPUT_EXCEL = Path("albums.xlsx")
ATOM_NS = "http://www.w3.org/2005/Atom"
REQUEST_DELAY = 1.5  # seconds between paginated requests

ALBUM_TYPES = ["ဓါတ်ပြားတေး", "တိတ်ခွေ", "ကက်ဆက်ဇာတ်လမ်း"]

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "MyanmarMusicLibraryScraper/1.0"})


# ── Feed pagination ───────────────────────────────────────────────────────────

def fetch_page(start_index: int, max_results: int = 25) -> str:
    url = (
        f"{FEED_URL}"
        f"?start-index={start_index}&max-results={max_results}&alt=atom"
    )
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            if attempt == 2:
                raise
            print(f"  Retry {attempt + 1}/3 after: {exc}")
            time.sleep(5)


def iter_entries(limit: int | None = None):
    """Yield raw XML <entry> elements, paginating until exhausted."""
    start = 1
    total = 0
    while True:
        xml_text = fetch_page(start)
        root = ET.fromstring(xml_text)
        entries = root.findall(f"{{{ATOM_NS}}}entry")
        if not entries:
            break

        for entry in entries:
            yield entry
            total += 1
            if limit is not None and total >= limit:
                return

        has_next = any(
            link.get("rel") == "next"
            for link in root.findall(f"{{{ATOM_NS}}}link")
        )
        if not has_next:
            break

        print(f"  {total} entries fetched — fetching next page …")
        start += 25
        time.sleep(REQUEST_DELAY)


# ── HTML parsing helpers ──────────────────────────────────────────────────────

def detect_type(text: str) -> str | None:
    for t in ALBUM_TYPES:
        if t in text:
            return t
    return None


def extract_year(text: str) -> str | None:
    # Burmese 4-digit numerals first (e.g. ၁၉၈၀)
    m = re.search(r"[၀-၉]{4}", text)
    if m:
        return m.group()
    # Western year 1900–2029
    m = re.search(r"\b(19[0-9]{2}|20[0-2][0-9])\b", text)
    return m.group() if m else None


def extract_format(text: str) -> str | None:
    # Match "MP3 / 320 KBPS / 125 MB" — stop at closing paren, newline, or Myanmar sentence end
    m = re.search(
        r"MP3\s*/\s*(\d+)\s*(?:KBPS|kbps)\s*/\s*([\d.]+\s*(?:MB|GB))",
        text, re.IGNORECASE
    )
    if m:
        return f"MP3 / {m.group(1)} KBPS / {m.group(2).strip()}"
    if re.search(r"cover only", text, re.IGNORECASE) or "Audio မရှိ" in text:
        return "Cover Only"
    return None


TRACKLIST_SECTION_HEADERS = [
    "ပါဝင်သော တေးသီချင်းများ",   # "Contains the following songs"
    "တေးသီချင်းများ စာရင်း",
    "Side A",
    "Side B",
]

# Numbered line: "01.", "၀၁.", "01)", "၁.", "1.", "01။", "၁။"
# Includes Myanmar full stop (།, U+104B) as valid separator
_NUM_LINE_RE = re.compile(r"^(?:[၀-၉]+|\d+)\W+(.+)")


def extract_tracklist(soup: BeautifulSoup) -> list[str]:
    # Strategy 1: <ol><li> list
    ol = soup.find("ol")
    if ol:
        tracks = [li.get_text(" ", strip=True) for li in ol.find_all("li")]
        if tracks:
            return tracks

    # Strategy 2: <ul><li> list (only if plausibly a tracklist)
    ul = soup.find("ul")
    if ul:
        tracks = [li.get_text(" ", strip=True) for li in ul.find_all("li")]
        if len(tracks) > 2:
            return tracks

    full_text = soup.get_text("\n")

    # Strategy 3: numbered lines with Myanmar OR ASCII numbering (any separator)
    tracks = []
    for line in full_text.splitlines():
        line = line.strip()
        m = _NUM_LINE_RE.match(line)
        if m:
            candidate = m.group(1).strip()
            # skip if the stripped text still looks like a section header
            if not re.search(r"Side [AB]|ပါဝင်သော|တေးသီချင်းများ", candidate):
                tracks.append(candidate)
    if tracks:
        return tracks

    # Strategy 4: extract only lines AFTER a known section-header phrase
    # to avoid capturing metadata that precedes the tracklist
    after_header = None
    lower = full_text.lower()
    for header in TRACKLIST_SECTION_HEADERS:
        idx = full_text.find(header)
        if idx != -1:
            after_header = full_text[idx + len(header):]
            break

    source = after_header if after_header is not None else full_text
    candidate_lines = []
    for line in source.splitlines():
        line = line.strip()
        if not line or len(line) > 70 or "http" in line:
            continue
        # Must be Myanmar-script and not look like a download/label line
        if re.search(r"[က-႟ꩠ-ꩿ]", line) and not re.search(
            r"MP3|KBPS|MB|GB|Studio|STUDIO|pCloud|MediaFire|Download"
            r"|Side [AB]|စာရင်း|တေးသံသွင်း|ပါဝင်သော",
            line, re.IGNORECASE
        ):
            candidate_lines.append(line)

    if len(candidate_lines) >= 3:
        seen: set[str] = set()
        return [x for x in candidate_lines if not (x in seen or seen.add(x))]  # type: ignore[func-returns-value]

    return []


def extract_links(soup: BeautifulSoup) -> tuple[str | None, str | None]:
    pcloud = mediafire = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not pcloud and "pcloud.link" in href:
            pcloud = href
        if not mediafire and "mediafire.com" in href:
            mediafire = href
    return pcloud, mediafire


def extract_cover(soup: BeautifulSoup) -> str | None:
    # Prefer Blogger-hosted images (most reliable)
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if "blogger.googleusercontent.com" in src or "bp.blogspot.com" in src:
            return src
    img = soup.find("img", src=True)
    return img["src"] if img else None


def split_artist_title(raw_title: str) -> tuple[str, str]:
    """Split 'Artist - Album Title' → (artist, title). Falls back to ('', raw)."""
    for sep in (" – ", " — ", " - ", "•"):
        if sep in raw_title:
            artist, _, title = raw_title.partition(sep)
            return artist.strip(), title.strip()
    return "", raw_title.strip()


def extract_record_label(text: str) -> str | None:
    # Pattern: "ShortName တေးသံသွင်း (City)" — limit prefix to 25 chars,
    # must start with a non-digit Myanmar character to avoid capturing
    # numbered list prefixes like "၃) ..."
    m = re.search(
        r"([က-႟ꩠ-ꩿ][^\n•;(]{1,24})\s+(တေးသံသွင်း(?:\s*\([^)]{1,20}\))?)",
        text,
    )
    if m:
        return f"{m.group(1).strip()} {m.group(2).strip()}".strip(" •·:()")
    # Fallback: lines with "Studio" or "STUDIO" keyword (short forms)
    m = re.search(r"(?:Studio|STUDIO)[^\n•<]{0,30}", text)
    if m:
        return m.group().strip(" •·:()")
    return None


# ── Entry → album dict ────────────────────────────────────────────────────────

def parse_entry(entry: ET.Element, verbose: bool = False) -> dict:
    def tag(name: str) -> str:
        return entry.findtext(f"{{{ATOM_NS}}}{name}") or ""

    raw_title = tag("title")
    blog_url = ""
    for link in entry.findall(f"{{{ATOM_NS}}}link"):
        if link.get("rel") == "alternate":
            blog_url = link.get("href", "")

    html_content = tag("content") or tag("summary")
    soup = BeautifulSoup(html_content, "html.parser")
    full_text = raw_title + " " + soup.get_text(" ")

    artist, album_title = split_artist_title(raw_title)
    pcloud_url, mediafire_url = extract_links(soup)

    album = {
        "id": None,
        "artist": artist,
        "title": album_title,
        "year": extract_year(full_text),
        "type": detect_type(full_text),
        "format": extract_format(full_text),
        "recordLabel": extract_record_label(full_text),
        "coverUrl": extract_cover(soup),
        "blogUrl": blog_url,
        "pcloudUrl": pcloud_url,
        "mediafire": mediafire_url,
        "tracklist": extract_tracklist(soup),
        "noAudio": not (pcloud_url or mediafire_url),
    }

    if verbose:
        status = f"tracks={len(album['tracklist'])}  pcloud={'Y' if pcloud_url else 'N'}  mf={'Y' if mediafire_url else 'N'}"
        print(f"  [{album['type'] or '?type'}] {raw_title[:60]}")
        print(f"    {status}")

    return album


# ── Output ────────────────────────────────────────────────────────────────────

def save_json(albums: list[dict], path: Path) -> None:
    path.write_text(json.dumps(albums, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(albums)} albums → {path}")


def save_excel(albums: list[dict], path: Path) -> None:
    if not HAS_OPENPYXL:
        print("openpyxl not installed — skipping Excel export (pip install openpyxl)")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Albums"
    ws.append([
        "id", "artist", "title", "year", "type", "format", "recordLabel",
        "coverUrl", "blogUrl", "pcloudUrl", "mediafire", "trackCount",
        "tracklist", "noAudio",
    ])
    for a in albums:
        ws.append([
            a["id"],
            a.get("artist") or "",
            a.get("title") or "",
            a.get("year") or "",
            a.get("type") or "",
            a.get("format") or "",
            a.get("recordLabel") or "",
            a.get("coverUrl") or "",
            a.get("blogUrl") or "",
            a.get("pcloudUrl") or "",
            a.get("mediafire") or "",
            len(a.get("tracklist", [])),
            " | ".join(a.get("tracklist", [])),
            a.get("noAudio", True),
        ])
    # Auto-width columns
    for col in ws.columns:
        max_len = max((len(str(cell.value or "")) for cell in col), default=0)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)
    wb.save(path)
    print(f"Saved {len(albums)} albums → {path}")


def print_summary(albums: list[dict]) -> None:
    total = len(albums)
    with_audio = sum(1 for a in albums if not a["noAudio"])
    by_type: dict[str, int] = {}
    for a in albums:
        t = a.get("type") or "Unknown"
        by_type[t] = by_type.get(t, 0) + 1
    print(f"\n{'─'*40}")
    print(f"Total albums : {total}")
    print(f"With audio   : {with_audio}  |  Cover-only: {total - with_audio}")
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")
    print(f"{'─'*40}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape phyuniwarpyar.blogspot.com Atom feed"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Stop after N posts (useful for testing)"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Load albums.json and skip already-scraped URLs"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print per-entry parse details"
    )
    args = parser.parse_args()

    existing_urls: set[str] = set()
    albums: list[dict] = []

    if args.resume and OUTPUT_JSON.exists():
        albums = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
        existing_urls = {a["blogUrl"] for a in albums}
        print(f"Resuming — {len(albums)} albums already saved")

    new_count = 0
    print(f"Fetching Atom feed from {FEED_URL} …")
    try:
        for entry in iter_entries(limit=args.limit):
            album = parse_entry(entry, verbose=args.verbose)
            if album["blogUrl"] in existing_urls:
                continue
            album["id"] = len(albums) + 1
            albums.append(album)
            existing_urls.add(album["blogUrl"])
            new_count += 1
    except KeyboardInterrupt:
        print("\nInterrupted — saving partial results …")

    print(f"\nParsed {new_count} new entries (total: {len(albums)})")
    save_json(albums, OUTPUT_JSON)
    save_excel(albums, OUTPUT_EXCEL)
    print_summary(albums)


if __name__ == "__main__":
    main()
