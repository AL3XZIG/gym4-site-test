# Tests v4 and pre-release QA

The repository has two test layers:

- Root demo checks validate source structure, links, education disclosure structure and selected backend behavior.
- tools/browser_qa.mjs runs Chromium smoke checks for every declared route at 320, 360, 390, 768, 1280, 1440 and 1920 CSS pixels. It checks page structure, uncaught JavaScript exceptions, horizontal overflow, mobile navigation, accessibility controls and axe-core WCAG 2.1 A/AA findings.

Run locally:

```bash
npm install --no-save --no-package-lock playwright @axe-core/playwright
npx playwright install --with-deps chromium
node tools/browser_qa.mjs
```

The GitHub Actions workflow .github/workflows/browser-qa.yml runs this suite on pull requests targeting main or v4-release-work.

Limitations:
- Chromium automation is not manual Firefox/WebKit testing.
- axe-core does not prove legal compliance or usability with every assistive technology.
- TalkBack, NVDA, VoiceOver, keyboard-only review, 200% browser zoom and real-device checks remain manual.
- Serious and moderate axe findings are reported as warnings; critical findings fail the job.
- A green run does not validate school content, legal basis for personal data, production configuration or backup restoration.
