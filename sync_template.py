#!/usr/bin/env python3
"""Regenerate templates/index.html (Flask) from index.html (GitHub Pages / Android app).

index.html is the single source of truth for the UI. The Flask version differs only in:
  - loading data from /api/albums instead of the static albums.json
  - a "run the scraper first" hint when loading fails

Run after every UI change:   python sync_template.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "index.html"
DST = ROOT / "templates" / "index.html"

REPLACEMENTS = [
    ('fetch("albums.json")', 'fetch("/api/albums")'),
    ("⚠ Could not load albums.json</div>",
     '⚠ Could not load albums.json<br><small style="color:#6b7280">Run the scraper first</small></div>'),
]


def main():
    with open(SRC, encoding="utf-8", newline="") as f:   # newline="" keeps line endings as-is
        html = f.read()
    # Jinja would treat these as template syntax and break the page.
    for token in ("{{", "{%", "{#"):
        if token in html:
            raise SystemExit(f"index.html contains Jinja syntax {token!r} — wrap it in {{% raw %}} or rewrite it")
    for old, new in REPLACEMENTS:
        if html.count(old) != 1:
            raise SystemExit(f"Expected exactly one {old!r} in index.html, found {html.count(old)}")
        html = html.replace(old, new)
    with open(DST, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print(f"wrote {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
