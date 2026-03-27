# CLAUDE.md — Adi's Personal Website

## Project Goal

A personal website for Adi Bhalla. Clean, elegant, slightly warm — feels like a well-designed personal homepage, not a portfolio template. The aesthetic is intentionally understated: off-white background with subtle paint fleck texture, serif typography, dark navy text.

## Running Locally

```bash
cd "/Users/adibhalla/Downloads/Adi's Website"
open index.html
# or
python3 -m http.server 8080
# → http://localhost:8080/
```

No API calls — opening `index.html` directly in the browser works fine.

## File Structure

```
Adi's Website/
├── index.html              # Entire site (single-page app — all sections here)
├── CLAUDE.md
├── Aditya_Bhalla_Resume_March_2026.pdf
└── assets/
    ├── voter-guide.png         # Screenshot of 2026elections.netlify.app
    ├── Adi_FirstTimeVoting.jpeg
    ├── Adi_Family_Vancouver.jpeg
    ├── Adi_Perbhaat.jpg
    ├── Adi_IceCream.jpg        # Was HEIC — converted to JPEG with: sips -s format jpeg file.jpg --out file.jpg
    ├── Adi_Ayo_JoJo.jpg
    └── covers/
        ├── apple_in_china.jpg
        ├── retribution.jpeg
        └── betrayal.jpg
```

## Design Language

- **Background**: `#faf7f2` (warm off-white)
- **Primary text**: `#1e3a5f` (dark navy)
- **Secondary/accent**: `#8fa4c2` (muted blue-gray — used for dots, dividers, meta text)
- **Body text**: `#2a4060` or `#3a5070` (slightly lighter navy for readability)
- **Font**: [Libre Baskerville](https://fonts.google.com/specimen/Libre+Baskerville) — clean professional serif, similar to Times New Roman but screen-optimized
- **Paint flecks**: 110 tiny dots/ellipses at seeded random positions; colors are muted warm tones (dusty rose, sage, ochre, muted blue, mauve). Seed is fixed so flecks don't jump on resize.

## Navigation / Structure

Single-page app. All content lives in `index.html`. JavaScript swaps sections in/out with fade transitions.

- **Landing**: Typewriter animation ("Hi, I'm Adi") → divider → 4 nav bullets (About, Writing, Projects, Book Reviews)
- **About**: Two-column layout — bio text left, photo collage right. Wider max-width (1100px vs 800px for other pages).
- **Writing**: Substack posts pulled manually from RSS feed
- **Projects**: Project cards with title, blurb, screenshot, link
- **Book Reviews**: Horizontal book cards with genre + star rating filters

## About Page — Photo Collage

5 photos arranged as an overlapping collage using absolute positioning within `.about-collage` (400×520px container). Each photo has its own class `.cp1`–`.cp5` controlling position, size, and tilt. Clicking a photo opens a lightbox (blurred overlay, image centered). Click outside or press Escape to close.

To adjust a photo's position/size, edit its class in the CSS:
```css
.cp1 { width: 175px; height: 215px; top: 0px; left: 0px; transform: rotate(-2.5deg); z-index: 4; }
```
- `top`/`left` → position within collage
- `width`/`height` → photo size
- `rotate()` → tilt angle (negative = lean left)
- `z-index` → which photo sits on top (higher = in front)

**Note on iPhone photos**: iPhones sometimes save HEIC images with a `.jpg` extension. Browsers won't display these. Convert with: `sips -s format jpeg file.jpg --out file.jpg`

## Landing Animation Sequence

1. `400ms` delay
2. "Hi, I'm Adi" types out (~92ms/char + random variance, +75ms at spaces, +110ms at commas)
3. Cursor blinks, then fades out after `850ms` pause
4. Divider fades in
5. Nav bullets appear one by one (`280ms` apart)

## Adding a Project

In the `#projects` section, duplicate the `.project-card` div and fill in:
- Title
- Blurb
- Screenshot → save image to `assets/` and update `src`
- Live link

## Adding a Book

In the `#books` section, duplicate a `.book-card` div (there's a commented-out template):
- Save cover image to `assets/covers/book-slug.jpg`
- Fill in title, author, star rating (★ = filled, ☆ = empty, out of 5), date, blurb
- Blurbs should be roughly 2–3 sentences for visual consistency across the grid

## Deployment

Hosted on **GitHub Pages** from the `adi-website` repo. Custom domain: **adibhalla.com** (registered on Squarespace).

To deploy updates: push to `main` — GitHub Pages auto-publishes.

## What's Next

1. Add the voter-guide screenshot (save `assets/voter-guide.png`)
2. Add book cover for Apple in China (save `assets/covers/apple-in-china.jpg`)
3. Add more projects and books as they come
