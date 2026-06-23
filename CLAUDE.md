# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A React component (`myanmar-music-library.jsx`) that serves as a music library browser for classical Burmese music from the blog **phyuniwarpyar.blogspot.com**. All album data is hardcoded directly in the component — there is no backend, database, or build tooling at this level.

## Running the Component

This is a standalone React JSX file with no `package.json`. To use it, embed it in a React project (Vite, Create React App, Next.js, etc.):

```bash
# Example with Vite
npm create vite@latest my-app -- --template react
# Copy myanmar-music-library.jsx into src/
# Import and render <App /> from it
npm run dev
```

The component has no external npm dependencies beyond React itself.

## Architecture

**Single file, three components:**

- `App` — root component; owns search/filter state, renders the two-column layout (album grid + detail panel)
- `AlbumCard` — displays cover art, title, artist, format badge, and "NO AUDIO" indicator
- `DetailPanel` — full album view with tracklist and download buttons (pCloud / MediaFire)

**Data shape** (hardcoded `albums` array at top of file):
```js
{
  id, artist, title, year, type, format, recordLabel,
  coverUrl,   // hosted on blogger.googleusercontent.com
  blogUrl,    // phyuniwarpyar.blogspot.com post
  pcloudUrl,  // pCloud download link
  mediafire,  // MediaFire folder link
  tracklist,  // string[] of track names in Myanmar script
  noAudio,    // optional bool — cover image only, no download
}
```

**Album types** (`type` field) drive color-coded badges via `TYPE_COLORS`:
- `ဓါတ်ပြားတေး` — vinyl/SP records
- `တိတ်ခွေ` — CD
- `ကက်ဆက်ဇာတ်လမ်း` — cassette drama

**Search** (`useMemo`) matches against `artist`, `title`, and every track in `tracklist` — Myanmar text is supported via standard JS string includes.

## Scaling Up

The `Claude Discussion.md` notes a planned Python scraper to pull 800+ blog posts from the Blogger RSS/Atom feed (`phyuniwarpyar.blogspot.com/feeds/posts/default`) into Excel, then feed into this UI. When implementing:
- The scraper output should match the `albums` array schema above
- Replace the hardcoded array with a JSON import or API call
