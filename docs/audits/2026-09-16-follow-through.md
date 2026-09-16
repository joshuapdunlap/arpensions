# Audit follow-through after deployment

## Status

The expanded audit corrections and subsequent confirmation privacy completion are live. The latest verified deployment is commit `1237d0c`; see the [privacy completion release record](../releases/2026-09-16-privacy-completion.md).

This separate candidate implements source-provenance and readable-context improvements, fixes enlarged-text overflow, and prepares a legislative working paper. It has not been deployed. The publication gate remains reset so the earlier release's approval cannot silently apply to changed content or code.

## Confirmed fixes implemented

### API-09: the legacy provenance gap is reconstructed

All 14 supplemental historical PDFs and both alternate extracts now have a checked source file, production date, exact physical-page mapping, original-file fingerprint and public-derivative fingerprint. All existing URLs and contextual anchors remain unchanged.

The review matched every supplemental page to the corresponding source-page rendering at 72 dpi, apart from the three documented account-field redactions across the two confirmation PDFs. The two alternate extracts have changed page canvases and campaign-added footers; their content and locators were visually checked, without claiming pixel identity. The original research files were not modified.

The public catalog now supplies:

- Clear display titles and event-date explanations, including the unsigned ATRS packet copy versus the executed resolution.
- The original source filename and physical pages, with production and review dates.
- Separate original and public SHA-256 fingerprints and a description of how the match was checked.
- Readable historical context and explicit limits on what each record proves.

The Berman/Lowery download URL retains its old filename for compatibility, but the display title now describes the May 2023 correspondence without using the filename to establish a death chronology. The news clipping is dated from its October 28, 2023 article header, rather than the date in the later compilation filename. Invitation, nomination, seller account, internal communications preparation and completed transaction records retain their different meanings.

`src/data/legacy-context.json` holds the reviewed context for each legacy catalog ID; `src/data/download-catalog.json` supplies its immutable public URL and current artifact fingerprint. Their only new public publication surface is the corresponding entry on `/assets/documents/`. These historical summaries do not enter the site's financial aggregation model or change its pension totals.

### API-10: more readable evidence, plus an enlarged-text fix

All 16 entries now have a readable, reviewed summary. Two semantic HTML tables preserve the face amounts, CUSIPs, coupons, issue dates and maturities of the three securities in the May 2025 and November 2023 Treasury confirmations. Each table identifies its public PDF page. Treasury remains historical comparison material, outside the pension proposal.

The November 2023 packet's outgoing payment report is explicitly labeled `Processing By Bank`; it is not promoted to settled-payment proof. The confirmation and the payment report remain different documents. The May packet's two $10 million confirmations are identified separately, and their sum is labeled as a calculation.

These are selected fields and summaries, **not complete transcriptions of all historical files**. Account, address, signature, repeated correspondence and other administrative content is not represented as fully transcribed. The source PDFs remain available.

A local 200% text-size probe exposed page overflow on 390-pixel home, catalog and action pages. Long text now wraps, the brand can shrink and wrap without displacing header controls, and tables retain ordinary word boundaries. The corrected pages passed the same probe; the home page also passed at 320 pixels. The probe changes computed text sizes only in the local audit server. It is absent from the production build.

### API-15: operational drafting work prepared

The [statutory crosswalk and operational working paper](../policy/2026-09-16-operational-crosswalk.md) includes inspected primary authorities, explicit version limits, ten transaction scenarios, recommended responsibility and publication rules, unresolved enforcement/transition choices, and a workload/fiscal worksheet.

The crosswalk accounts for Act 419's updated delegation/procurement references. It does not represent the historical session laws as a complete current code. The cost example is arithmetic using invented assumptions, not an agency estimate or official fiscal note. No unsettled policy recommendation was added to public campaign copy.

## Verification

- Full `npm run validate`: 14 tests; zero Astro errors, warnings or hints; 69 built HTML pages; 43 central claims and 35 curated source references.
- Historical route, fragment, download and reviewed-source hash checks remain intact. All 52 public PDF/TXT downloads have one catalog entry. All 16 legacy context records have a valid original fingerprint, page-count mapping and matching reviewed public fingerprint.
- A deliberate private test changed a legacy artifact fingerprint. The validator rejected the mismatch; the exact reviewed file was then restored.
- Expanded catalog testing covered 320, 390, 768, 1280 and 1536 pixels in light and dark themes. No automated WCAG-rule violations or page overflow were reported. Narrow-table contrast checks include incomplete results for horizontally clipped cells; those are not claimed as automated passes. The same cells passed at wider widths.
- After the global wrapping adjustment, 21 responsive checks covered home, catalog, Aon source, action, policy, document library and search at 320, 390 and 1280 pixels: no page overflow, broken images or automated WCAG-rule violations.
- The native disclosure opens by keyboard, and the labeled table region scrolls with the Right arrow. The catalog remains readable with application scripts omitted. Its native disclosure and ordinary download links do not depend on JavaScript.
- The 200% text probe covered five key routes at desktop width and home/catalog/action at phone width. The confirmed phone overflow was repaired and retested. This is a local text-resize simulation, not a browser-setting or screen-reader certification.
- Campaign assets were regenerated against the changed Astro inputs. The one-page brief has exactly the same visible text and rendered pixels at 144 dpi as the previously reviewed brief; PDF packaging bytes differ. Social-card and QR checks pass.

## Remaining work, with concrete dependencies

| Audit item | Remaining dependency / next action |
|---|---|
| API-05: indexed gambling anomaly | Correct Search Console property access. Inspect URL Inspection's indexed crawl, Security Issues, Manual Actions and relevant ownership/settings before attributing the cause. The signed-in account previously showed no properties; clean live files do not explain the search result. |
| API-06: organizational disclosure | Joshua must confirm the public lead/entity status, funding, organizational relationships and supporter-data administrator/retention practices. The facts cannot be inferred from a domain or repository account. |
| API-10: full accessible equivalents | Continue complete historical transcriptions where appropriate; review specialized source content and omissions. A real assistive-technology pass remains required. Native screen-reader control is unavailable in this environment. Browser zoom keypresses did not produce a measurable zoom change, so a real browser 200%/400% zoom pass is also unverified. Narrow reflow and simulated doubled text were tested separately. |
| API-15: filing readiness | Complete current plan-specific codification/rule checks, settle the scenario choices, obtain measured workload/fee inputs and qualified Arkansas legislative/legal review. The working paper alone does not satisfy these steps. |

API-09 is resolved in this local candidate. Overall, 16 of the original 20 findings have implemented resolutions, three remain partially addressed, and one remains open. Deployment status is stated separately: the new provenance, readable context and text-wrapping changes are local, while the preceding audit and privacy fixes are live.

No external petition changes, correspondence, account creation, DNS changes or Search Console ownership changes accompanied this follow-through. Ignored local QA holds the source-matching report, browser reports, privacy inspection records and validation logs. The public repository contains reviewed derivatives and metadata, not local evidence-vault paths or requester identity material.
