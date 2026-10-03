# Design critique fixes

An October 3, 2026 design critique of the whole site scored it 24/40 and found five priority issues: Take Action, the legislator briefing, legible evidence, plain language, and type and tap targets. Joshua chose to keep the current visual identity and fix the issues within it, with new copy drafted for his review. PR #162 fixed the letter box and copied-letter formatting. PR #163 fixed the five issues and the consistency list. Joshua reviewed the before-and-after page and the full list of new wording, merged both pull requests and the Dependabot updates #159–#161, closed #149 (TypeScript 7, failing build), and approved publication.

## What changed

- Take Action leads with one petition action, the petition's ask taken from its approved text, and what happens next. The letter text is unchanged.
- The legislator page opens with a one-page briefing: dated figures with their stages, the five safeguards, session dates, and a briefing request and PDF.
- The home exhibit is a rectangular crop of the existing reviewed image, showing the Israel rows, with selected fields typed from the reviewed transcription. Sidebar thumbnails are now typed key-record cards. The evidence summary stacks into cards on phones.
- "In plain terms" openers appear on six pages. Each restates claims already on that page.
- No functional text is under 12 px, interactive targets are 44 px, the focus ring and dark theme are fixed, and safeguard names, arrows, dates and breadcrumbs are consistent.
- PRODUCT.md records the product context and that the visual identity changes only after consulting the team.

No record, figure, title, URL, historical PDF, text download or exhibit changed. The campaign-asset manifest changed only its input fingerprints. Regenerating the assets in a scratch copy produced pixel-identical images and identical PDF text, so the published bytes were left untouched. The September 17 PDF brief still uses the older safeguard names.

## Verification on the merged main

- Full validation: 14 tests passed. Astro check reported zero errors. All 70 pages passed the publication audit (43 claims, 35 source references) and the asset audit (27 historical PDFs including two privacy revisions, 33 reviewed source exhibits). Astro is 7.3.5.
- Browser QA through `scripts/qa_server.py` ran 144 page reports. It covered 14 routes at 320, 390, 768, 1280 and 1536 pixels in light and dark themes, plus four no-JavaScript checks. There were no axe violations (WCAG 2.0/2.1/2.2 A and AA), horizontal overflow, broken images, hidden elements shown or external resources.
- Functional checks passed:
  - Escape closes the menu, and the theme switches.
  - The copied letter keeps its seven paragraphs, and the petition link and the load-in-page option both work.
  - Search returns results.
  - Preserved anchors resolve, including `/the-issue/#how-the-proposal-moved`, `/legislators/#the-proposed-decision-record` and the Take Action anchors.
- An independent reviewer checked every new sentence against existing page content and records. The three wording problems it found were corrected before merge.

The external petition is unchanged. The site's petition panel quotes its approved ask.

The candidate source digest and authorization are recorded in `release-status.json`. Deployment history is updated only after a successful Pages run and live verification.
