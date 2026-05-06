# Gold Gala 2026 — Staff Hub

A mobile-first staff directory and event reference site for Gold Gala 2026.

## Project structure

```
gg26-staff-hub/
├── index.html              # Landing page (5-item menu + quick find)
├── staff/
│   ├── index.html          # Directory with phase tabs + search
│   └── [name].html         # Detail page (handles /staff/ada-lee/ etc.)
├── ros/index.html          # Run of show
├── faqs/index.html         # FAQ accordion
├── leads/index.html        # Key contacts (tap to call)
├── walkies/index.html      # Walkie channels + protocol
├── assets/
│   ├── style.css           # Shared design system
│   ├── data.js             # Staff, leads, walkies (window.GG_DATA)
│   └── faqs.js             # FAQ content (window.GG_FAQS)
├── vercel.json             # Routing config
└── README.md
```

## Deploy to GitHub + Vercel (10 min)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USER/gg26-staff-hub.git
git push -u origin main
```

### 2. Deploy on Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the GitHub repo
3. Framework preset: **Other** (it's static, no build needed)
4. Build command: leave blank
5. Output directory: leave blank
6. Click Deploy

You'll get a URL like `gg26-staff-hub.vercel.app` in ~30 seconds.

### 3. Custom domain (optional)
Vercel → Project → Settings → Domains → add a domain. Free SSL included.

## Update data when staffing changes

Two ways:

**Quick edits:** Open `assets/data.js` directly. It's a single `window.GG_DATA = { staff: [...], leads: [...], walkies: [...] };` object. Edit, commit, push. Vercel auto-redeploys.

**Full re-import from spreadsheet:** If you re-export the Day of Staffing Kit xlsx, run the Python build script (see `build_data.py` if added later, or send the file to Joanna for regeneration).

## Design notes

- Inspired by the GG26 creative direction deck — pure black backgrounds, warm amber-gold (`#c89c3f`), refined Fraunces serif headlines paired with Inter body
- Mobile-first at 390px viewport (iPhone 13/14/15 Pro)
- All phone numbers are tap-to-call (`tel:` URIs)
- All emails are tap-to-email (`mailto:` URIs)
- Phase tabs respect that team assignments change per phase (e.g. Amy Qi: Talent during Cocktails → Gifting during Founders Party)
- Search hits name, role, AND team simultaneously

## Routes

| URL | Purpose |
|---|---|
| `/` | Home menu |
| `/staff` | Directory with phase tabs |
| `/staff#dinner` | Directory pre-selected to Dinner phase |
| `/staff/ada-lee` | Individual staff detail |
| `/ros` | Run of show |
| `/faqs` | FAQs |
| `/leads` | Team leads |
| `/walkies` | Walkie channels |

## Known data caveats

- "z." prefix names (z.Bing Chen, z.Rose Yan) are normalized to drop the prefix
- "MIkkoh" (typo) → "Mikkoh"
- "Photo / VIdeo" (typo) → "Photo / Video"
- Mikkoh Chen: Cocktails only. No assignment for Dinner/Founders.
- Tiffany Hsu: Cocktails (Traffic Flow), Founders (VIP Support 10-11 PM). No Dinner assignment.
- Ananya Mishra: Social Team Floater across all phases.

## Working with Claude Code

To continue iterating in Claude Code, paste this when you start the session:

> I'm working on `gg26-staff-hub`, a mobile-first static site for Gold Gala 2026 staff. Pure HTML/CSS/JS, no build step. Data lives in `assets/data.js` as `window.GG_DATA = { staff, leads, walkies }`. FAQs in `assets/faqs.js` as `window.GG_FAQS`. Each route is its own folder with `index.html` (e.g. `/staff/index.html`, `/ros/index.html`). Detail pages use `/staff/[name].html` with Vercel rewrites in `vercel.json` mapping `/staff/:name` to it. Design system in `assets/style.css` — pure black bg (`#050505`), warm amber gold (`#c89c3f` primary, `#e8b94a` bright), Fraunces serif headlines + Inter body. The site uses CSS variables defined at `:root` in `style.css`. Mobile-first (max-width 640px). All pages share the topbar + back button pattern.

### Common tasks for Claude Code

- **Add a new section to ROS:** edit the `phases` array in `ros/index.html`
- **Update FAQ content:** edit `assets/faqs.js` (or regenerate from the docx)
- **Change a staff member's role:** edit `assets/data.js` — find by name in the `staff` array
- **Add a new menu item to home:** add an `<a class="menu-item">` in `index.html` and create the matching `/section/index.html`
- **Tweak the design:** edit CSS variables at the top of `assets/style.css`
