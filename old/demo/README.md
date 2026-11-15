# Static HTML demo

This directory is the website. Every page is a real, standalone HTML file.

## Source layout

- `*.html` — page markup; edit the relevant page directly.
- `assets/css/style.css` — shared layout, responsive design and visual components.
- `assets/js/app.js` — mobile menu, accessibility controls, scrolling and demo form feedback.
- `assets/favicon.svg` — site icon.

## Run locally

Open `index.html` directly in a browser, or run:

```bash
python -m http.server 8000
```

Then visit http://localhost:8000.

No Python generator, Node.js, npm or build step is required. Python's built-in server is optional and only serves the files locally.

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

All school-specific facts are clearly marked as placeholders. The form does not transmit or persist entered text.

GitHub Actions uploads this directory directly as the Pages artifact. In repository Settings → Pages, select GitHub Actions as the deployment source.
