# Gold Gala 2026 — Staff Hub

A mobile-first staff directory and event reference site for Gold Gala 2026.
Lives at https://github.com/joannaleelin/gg26 and auto-deploys to Vercel on every push to `main`.

## Project structure

```
gg26/
├── index.html                          # Landing page (Gold House logo, 5-item menu)
├── staff/
│   ├── index.html                      # Directory with phase tabs + search
│   └── [name].html                     # Per-person detail page (handles /staff/ada-lee/ etc.)
├── ros/index.html                      # Run of show
├── faqs/index.html                     # FAQ accordion
├── leads/index.html                    # Key contacts (tap to call)
├── walkies/index.html                  # Walkie channels + radio protocol
├── before-you-arrive/index.html        # Shared "Before You Arrive: Saturday, May 9" page
├── day-of-professionalism/index.html   # Shared "Day-of Professionalism" page
├── assets/
│   ├── style.css                       # Shared design system
│   ├── data.js                         # Staff, leads, walkies (window.GG_DATA)
│   ├── faqs.js                         # FAQ content (window.GG_FAQS)
│   ├── info-sheets.js                  # Per-person info sheets (window.GG_INFO_SHEETS)
│   └── images/
│       └── gold-gala-logo.png          # Gold House logo (used in home topbar)
├── vercel.json                         # Routing config (rewrites /staff/:name → [name].html)
└── README.md
```

## Local preview

You can open `index.html` directly in a browser, but the dynamic per-person URLs
(`/staff/ada-lee` → routed to `[name].html`) only work when served over HTTP.

From the repo root:
```bash
python3 -m http.server 8765
```

Then visit http://localhost:8765/. To stop the server, hit `Ctrl+C` (or `pkill -f "http.server 8765"`).

For local testing, person URLs use a query string: `http://localhost:8765/staff/[name].html?slug=ada-lee`.
On the deployed site, Vercel rewrites give you the cleaner `https://YOUR-VERCEL-URL/staff/ada-lee`.

## Day-to-day workflow

1. Edit files locally (in your editor of choice, or with Claude Code).
2. Preview with `python3 -m http.server 8765` if you want to click around.
3. Commit and push:
   ```bash
   git add <files-you-changed>
   git commit -m "describe the change"
   git push origin main
   ```
4. Vercel auto-deploys in ~30 seconds. Check your Vercel project URL.

If you don't want to run terminal commands, you can also edit files directly on
github.com (each file has a pencil ✏️ icon) and Vercel will deploy on save.

## Updating staff data

There are two layers:

### Layer 1 — `assets/data.js` (driver of the staff directory)

This is the canonical staff list — name, contact info, per-phase role/team/lead.
It powers `/staff` (the directory) and the basic per-person view.

- **Quick edit:** open `assets/data.js`, find the person, change their fields, push.
- **Full re-import from spreadsheet:** if you re-export `Gold Gala 2026 - Day of Staffing Kit.xlsx`,
  send to whoever maintains the build script and they regenerate `data.js`.
  (The script that originally produced it is not in this repo — keep `data.js` as the source-of-truth here.)

### Layer 2 — `assets/info-sheets.js` (rich per-person detail pages)

This is the per-person personalized info sheet — timeline, assignments table, role
description, ideal break window, etc. It corresponds to the Word docs in
`/Individual Assignments/` (kept outside this repo).

- **Currently populated for:** Ada Lee, Daniel Park, Allie Woo (3 of ~47 .docx files).
- **A name in `data.js` is clickable on `/staff` only if there's an entry for them in `info-sheets.js`.** Names without an entry render as plain text (intended — full-time staff don't need an individual page).
- **To add an info sheet** for someone new: open `assets/info-sheets.js`, copy one of the existing entries (Ada Lee is a good template — single role across phases; Allie Woo is the right template if the person has multiple different roles), update every field. The schema is documented at the top of the file.
- The shared "Before You Arrive" and "Day-of Professionalism" content does NOT belong in info sheets — those are pulled out into their own pages (see below).

## Editing shared content

Two pages are shared by every per-person info-sheet page (linked from the top
nav buttons). When you edit them, the change is reflected for everyone:

- `/before-you-arrive/index.html` — Arrivals · Where to Meet · What to Bring
- `/day-of-professionalism/index.html` — Dress · Phones, Photos & Social · Activations & Alcohol · Conduct & Escalation

Don't duplicate this content into individual info sheets.

## Routes

| URL | Purpose |
|---|---|
| `/` | Home menu |
| `/staff` | Directory with phase tabs |
| `/staff#dinner` | Directory pre-selected to Dinner phase |
| `/staff/ada-lee` | Individual staff detail (rich layout if info sheet exists) |
| `/ros` | Run of show |
| `/faqs` | FAQs |
| `/leads` | Team leads |
| `/walkies` | Walkie channels + radio protocol |
| `/security` | Badge types, zone maps, banned list |
| `/before-you-arrive` | Shared "Before You Arrive: Saturday, May 9" page |
| `/day-of-professionalism` | Shared "Day-of Professionalism" page |

## Design notes

- Inspired by the GG26 creative direction deck — pure black backgrounds, warm amber-gold (`#c89c3f`), refined Fraunces serif headlines paired with Inter body
- Mobile-first at 390px viewport (iPhone 13/14/15 Pro)
- All phone numbers are tap-to-call (`tel:` URIs)
- All emails are tap-to-email (`mailto:` URIs)
- Phase tabs respect that team assignments change per phase (e.g. Amy Qi: Talent during Cocktails → Gifting during Founders Party)
- Search on `/staff` hits name, role, AND team simultaneously

## Known data caveats

- "z." prefix names (z.Bing Chen, z.Rose Yan) are normalized to drop the prefix
- "MIkkoh" (typo) → "Mikkoh"
- "Photo / VIdeo" (typo) → "Photo / Video"
- Mikkoh Chen: Cocktails only. No assignment for Dinner/Founders.
- Tiffany Hsu: Cocktails (Traffic Flow), Founders (VIP Support 10-11 PM). No Dinner assignment.
- Ananya Mishra: Social Team Floater across all phases.

## Working with Claude Code

This repo was built with Claude Code's help. To continue iterating, just open the
repo folder in Claude Code and describe what you want — Claude can read all the
files directly.

For long-running work, here's a context block worth pasting at session start:

> I'm working on `gg26`, a mobile-first static site for Gold Gala 2026 staff (deployed to Vercel from GitHub `joannaleelin/gg26`). Pure HTML/CSS/JS, no build step. Three data sources: `assets/data.js` (window.GG_DATA = { staff, leads, walkies }), `assets/faqs.js` (window.GG_FAQS), `assets/info-sheets.js` (window.GG_INFO_SHEETS — per-person personalized pages, schema documented at top of the file). Each route is its own folder with `index.html`. Per-person pages use `/staff/[name].html` with Vercel rewrites in `vercel.json` mapping `/staff/:name` → it. Shared content for individual pages lives at `/before-you-arrive` and `/day-of-professionalism`. Design system in `assets/style.css` — pure black bg (`#050505`), warm amber gold (`#c89c3f` primary, `#e8b94a` bright), Fraunces serif headlines + Inter body, CSS variables at `:root`. Mobile-first (max-width 640px). All pages share the topbar + back button pattern. Source materials live in the parent folder: `Individual Assignments/` (.docx info sheets for ~47 staff) and `Reference for Content/` (Excel staffing kit, FAQ docx, creative direction pptx).

### Common tasks

- **Add a new info sheet for someone**: copy an entry in `assets/info-sheets.js` (Ada Lee = single role, Allie Woo = multiple roles), fill in their fields from the corresponding `.docx`, push.
- **Edit shared "Before You Arrive" / "Day-of Professionalism" content**: edit `before-you-arrive/index.html` or `day-of-professionalism/index.html`. Changes propagate to every person automatically.
- **Update a staff member's role/lead/phone in the directory**: edit `assets/data.js` — find by name in the `staff` array.
- **Update FAQ content**: edit `assets/faqs.js`.
- **Add a new section to ROS**: edit the `phases` array in `ros/index.html`.
- **Add a new menu item to home**: add an `<a class="menu-item">` in `index.html` and create the matching `/section/index.html`.
- **Tweak the design**: edit CSS variables at the top of `assets/style.css`.
