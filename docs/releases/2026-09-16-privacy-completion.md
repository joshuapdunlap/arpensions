# September 16 privacy completion: deployed and verified

The expanded audit release is recorded [separately](2026-09-16-audit-fixes.md). Continued visual review found a broker-account field on page 2 of the May confirmation that the first-page repair and OCR screen had missed. This release completes that redaction and adds an image-based regression guard. All 21 pages in the two affected confirmations were visually reviewed; see the [review scope and limitations](../audits/2026-09-16-privacy-follow-through.md).

Joshua's September 16 instruction to deploy and continue implementing confirmed fixes authorized this narrowly scoped completion. No unsettled policy or organizational disclosure was published with it.

- [PR #152](https://github.com/joshuapdunlap/arpensions/pull/152), merged at `2026-09-16T19:47:37Z`.
- Deployed commit: `1237d0cd6aeacd4ac68fa2247904610bd30fb8b9`.
- Approved source digest: `9f9e753e4c9b4801a91e68bad04f86f530128be625250c53b2d59a0d7aab9c10`.
- [Pages run 35142844123](https://github.com/joshuapdunlap/arpensions/actions/runs/35142844123) succeeded at `2026-09-16T19:50:16Z`.
- Deployed TAR SHA-256: `a6494346e9c19680b2e28e1d5f36eb132c8e2bf1d7810aacfd0135e4b19d4edb`.
- May confirmation SHA-256: `771c5a2cff1fdb485ac741cff1de361b9b57e8687512320cb98ef512a91368c1`.

## Verification

The branch and exact merged tree both passed the approval fingerprint gate. PR and main CI passed. Full validation passed 14 tests, zero Astro diagnostics, evidence/route/anchor checks and all asset checks. The new image-area check failed on the exposed page before the repair and passed after it.

Post-release HTTP verification matched all 69 HTML pages and 55 public assets, including the corrected May PDF, with zero failures. The custom missing-page response returned HTTP 404. Page checks cover visible text, titles, expected anchors and canonicals; asset checks cover PDFs, text downloads, RSS, sitemap and robots.

The deployed artifact is retained privately outside the repository. Older recovery artifacts contain superseded PDF derivatives. Any rollback must carry forward all redactions in `src/data/download-revisions.json`; it must not restore the exposed account fields. Prior distribution and Git history are not erased by this release.

The separate provenance/accessibility/drafting candidate is not part of this deployment and has its approval gate reset.
