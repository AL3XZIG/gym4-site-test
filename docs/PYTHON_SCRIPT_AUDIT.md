# Python prototype audit (historical)

The original Qwen Python files are retained in the repository as historical prototypes. They were useful for producing early visual iterations, but a Python-generated HTML pipeline is not part of the current demo architecture.

## Current decision

The GitHub Pages demo is plain static web content:

- `demo/*.html` — independently editable pages.
- `demo/assets/css/style.css` — shared stylesheet.
- `demo/assets/js/app.js` — browser-side interaction.
- `demo/assets/favicon.svg` — favicon.

There is no Python site generator, runtime backend, npm build, or generated `site/` directory. GitHub Actions verifies the expected files and publishes `demo/` directly.

## Historical observations

The earlier prototype scripts combined page content, shared shell, CSS/JS generation and build/deploy configuration in large Python string templates. This made ordinary content edits harder for a school administrator and obscured the actual HTML/CSS deliverables. The scripts also included demo-form persistence and unverified school contact/content claims in earlier iterations.

The current static implementation intentionally removes that generator dependency. Each HTML file can be opened and edited directly in any text editor. Shared appearance belongs in the CSS file; browser behavior belongs in the JS file.

## Future production system

For a real editorial workflow with login, roles, document uploads and server-side forms, use the separate production proposal in `ARCHITECTURE.md`. That future backend is not required to run or publish this static demo.
