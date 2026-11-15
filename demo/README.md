# Demo site

Static multi-page preview for GitHub Pages. The generator creates `site/` from `build_demo.py`; generated output is not committed.

## Source layout

- `build_demo.py` — creates the pages and copies assets into the generated site.
- `assets/css/style.css` — shared responsive styles.
- `assets/js/app.js` — menu, accessibility controls, motion and demo-only form feedback.
- `site/` — generated output; do not edit by hand.

## Run locally

```bash
python build_demo.py
python -m http.server 8000 --directory site
```

Open http://localhost:8000.

## Pages

- `index.html` — home
- `sveden.html` — organization information
- `parents.html` — parents
- `students.html` — students
- `news.html` — news and announcements
- `priem.html` — admissions
- `contacts.html` — contacts and non-submitting demo form
- `styleguide.html` — design system
- `404.html` — not found

All content blocks requiring school-specific facts are explicitly marked as editor placeholders. The demo form does not transmit or persist entered text.

GitHub Actions builds and tests the site on pull requests but deploys only after a push to `main`. In repository Settings → Pages, select GitHub Actions as the deployment source once.
