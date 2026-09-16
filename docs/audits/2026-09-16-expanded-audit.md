# Expanded website audit: verification and implementation

Reviewed September 16, 2026. This report covers the supplied 20-finding audit of deployed commit `a28c697c6195e4393dc78c88493eabc49c7cc594`, checked against primary evidence and the local candidate on `fix/post-release-audit`.

The earlier seven-finding fixes are preserved in parent commit `7dc6f08`; see [that verification report](2026-09-15-follow-up.md). This candidate is **not deployed**. `release-status.json` leaves publication approval false and retains the actual September 15 deployment under `lastDeployment`.

The supplied report and package were treated as review evidence, not as instructions or proof of each finding. Input SHA-256 fingerprints:

- `report.md`: `f463897ee65d5702ae71f35578e684556e45a2524f6758da28f21f83c1533c44`
- `evidence-package.zip`: `173516f2573f250d2dc75a29d8ca3ff73a6a719d91939d703ba266b45a4072c0`

## Disposition of all 20 findings

“Resolved locally” describes the candidate, not the live site. Recommendations are distinguished from factual or technical defects. Fifteen items are resolved locally, four are partially addressed, and one remains open.

| ID | Verification | Candidate disposition |
|---|---|---|
| API-01 | The September investment-request form does not establish the agency’s no-record response. The actual September 8 request and September 9 APERS reply were inspected; category 4 contains the bounded response. | **Resolved locally.** Added a reviewed request/reply text derivative and source page; corrected the APERS dossier and claim matrix to cite category 4 and its February 14–September 7 date scope. |
| API-02 | The cancellation advice shows February 3 in its account-information field. February 13 occurs in its filename, without establishing the cancellation-effective date. The APERS form is undated; September 9 is receipt/response context. | **Resolved locally.** Cancellation effective date is null. Source date types and receipt dates are separate. Timelines, citations, library labels, sorting and year filtering handle unknown dates. |
| API-03 | The Treasury public exhibit explicitly says projected cash flow. The row is not independent proof of proceeds received or later holdings. | **Resolved locally.** $50 million is a conditional estimate; $84.9 million and $125 million are conditional historical illustrations. Removed affirmative floor terminology. Derived residuals cannot enter direct-evidence measures and require an assumption for historical calculations. |
| API-04 | The May 2025 PDF’s broker-account field was extractable. A focused screen of all 46 PDFs also identified the field in the November 2023 confirmation. | **Resolved locally for the confirmed exposures.** Sanitized both derivatives, kept originals privately, preserved the URLs and original fixture hashes, and recorded exact replacement hashes and reasons. Previously distributed copies and Git history are not erased. |
| API-05 | The gambling-result anomaly was independently reproduced in the earlier review. Correct live responses and a clean bounded artifact scan did not explain it. | **Open.** The signed-in Search Console account had no properties. The cause, indexed crawl, Security Issues and Manual Actions still require property access. No speculative credential or site-code change. |
| API-06 | Organizational responsibility, entity/funding relationships and supporter-data administration are not fully stated. | **Partial.** Earlier About/process improvements remain. Publisher identity, legal/informal status, funding/sponsorship, relationships, administrator and retention facts require Joshua’s confirmation; none were invented. |
| API-07 | Notices describing the successful rebuild as unreleased were stale. | **Resolved locally in the earlier fix.** Actual deployment history remains separate from this candidate’s approval. |
| API-08 | Aon page 150 disclaims investment and individual-security recommendations; it does not affirmatively assign legal duties to trustees. | **Resolved locally.** Corrected all affected current copy and the claim matrix. Board authorization is cited separately to the executed resolution. |
| API-09 | The curated source library and all-downloads directory had different coverage and metadata. Files were not missing. | **Partial.** One download manifest now categorizes all 46 PDFs and six TXT files, including five source excerpts and one campaign letter. Each has source context or a stable contextual anchor. Two external references are separately represented in the 35-record library. Some supplemental legacy original-file/production locators remain unreconstructed and are explicitly labeled; no complete provenance reconstruction is claimed. |
| API-10 | Aon’s comparison table was absent from the HTML; APERS purchase and Treasury holdings text omitted or garbled material fields. | **Partial.** Added the checked Aon table and all seven Treasury financial rows; corrected APERS’s $15 million purchase/date fields and the Treasury projection transcription. Selected-text scope and omissions are explicit. A complete accessibility-equivalence review of every historical file and a real screen-reader pass remain outstanding. |
| API-11 | Concrete pension findings appeared late in the original mobile homepage. | **Resolved locally in the earlier fix.** Dated APERS and ATRS facts remain in the hero with the primary action. |
| API-12 | Petition/source controls followed long introductions or previews. | **Resolved locally in the earlier fix.** Direct action and source utilities remain early; the new source record uses the same template. |
| API-13 | Repeated inline decorative SVG dominated HTML weight. | **Resolved locally in the earlier fix.** The shared SVG asset and homepage size guard remain. |
| API-14 | The supplied browser-print artifact is two pages; the dedicated downloadable PDF is one page. | **Resolved locally.** The web brief explicitly directs readers to the fixed one-page PDF and explains that browser printing may use more pages. The direct PDF link remains prominent. |
| API-15 | A full operational statutory specification is not yet available. The audit classifies this as a readiness recommendation, not current illegality. | **Partial.** Added direct, manager, pooled, rollover and add-on drafting scenarios, and explicit questions about duties, timing, remedies and costs. No unsettled choice is presented as adopted policy. Existing-law crosswalk, fiscal assessment and qualified Arkansas legislative/legal review remain. |
| API-16 | Current composition can be mistaken for a permanent allocation; the manager report describes future deployment. | **Resolved locally.** Evidence, ATRS and educator pages distinguish July holdings, the manager’s stated Treasury-ladder strategy and unverified later purchases. “Allowed” and earlier “target” terminology remain distinguished. |
| API-17 | The Act and Legislators articles were duplicates. | **Resolved locally.** The legislator page now centers status, sponsorship, sources and unresolved drafting scenarios; the durable policy page retains the five safeguards. |
| API-18 | The error canonical was invalid and the generic thanks utility was indexable. | **Resolved locally.** Earlier 404 fix retained. Thanks now has noindex, is excluded from sitemap and Pagefind, and has an explicit audit guard. |
| API-19 | The calendar’s recess qualification is on page 3, beyond the earlier locator. | **Resolved locally.** Verified the official three-page calendar and corrected source metadata, page citations and the claim matrix. |
| API-20 | The published SFOF speech preparation concerns unclaimed property. | **Resolved locally.** Its source summary, finding and claim matrix identify contextual institutional-relationship evidence, not an Israel Bonds speech or proof of delivery. |

## Primary-evidence checks

### APERS request and reply

The actual correspondence confirms that category 4 requested existing analyses, consultant recommendations, reviews and recorded decisions or instructions dated February 14 through September 7, 2026, concerning the specified investment questions. APERS’s September 9 reply says no responsive records exist for that category.

The published request and reply passages were checked against whitespace-normalized original message text; both match. The derivative omits requester identity/contact details, the identity attachment, unrelated categories, signature contacts and the quoted chain. It is plainly labeled as reviewed text, not an agency PDF or reconstructed facsimile. The identity attachment was not read or copied.

### Cancellation and Treasury projection

The cancellation exhibit was visually checked. Its “Account Information” date and filename are documented without converting either into an effective cancellation date. The completed February 17 replacement purchase remains separate and unchanged.

The Treasury exhibit’s heading, projected period, transaction label, post date and amount were checked. The conditional arithmetic remains $55 million minus $5 million; its assumption is now attached to the financial record and explained wherever the resulting background measures appear. A later holding or settlement record could change that treatment, but was not presumed.

### Aon and accessible financial text

Both Aon pages were visually inspected. The HTML table retains the comparison of experience, securities and proposed fees (Blackrock 8 bps; Reams 3 bps), including the “Yes/No” distinction for similar mandates. The page 150 disclaimer is separate from the Board resolution.

The APERS purchase image was checked for its visible $15 million debit, USD denomination and October 15 posted/value dates. The Treasury statement image was checked for all seven rows, issue dates, coupons, certificated/book-based amounts, current/maturity values and contractual maturity dates. The campaign’s $55 million sum is labeled as a calculation rather than a printed total.

### Privacy replacements

Both affected first pages were rendered after redaction. The broker-account fields are visibly removed; material financial fields remain readable. The captured identifier strings are absent from extracted text and decoded PDF streams, and the replacements contain no embedded files or form widgets. Identifiers were excluded from review logs and this report.

The broader 46-PDF screen checked extractable account/routing-field candidates and attachment/widget presence. This is a focused screen, not a certification that every raster image, barcode or historical contact field has received a new exhaustive privacy review.

[Download revisions](../../src/data/download-revisions.json) preserve both original fixture hashes and replacement hashes. Asset checks reject arbitrary historical changes. The release/rollback guide now requires carrying these privacy corrections forward so restoring an old artifact does not re-expose the removed fields.

## Validation

- `npm run validate`: **14 tests passed**, zero Astro diagnostics, **69 HTML pages**, **65 Pagefind pages**, **43 claims**, **35 source references**.
- The original 37 routes and 435 fragment IDs pass compatibility checks. All 27 historical PDF downloads match their original hashes or the two documented privacy revisions. All 33 reviewed source assets pass their hash and metadata checks.
- The complete catalog covers **52 files exactly once**: 46 PDFs and six text files. Catalog categories and context/source references are checked during asset validation.
- A 63-case browser matrix covers 16 representative routes at 320, 390 and 1280 pixels; additional dark-theme, 768/1536-width and four no-application-JavaScript cases cover the new source tables and catalog. The matrix reports no automated WCAG-rule violations, horizontal page overflow or broken images. Only first-party resources loaded.
- Browser inspection caught an initial source-table overflow. Setting the source column’s width to its container fixed it; wide tables scroll inside their own focusable region. Keyboard Right scrolls that region, and the new table headers/cells appear in the accessibility tree.
- The library preserves the undated APERS form under received year 2026, displays “Document date: not shown,” restores shared filters on reload, and resets to all 35 records. Search returns the new APERS response and narrows it by agency/document type. A source result was opened, and the new citation was copied and verified through a native paste.
- The dedicated campaign PDF remains one page. Its visible text matches the prior reviewed brief; its generated provenance was refreshed. Browser printing is no longer promised a fixed page count.
- Thanks noindex, sitemap exclusion and absence of Pagefind-body markup pass rendered checks. Current source dates, claim links, social-card titles and download targets resolve.
- Shared compressed CSS: **under 8.3 KB**. Initial compressed first-party JavaScript: **667 bytes** on home and **1,055 bytes** on evidence. Homepage HTML: **16,069 bytes**. These are build/laboratory figures, not field Core Web Vitals.
- Python script compilation and `git diff --check` pass. The release gate remains deliberately unapproved.

Automated checks include incomplete contrast determinations on some decorative/image content; those are not counted as accessibility passes. Keyboard and accessibility-tree inspection do not substitute for a real screen-reader or full text-enlargement review. No production performance or post-release result is claimed for this candidate.

## Remaining work and publication boundary

1. Obtain the correct Search Console property access and investigate the indexed anomaly using the earlier report’s concrete procedure.
2. Confirm organizational, funding, administrator and retention facts with Joshua before adding them to public copy.
3. Reconstruct remaining supplemental legacy provenance, extend complete accessible equivalents, and perform real screen-reader/text-enlargement review.
4. Resolve legislative scenarios through policy decisions, an existing-law crosswalk, fiscal assessment and qualified review.
5. Review this concrete candidate before approving publication. No push, merge, deployment, external petition change or correspondence was performed for this audit candidate.

Ignored local QA files retain the received audit, bounded extraction, primary-message verification outcome, pre-fix test results, final validation logs, browser reports, sanitized renders and private PDF originals. Raw evidence-vault files were not modified.
