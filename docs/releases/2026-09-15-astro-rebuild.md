# September 15, 2026: Astro production release

## Verified deployment

- Public site: https://arpensions.org/
- Deployed commit: `a28c697c6195e4393dc78c88493eabc49c7cc594`.
- [Merged PR #148](https://github.com/joshuapdunlap/arpensions/pull/148).
- [Release run 35016601383](https://github.com/joshuapdunlap/arpensions/actions/runs/35016601383): successful, last updated September 15, 2026 at 19:58:33 UTC.
- Pages artifact: `10416475008`; ZIP digest `d470e58731dae33e25721d7487b9770db87aaca2a61ecbdbcaa1e5b1dab4d85b`.
- Preserved deployment TAR SHA-256: `cb46ee3f1caabe8e52adc9838217b12e5981c4519b2bdd6aa98992d61ececcac`.
- Approved source digest: `fc6e4b1faccef3d105f5c8ffa612dd40f6bbb1d51399388266d30962c3c0dbda`.

Joshua approved the candidate and explicitly requested deployment. Pages was switched from legacy branch publishing to Actions before the reviewed candidate was merged. The domain and HTTPS settings were preserved. The local main checkout was fast-forwarded to the deployed commit.

## Distinct verification steps

| Step | Evidence and limit |
|---|---|
| Source approval | Joshua approved the reviewed source candidate; the release workflow matched its fingerprint. This approval does not extend to later changed source. |
| Petition alignment | On Joshua’s explicit instruction, Codex applied the prepared revision and read back public copy and saved administrator settings at 19:42 UTC. Defaults were disclosed. No signature or test email was submitted, so receipt/email delivery were not verified. |
| Build | 13 tests, Astro diagnostics, static publication audit and asset audit passed locally and on GitHub. |
| Deployment | The GitHub Pages workflow successfully published the main commit above. |
| Independent live checks | Completed at 20:03 UTC: 68 HTML pages matched expected text/titles and anchors; 46 PDFs plus three feed/robots assets matched; the custom missing-page response was 404; HTTP and www redirected to canonical HTTPS. |
| Browser smoke checks | 390 and 1280 px: both themes, mobile menu, visible homepage action, search and its filters, document-library filters, source previews, and live petition loading. No console warning/error was observed in that session. |

The first main-branch audit run was superseded by a delayed PR run. Its second attempt passed. This was operational release verification, not a complete security, accessibility, or field Core Web Vitals certification. A later audit identified improvements to mobile control placement and page weight; those findings do not change what these checks actually established.

## Recovery

The pre-migration source commit is `2050a39b4dbb44f19075586aadafabc6890cd1fe`. Its preserved static archive SHA-256 is `f5a775f2dc19556c961b4c90753901cae17aa52e3fa84d19af456b4b697bb802`. The reviewed Astro archive and actual deployed TAR are preserved outside the implementation worktree and CI retention.

Follow the [release and rollback guide](../release-guide.md). Never re-enable legacy branch publishing over an Astro-only source tree. Preserve the corrected external petition when considering a content rollback.
