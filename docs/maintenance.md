# Maintaining the site

The public site builds from this repository. Evidence-vault access is an optional authoring workflow, never a deployment dependency. Preserve original agency evidence and publish only reviewed derivatives.

## Set up and validate

Use Node.js 22 (minimum 22.12.0) and Python 3.13, matching GitHub workflows:

```sh
node --version
python --version
npm ci
python -m pip install -r requirements-dev.txt
python scripts/sync_campaign_content.py
npm run validate
npm run preview
```

Use an isolated Python environment if needed and ensure `python` resolves to it. `npm ci` honors `package-lock.json`; do not substitute an unreviewed dependency upgrade.

`npm run validate` checks shared campaign copy, TypeScript tests, Astro diagnostics and the build. The build generates `dist/`, restores compatibility output, indexes Pagefind, audits the site and verifies public assets. The separate shared-copy check is also run by CI. Investigate failures rather than bypassing them.

Use `npm run dev` for editing. Use the built preview for final search, generated feeds, links and downloads. The terminal prints the address. Never edit `dist/`, `.astro/` or Pagefind output as source.

## Edit public content

Public Markdown lives in `src/content/pages/`. Frontmatter declares title, description, permalink, template, source IDs and string dates, such as `reviewedAt: '2026-09-15'`. The schema is in `src/content.config.ts`.

Keep public URLs stable. When changing headings or routes, review `src/data/legacy-anchors.json` and test old links. Make the description and opening paragraph complementary.

For a factual change:

1. Read the strongest underlying record and its exact page, row or message locator.
2. Update the source entry and relevant financial records in `src/data/investigation.json`.
3. Update the claim, source IDs, scope, interpretation and boundary in `src/data/publication-matrix.json`.
4. Reconcile affected pages, agency summaries, dated corrections, briefs and shared campaign materials.
5. Run synchronization and validation, then inspect the rendered pages and source exhibits.

An absence within a reviewed production is not proof that a record never existed. Preserve attribution to schedules, participants and sellers. The policy remains a campaign proposal until evidence establishes a different status.

## Keep the financial model honest

`financialRecords` separates authorization, funding, purchase, holding, cancellation, processing and derived residual. Each amount has a basis, account scope and source IDs. An unestablished effective date is null, not a filename or production date. Sources separately label document/message/transaction/account/report dates, with an optional received date. Observations of the same security share a `securityId`; a security inside manager funding has a `parentFundingId`. Aggregate reports and their earlier transactions or statements use `overlapsRecordIds` to prevent counting the same positions twice.

September baseline boundaries:

- APERS's $25 million is a dated custody amount; allocation among APERS-administered systems is unresolved.
- ATRS's $9.9 million bond is inside its $50 million funding. Purchase and later holding are observations of the same asset.
- Treasury's $50 million is conditional on a projected $5 million maturity reducing a historical $55 million statement and no other transactions. The projection does not establish receipt or later holdings. Its separate $10 million processing payment remains excluded.
- The $84.9 million historical calculation and $125 million mixed-stage illustration combine different dates and share the Treasury assumption. Neither is a confirmed floor or current holding. Derived residuals are ineligible for direct-evidence measures; historical calculations require their assumption.

Never sum all financial records indiscriminately. Follow explicit inclusion rules in the financial code and tests. Separate par from value including accrued income. Source percentages may contain rounding error; preserve values and label the display basis.

## Synchronize shared campaign copy

After an approved edit to `src/data/campaign.json`, synchronize its letter block and text download:

```sh
python scripts/sync_campaign_content.py --write
python scripts/sync_campaign_content.py
npm run validate
```

The write command changes the marked block in `src/content/pages/take-action.md` and the dated text download in `public/assets/documents/`. Review both. Do not maintain the generated letter block as an independent version.

Optional PDF and campaign-artwork generation requires additional dependencies:

```sh
python -m pip install -r requirements-authoring.txt
npx astro build
python scripts/postbuild.py
python scripts/generate_campaign_assets.py
npm run validate
```

Always use this order: build current HTML, generate the public assets, then validate the final build. The generator reads current HTML titles for 65 page-specific social cards. Input fingerprints and rendered-title comparisons reject stale artifacts. Text derivatives use LF line endings so Git and Linux CI preserve their hashes.

Run only after reviewing structured copy and the generator's output paths. Inspect brief layout, text, links and QR destination. It writes files in `public/`; do not run it over a historical publication that must remain immutable. For a new publication date, update date-dependent filenames and metadata deliberately. Generated files do not establish external publication.

## Preserve historical downloads and evidence

For substantive evidence updates, preserve historical public artifacts and publish a new dated version. A confirmed privacy exposure is an explicit exception: retain the original privately, remove the sensitive pixels and hidden text, verify the replacement, and record the original fixture hash, replacement hash, date and reason in `src/data/download-revisions.json`. Serve the reviewed replacement at the existing URL and describe it in Corrections and the download catalog. Do not rewrite the original fixture hash or claim that previously distributed copies were erased.

`src/data/download-catalog.json` must enumerate every public PDF and TXT exactly once, with its category, source record or explicit provenance limits, and stable context anchor. `src/data/public-assets.json` records public-file hashes, original locators, treatments, previews, selected transcripts and checked HTML tables. The manual authoring script retains separately reviewed email excerpts and table metadata; it is not a complete reconstruction of every public artifact from the raw corpus. Review these together. Distinguish quoted source text, omissions and commentary. Plain-text email excerpts are not original agency PDFs. Evidence images must be literal rendered pages or rectangular crops, with explanatory captions outside them.

Remove sensitive information from both published pixels and hidden layers. Never publish requester identity material, account identifiers or private contact fields. Asset verification does not replace substantive source and visual review.

## Optional local inventory comparison

With authorized local-vault access:

```sh
npm run evidence:delta -- --wiki "<local-evidence-vault>"
```

Alternatively supply `EVIDENCE_ROOT`. The script writes `.qa/evidence-delta.json` and identifies potentially affected sources and claims. The tracked `docs/evidence-inventory-snapshot.json` stores hashed relative paths and metadata. It is not a content-hash audit or proof of completeness or review.

After deliberate review, update the snapshot if appropriate:

```sh
npm run evidence:delta -- --wiki "<local-evidence-vault>" --snapshot
```

The local report can contain filenames. Keep `.qa/` private and out of public assets. Inventory changes do not authorize automatic ingestion, revised claims or publication.

## Optional source-exhibit authoring

`scripts/publish_sources.py` is a manual allowlisted workflow. Read its source selections and masking instructions first. It needs Python dependencies plus Tesseract and LibreOffice for native spreadsheet exports. Prepare the reviewed exports in `.qa/source-work/single/` as the script expects.

```sh
python scripts/publish_sources.py --wiki "<local-evidence-vault>" --reviewed
```

`--reviewed` is a maintainer assertion, not an automatic review. The script writes public derivatives, previews and metadata; ordinary builds never call it. Export from working copies, preserve original bytes and cell values, inspect each page/transcript, then run validation. Reconcile substantive changes through the claim matrix and public copy.

## Hand off a candidate

Record changed files, source checks, validation and remaining browser review. Inspect mobile widths, both themes, keyboard focus, reduced motion, no-JavaScript reading, search, print and downloads. Automated success alone does not establish completed browser QA or accessibility.

Follow [the release guide](release-guide.md). Source changes after approval require a new digest and approval. External correspondence, petition changes and publication require Joshua’s authorization. Keep historical deployment evidence separate from approval of a changed candidate.
