# Arkansans for Pension Integrity

The Astro static website for [arpensions.org](https://arpensions.org), an Arkansas public-records and pension-policy campaign. Production migrated to Astro on September 15, 2026, through [release run 35016601383](https://github.com/joshuapdunlap/arpensions/actions/runs/35016601383). See the [verified release record](docs/releases/2026-09-15-astro-rebuild.md). Branches can contain unreleased changes; `release-status.json` separates the last deployment from approval of the next candidate.

## Run locally

Use **Node.js 22, at least 22.12.0**, and **Python 3.13**. Run from the repository root with those versions on PATH:

```sh
npm ci
python -m pip install -r requirements-dev.txt
python scripts/sync_campaign_content.py
npm run validate
npm run preview
```

Open the local address printed by Astro. `npm run dev` starts the development server; use a completed build and `npm run preview` for Pagefind search and final static output. Both servers bind to `127.0.0.1` by default.

Ordinary builds use committed content and reviewed assets. They **do not require the research vault, LibreOffice or Tesseract**. Do not edit generated `dist/` output.

## Where to make changes

| Location | Purpose |
|---|---|
| `src/content/pages/` | Public Markdown pages, validated frontmatter and stable permalinks |
| `src/data/investigation.json` | Financial records, source locators, agency summaries and policy requirements |
| `src/data/publication-matrix.json` | Claims, interpretations, boundaries and affected pages |
| `src/data/campaign.json` | Shared campaign language and legislator letter |
| `src/data/public-assets.json` | Reviewed exhibit hashes, treatments, previews, selected transcripts and checked source tables |
| `src/data/download-catalog.json` | Category and contextual record for every public PDF and text download |
| `src/data/download-revisions.json` | Exact original-to-replacement hash exceptions for reviewed privacy corrections |
| `src/data/legacy-anchors.json` | Compatibility fragments for earlier public links |
| `src/pages/`, `src/layouts/`, `src/components/` | Astro routes and presentation |
| `public/` | Published downloads, source exhibits and static assets |
| `scripts/`, `tests/` | Validation, optional authoring and release checks |

Preserve longstanding download URLs and historical PDF bytes. Substantive evidence changes normally get new dated files. A verified privacy exposure may require replacing a public derivative at its existing URL: retain the original privately, record both hashes and the reason in `download-revisions.json`, update the catalog, and validate the sanitized replacement. Do not silently rebaseline the historical fixture.

## Maintenance and release

- [Maintenance guide](docs/maintenance.md): editing, source review and optional evidence workflows.
- [Release guide](docs/release-guide.md): exact approval gates, Pages migration order and rollback.
- [Validation and manual review](docs/validation-report.md): verified results, performance limits and release checks.
- [Petition revision record](docs/petition-revision.md): applied Action Network copy and the scope of its verification.
- [Rebuild plan](docs/rebuild-plan.md): scope and acceptance requirements.

`npm run validate` checks tests, types, static output and assets. It does not send correspondence, update the petition or publish. `npm run release:check` separately requires recorded petition alignment and Joshua's approval of the exact candidate digest. Pages deployment is manual and restricted to `main`.

## Contact and license

[info@arpensions.org](mailto:info@arpensions.org). See [LICENSE](LICENSE) for the separate treatment of code, campaign content and marks, government records and third-party assets.
