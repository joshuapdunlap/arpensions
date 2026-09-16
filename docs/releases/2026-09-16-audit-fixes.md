# September 16, 2026: audit corrections release

## Verified deployment

- Public site: https://arpensions.org/
- Deployed commit: `e1360b8f4414926febc277ea6d6cef8112f4020e`.
- [Merged PR #151](https://github.com/joshuapdunlap/arpensions/pull/151).
- [Release run 35140199770](https://github.com/joshuapdunlap/arpensions/actions/runs/35140199770): successful, last updated September 16, 2026 at 19:23:48 UTC.
- Approved source digest: `1b46a4711191b4a08971a41d2e4cd2821d0d6e2f6be0338ecb454d2471f6ffaa`.
- Pages artifact: `10464532626`; ZIP SHA-256 `571e6fd755bf8662cad177afa99704bafd2499a4d5a2f495c67e5c5df80b8e52`.
- Preserved deployment TAR SHA-256: `07868f560c4eabea3ee036db892a57adf7fbbc99fb5f8f16c6606026069ecd40`.
- Reviewed local static ZIP SHA-256: `c312cea8a158eabaa9d8bf26d31dd5da06ec8edeb309ce45b0997af10396a573`.

Joshua explicitly instructed: "Deploy then proceed with the remaining work." The reviewed candidate was integrated only after fresh local validation and passing PR checks. The resulting main commit passed its own audit and matched the approved source digest. GitHub Pages remains Actions-built at the existing custom domain with HTTPS enforced. The main checkout was fast-forwarded to the deployed commit.

## Verification and limits

- Fresh local validation: 14 tests, zero Astro diagnostics, 69 HTML pages, 43 claims and 35 source references. Historical routes, anchors, source assets and download hashes passed.
- PR and main audits passed; the separate release workflow passed its approval gate, validation and deployment.
- Independent HTTPS checks completed at 19:24:27 UTC: all 69 HTML pages matched expected visible text, titles, anchors and canonical metadata; 46 PDFs, six document TXT files and three feed/robots assets matched expected content. The custom missing-page response returned 404. No failures.
- Live hashes matched both corrected purchase PDFs and the new APERS September response text. Recovery archives are retained outside the worktree and CI retention.
- Browser smoke review confirmed the primary mobile action is visible without page overflow, theme switching, navigation, search and document access. No petition signature or test email was submitted.

The source-level and live checks do not certify universal accessibility, field Core Web Vitals, Search Console health or delivery of third-party petition messages. The full [audit disposition](../audits/2026-09-16-expanded-audit.md) preserves those distinctions.

## Privacy and recovery

The two historical purchase PDFs retain their URLs with exactly documented privacy revisions. The May 2025 replacement SHA-256 is `7552ba6896690f7f5cd9b880f4ccbbf572bb104f99e2c617dd492801de59d5c4`; the November 2023 replacement is `5c077bc09f1c9a2c8fd2767936ca495e6cfb3bad37b09c724c63675890d94561`. Prior distributed copies and Git history are not erased.

The [September 15 recovery record](2026-09-15-astro-rebuild.md) is preserved. Follow the [release and rollback guide](../release-guide.md): carry the two privacy corrections into any rollback candidate, and never republish old account fields by blindly restoring an earlier archive.

## Continuing work

Search Console access and organizational facts remain requested. Supplemental historical provenance, accessible equivalents and the legislative drafting crosswalk continue on a separate local branch. The new candidate approval fields are reset; the successful deployment remains recorded under `lastDeployment`.
