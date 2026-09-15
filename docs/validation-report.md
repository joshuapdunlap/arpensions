# Rebuild validation and review handoff

Candidate reviewed September 15, 2026. This report describes local implementation and verification. It does not establish production deployment, petition alignment or complete WCAG conformance.

## Automated checks

| Check | Result |
| --- | --- |
| Financial and release tests | 13 pass, including canceled/processing exclusions, overlapping portfolio observations, manager-funding double counting, mixed dates and approval fingerprints |
| Astro diagnostics | No errors, warnings or hints |
| Production output | 68 HTML pages; 65 indexed by Pagefind |
| Publication relationships | 43 claims, 34 sources; source and financial-record references resolve |
| Compatibility | All 37 original routes and 435 original fragment IDs preserved; aliases placed beside relevant updated sections |
| Historical downloads | All 27 PDF hashes match the baseline |
| Reviewed public evidence | 32 source assets with locators, transcripts, treatments and hashes; source-page previews retained |
| Current campaign assets | One-page PDF brief, synchronized letter, 65 page-specific social cards and owned QR destination |
| Artifact freshness | Source fingerprints and rendered-title comparisons reject outdated briefs/cards; explicit LF exports preserve text hashes across Windows and Linux |
| Initial compressed JavaScript | Home 659 bytes; evidence 1,047 bytes. Search and the explicitly requested petition load separately |
| Shared compressed CSS | 7,759 bytes, below the 40 KB budget |
| Dependencies | npm audit reports zero vulnerabilities, including development dependencies |
| Release gate | Correctly rejects the unapproved candidate and unverified external petition |

Ordinary validation runs entirely from the repository, without the evidence vault. The optional metadata inventory covers 1,980 files across the raw agency directories. Inventory presence is not a certificate that every file was substantively reviewed.

## Browser review

The local browser audit used axe-core against WCAG 2 A/AA, 2.1 AA and 2.2 AA rules, plus layout and request diagnostics. All 68 pages were checked at 390 px in light theme and 1280 px in dark theme. Representative home, evidence, action and source pages were also checked at 320, 768 and 1536 px; additional narrow-phone light-theme checks covered the library, policy and search pages.

Saved reports have no automated accessibility violations or horizontal page overflow. Clipped cells in horizontally scrollable tables require manual contrast interpretation; their text and background tokens were reviewed. The largest saved local layout-shift value after fixes is below 0.02. These are unthrottled local diagnostics, often with warm caches. They do not establish field LCP, INP or CLS performance.

Functional checks verified:

- Visible keyboard focus, skip-to-content, the mobile menu and Escape returning focus to its summary.
- Document agency/type/year filters, shareable filter URLs, empty results and reset.
- Agency timeline filtering and ATRS composition values, with ordinary HTML tables and source links.
- Search results, pagination, document-type filtering, query restoration after reload and the empty state for an absent phrase.
- The letter-copy status and copied text; no message was sent.
- Explicit petition loading and the persistent direct-link/failure fallback; no form was submitted.
- Source previews, full-resolution links, reviewed email text and download references.
- Home, policy, evidence, library, record, search and action pages with application scripts removed. The local audit probe still ran. Ordinary reading and the native mobile menu remained usable.

Visual review covered the desktop and phone homepage, agency facts, source exhibit, article/document/action page families, both color themes, the current one-page PDF and representative social artwork. Reduced-motion and print rules were inspected in source; the generated brief was rendered and visually inspected.

## Pension focus follow-up

The September 15 editorial follow-up centers the news feed, issue page, press summary and main evidence timeline on APERS and ATRS. Treasury remains a labeled governance comparison, with the combined financial measures in its background dossier. Original transaction data, source assets and proposal coverage are unchanged.

Full validation passes after the revision. All six changed article/evidence pages were rechecked at 390 px in light theme and 1280 px in dark theme with no automated accessibility violations or horizontal page overflow. Native Treasury measure expansion and the pension timeline filters were exercised. A separate output check confirms that the main campaign pages omit the combined figures, the main timeline contains only APERS and ATRS, and changed fragment targets resolve.

## Manual release review still required

Before approving publication, complete an actual assistive-technology pass (for example NVDA), browser zoom/text-enlargement checks and browser print pagination. The automation environment did not provide those complete user experiences. Review on a real mobile device is also valuable. These tasks are separate from the passing automated checks.

Joshua must apply and verify the [external petition package](petition-revision.md), then approve the concrete candidate. GitHub Pages settings, required checks and deployment remain the release steps in [release-guide.md](release-guide.md). HTTPS/domain and end-to-end production checks follow the actual deployment.

## Historical QR behavior

The preserved printed QR still encodes its existing provider URL. On September 15, a browser visit displayed the provider's “Open Link” interstitial; following that link reached `https://arpensions.org/`. A simple HTTP redirect check cannot verify this JavaScript journey and therefore does not pass `verify_assets.py --live`. Keep the original artwork intact, record this limitation, and use the new owned `/go/` QR in new materials.

Local logs, browser reports, archive hashes and release ZIPs are kept in the ignored `.qa/` directory. They are review artifacts, not public evidence sources.
