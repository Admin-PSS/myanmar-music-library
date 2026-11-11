# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A browser and player for **6,800+ classical Burmese music albums** scraped from the blog **phyuniwarpyar.blogspot.com**. It ships three ways from **one UI file**:

| Target | Entry point | Data source |
|---|---|---|
| Website (GitHub Pages) | `index.html` | `albums.json` (static fetch) |
| Local Flask server | `app.py` → `templates/index.html` | `/api/albums` |
| Android app (Capacitor) | `mobile/` (separate **private** repo) | `albums.json` bundled in the APK |

- Public repo: `Admin-PSS/myanmar-music-library` (GitHub Pages + APK downloads via Releases)
- Private repo: `Admin-PSS/myanmar-music-library-android` (the `mobile/` folder)

## Golden rule: `index.html` is the single source of the UI

- Edit **only** the root `index.html` (plain HTML/CSS/JS, no build step, no framework).
- Then run `python sync_template.py` to regenerate `templates/index.html`. **Never hand-edit the template.** The script swaps the data URL to `/api/albums` and adds a "run the scraper first" hint. It fails if `index.html` contains Jinja syntax (`{{`, `{%`, `{#`), so avoid those.
- If the change should ship in the Android app, rebuild it (see below).

## Running

```bash
pip install -r requirements.txt   # requests, beautifulsoup4, lxml, openpyxl, flask
python app.py                     # Flask on http://localhost:5000 (opens a browser)
python -m http.server             # or serve the static index.html + albums.json
```

## Data

`albums.json` is a ~12 MB array, committed to the repo. Each item:

```js
{ id, artist, title, year, type, format, recordLabel,
  coverUrl,   // https://blogger.googleusercontent.com/... (~400px)
  blogUrl,    // phyuniwarpyar.blogspot.com post
  pcloudUrl,  // pCloud download link
  mediafire,  // MediaFire folder/file link (used for streaming)
  tracklist,  // string[] in Myanmar script
  noAudio }   // optional: cover only
```

`type` drives the colour-coded badges (`TYPE_STYLES`): `ဓါတ်ပြားတေး` (78rpm records), `တိတ်ခွေ` (cassette), `ကက်ဆက်ဇာတ်လမ်း` (cassette drama).

### Scraper

```bash
python scraper.py              # full scrape of the Blogger Atom feed, 30–60 min → albums.json + albums.xlsx
python scraper.py --resume     # skip blogUrls already in albums.json
python scraper.py --limit 20 -v
python scraper_ui.py           # Tkinter GUI wrapper
```

Tracklists are extracted with 4 fallback strategies in `scraper.py`. Strategy 4 (loose lines after a section header) can capture metadata as tracks. Fix bad tracklists in the scraper and re-scrape; don't add JS filters.

## `index.html` architecture

- **Layout:** desktop has three panels (artists | album grid | detail) plus a bottom player bar. At **≤760px** there's a mobile layout: one panel at a time (`body.view-artists|albums|detail`, switched by `setView()`), bottom tab bar, and history entries so Back works. Panels are hidden with `visibility`, not `display:none`, to keep scroll position.
- **Album grid** renders in pages of 60 (`PAGE`) via an IntersectionObserver sentinel. Don't render all 6,800 cards at once (very slow on phones). Clicks use event delegation on `#albums-grid`.
- **Search** matches artist, title and every track (plain JS `includes`, so Myanmar text works).
- **Streaming:** the public MediaFire API (`/api/1.5/folder/get_content.php`, `file/get_info.php`, CORS `*`) lists audio files in an album's folder (up to 2 subfolder levels). `<audio>` plays each file's `links.normal_download`. Results are cached per album in `mfCache`. RAR/ZIP-only albums show a "download instead" message.
- **Android hooks** are guarded by `window.Capacitor` and do nothing on the web:
  - `Capacitor.Plugins.App`: hardware Back calls `history.back()`; on the Albums view it calls `minimizeApp()`.
  - `Capacitor.Plugins.BackgroundAudio` (custom native plugin): `update({title, artist, playing, artUrl})`, `stop()`, and a `"control"` listener (play/pause/next/prev/stop).
  - `body.in-app` hides the "📱 Android App" download link.

## Android app (`mobile/`, private repo, ignored by this repo)

- Capacitor 7, appId `com.adminpss.mmmusic`, `webDir: www`. `npm run copy-web` copies `../index.html` + `../albums.json` into `www/`.
- Native code is in `android/app/src/main/java/com/adminpss/mmmusic/`:
  - `PlaybackService.java`: foreground service (type `mediaPlayback`), MediaSession notification and lock-screen controls, album cover downloaded once per album, wake lock while playing.
  - `BackgroundAudioPlugin.java`: JS bridge, registered in `MainActivity`.
- Build (Windows). Needs **JDK 21**; the system Java is 8, so a portable copy is used:
  ```powershell
  cd mobile
  $env:JAVA_HOME="$env:LOCALAPPDATA\jdk21\jdk-21.0.13+9"
  npm run build:debug      # android/app/build/outputs/apk/debug/app-debug.apk
  npm run build:release    # signed release APK
  npm run assets           # regenerate icon + splash from scripts/make-assets.js (SVG)
  ```
  Android SDK: `%LOCALAPPDATA%\Android\Sdk`. Emulator AVD: `pixel_7_-_api_35`.
- **Release signing:** `android/keystore.properties` (git-ignored) points to a keystore kept **outside both repos**. Never commit `*.jks` / `keystore.properties` or print their contents. If the key is lost, users can't upgrade in place.
- **Releasing a new version:**
  1. Bump `versionCode` / `versionName` in `mobile/android/app/build.gradle`.
  2. `npm run build:release`, then copy the APK to `mobile/release/myanmar-music-library.apk`.
  3. `gh release create vX.Y.Z mobile/release/myanmar-music-library.apk ...` on the **public** repo. The README/website link `releases/latest/download/myanmar-music-library.apk` then points at it automatically.
  4. Add a row to the Versions table in `README.md`.
- Not published on Google Play (copyright risk with streaming third-party-hosted music). Distribution is via the APK on GitHub Releases only.

## Other files

- `myanmar-music-library.jsx`: the original React prototype with a few hard-coded albums. Not used by any target; kept for history.
- `Claude Discussion.md`: early planning notes.
- `docs/`: README screenshots.
