# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Four audiences, weighted equally (confirmed by Joshua Dunlap, October 3, 2026), between now and Arkansas's 2027 legislative session:

- **Pension members:** teachers, public employees and retirees in ATRS, APERS and the other covered systems. Their job is to understand what the records show about their retirement money, sign the petition and contact their legislators.
- **Legislators:** possible sponsors and votes. Their job is to grasp the proposal and the financial case quickly and request a briefing.
- **Coalition partners:** members of allied organizations deciding whether to put weight behind the proposal.
- **Journalists:** reporters who need dated facts, primary documents, attribution guidance and a contact.

Each audience has a dedicated entry route (`/educators/`, `/public-employees/`, `/legislators/`, `/press/`).

## Product Purpose

arpensions.org is the public site of Arkansans for Pension Integrity (API), a volunteer-led campaign. It explains Arkansas public records about covered pension investments, publishes the source exhibits behind each finding, and builds support for the Pension Investment Integrity Act, a proposal for the 2027 session. Success is legislative sponsorship and enough member and coalition support to carry the proposal.

## Positioning

Fiduciary first (confirmed). The site leads with pension governance and a public investment record: before a covered investment, a written financial case; after it, publication. The Israel Bonds holdings appear as the documented decisions that show why the standard is needed, not as the headline. The same standards apply regardless of the issuer.

What no neighboring campaign can copy: every figure is tied to a dated primary record the reader can open, with its scope and limits stated.

## Operating Context

- The petition is hosted on Action Network (`ActionPanel.astro`); the site links out and can embed it on request.
- Legislator contact is a copy-and-personalize letter plus a plain-text download.
- A printable one-page policy brief exists as HTML (`/legislators/one-page/`) and PDF.

## Capabilities and Constraints

- Astro static site on GitHub Pages; content in `src/content/pages/` and `src/data/*.json`; Pagefind search; RSS; light and dark themes.
- Publication requires Joshua's approval of the exact candidate (`release-status.json`, `npm run release:check`). Deployment is manual from `main`.
- No analytics, CMS, supporter database, paid service or automatic correspondence. Self-hosted fonts and assets.
- Longstanding URLs, download URLs and historical PDF bytes are preserved.
- Figures from different record dates are never added together; the ATRS bond is inside the ATRS funding, not additional to it.
- Performance budgets: first-party JS ≤50 KB home, ≤100 KB evidence (compressed); shared CSS ≤40 KB.

## Brand Commitments

Name: Arkansans for Pension Integrity (API); domain arpensions.org; contact info@arpensions.org.

The current visual identity is the campaign's established identity: the API badge, pine, teal and jade greens, League Spartan, Mulish and IBM Plex Mono, and the guilloche motif. Joshua does not want it overhauled without consulting the campaign's people (October 3, 2026). Design work refines within it; any change to the identity itself is proposed to the team first.

## Evidence on Hand

- Source records, exhibits, transcripts and checked tables: `public/assets/documents/`, `public/assets/exhibits/`, catalogued in `src/data/public-assets.json` and `src/data/download-catalog.json`.
- Financial records and source locators: `src/data/investigation.json`; claims and their limits: `src/data/publication-matrix.json`.
- No testimonials, endorsements, sponsorships, votes or photographs of members exist. Never invent any. Coalition selection is not enactment or sponsorship.

## Product Principles

1. Prove, don't assert: every claim links to the dated record and states what it can and cannot establish.
2. Lead with members' retirement money and a reasonable governance standard.
3. Plain language over finance jargon; define terms where they first appear.
4. One clear next step per audience.
5. Honesty about limits is part of the case, not a disclaimer.

## Accessibility & Inclusion

WCAG AA as the floor; keyboard navigation, reduced motion, no-JavaScript reading, print, and 320 px phones are acceptance requirements in `docs/rebuild-plan.md`.
