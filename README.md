# ဖြူနီဝါပြာ Music Library

A browser for **6,800+ classical Burmese music albums** scraped from [phyuniwarpyar.blogspot.com](https://phyuniwarpyar.blogspot.com).

**[▶ Open Live Demo](https://admin-pss.github.io/myanmar-music-library/)** · **[📱 Download Android App (APK)](https://github.com/Admin-PSS/myanmar-music-library/releases/latest/download/myanmar-music-library.apk)**

![screenshot](screenshot.png)

## Features

- Browse albums by artist with album count
- Filter by format type (ဓါတ်ပြားတေး · တိတ်ခွေ · ကက်ဆက်ဇာတ်လမ်း)
- Search by artist name, album title, or any song in the tracklist
- Full tracklist with track-level search
- pCloud / MediaFire download links and blog post links
- Listen in the browser (MediaFire streaming player)
- Mobile-friendly layout

## Android app

Download the latest APK from [Releases](https://github.com/Admin-PSS/myanmar-music-library/releases/latest).
It keeps playing music in the background and has lock-screen / notification controls.

To install: open the downloaded `.apk` on your phone and allow **"Install unknown apps"** when Android asks.
Google Play Protect may warn that the app is from an unknown developer — tap **Install anyway**.

## Run locally

```bash
pip install -r requirements.txt
python app.py
# Opens http://localhost:5000 automatically
```

## Re-scrape the blog

```bash
# Full scrape (~6,800 posts, takes 30–60 min)
python scraper.py

# Resume after interruption
python scraper.py --resume

# Or use the GUI
python scraper_ui.py
```

Scraper output: `albums.json` + `albums.xlsx`

## Project structure

```
├── scraper.py          # Blogger Atom feed scraper
├── scraper_ui.py       # Tkinter GUI for the scraper
├── app.py              # Flask dev server
├── templates/
│   └── index.html      # Flask template (fetches /api/albums)
├── index.html          # Static version for GitHub Pages
├── albums.json         # Scraped album data (6,800+ albums)
└── requirements.txt
```

## Data source

All album data is scraped from [phyuniwarpyar.blogspot.com](https://phyuniwarpyar.blogspot.com) — a blog dedicated to preserving classical Burmese music. Downloads link to pCloud and MediaFire as hosted by the blog author.
