# Release and rollback

Production migrated from Jekyll to Astro on September 15, 2026. GitHub Pages now builds through Actions, with the existing custom domain and HTTPS. The [verified release record](releases/2026-09-15-astro-rebuild.md) documents the deployed commit, petition verification, and live smoke checks. The transition steps below remain a historical migration and rollback reference; they are not a statement that the site is still awaiting its first deployment.

For subsequent releases, verify current remote state, validate and review the changed candidate, record Joshua’s approval of its exact digest, then use the existing Actions workflow. `release-status.json` keeps `lastDeployment` as history while top-level approval fields apply only to the next candidate. A successful build alone does not update that deployment history.

## Pre-migration state: historical reference

The read-only GitHub inspection established:

- Base `main`: `2050a39b4dbb44f19075586aadafabc6890cd1fe`.
- GitHub Pages uses legacy **main / root** branch publishing, with HTTPS at **arpensions.org**.
- No branch protections were present in the inspected configuration.
- PR **#139** upgrades checkout v4 to v7; PR **#147** upgrades setup-python v5 to v7. The rebuild replaces those workflows with pinned v7 revisions, so the earlier changes are superseded within this candidate. Joshua must decide their disposition; do not merge or close them automatically.

Verify branch, Pages, domain and PR state before acting because the snapshot can change. Adding branch protections or required environment reviewers is a separate settings decision for Joshua.

## Preserve recovery materials

Local package paths:

- `.qa/legacy-site-2050a39.zip`: preserved legacy site artifact.
- `.qa/arpensions-astro-release-2026-09-15.zip`: reviewed Astro static candidate.

Confirm both archives exist, inspect their contents and record SHA-256 hashes before release. A documented path does not prove an archive was created. Keep copies outside the disposable worktree and CI artifact retention. PowerShell can calculate each hash with `Get-FileHash -Algorithm SHA256 -LiteralPath <path>`.

Preserve the legacy source commit as well as the built artifact. Record Pages source, custom domain, HTTPS and relevant environment configuration. Rollback may require both content and hosting configuration; a source archive alone is not the deployed artifact.

## Build and review

Use Node 22, minimum 22.12.0, and Python 3.13:

```sh
npm ci
python -m pip install -r requirements-dev.txt
python scripts/sync_campaign_content.py
npm run validate
npm run preview
```

Read [the validation report](validation-report.md), then review the actual static candidate. Record browser checks at mobile 320/390/768 and desktop 1280/1536 widths, in both themes. Include keyboard focus, reduced motion, no-JavaScript reading, search, source filters/previews, print, action fallbacks and old routes/fragments. Check PDFs, text downloads, metadata, sitemap and RSS. Resolve material failures before approval.

For a new dated campaign brief, first update `src/data/campaign.json`, current download links and the download catalog. Preserve earlier dated files and label them historical. With the authoring dependencies installed, run `python scripts/generate_campaign_assets.py --brief-only` to create the new PDF and letter before the catalog build reads them; then run `npm exec -- astro build`, the full `python scripts/generate_campaign_assets.py`, and `npm run validate`. The full generator refreshes social cards and provenance. Render and inspect the new PDF before publication. Ordinary CI builds continue to use the checked-in approved assets.

CI uploads `arpensions-static-candidate` with 30-day retention. CI artifacts and local ZIPs support review; neither establishes publication. The build needs no local evidence vault.

## Joshua aligns the external petition

Joshua applies the description, letter, subscription disclosure and confirmation staged in [petition-revision.md](petition-revision.md) to the [existing Action Network petition](https://actionnetwork.org/petitions/stand-for-pension-integrity?source=arpensions).

Verify public text, actual subscription settings and displayed preferences, links and confirmation behavior. A draft, website preview or visit to `/take-action/thanks/` does not prove that a petition was updated or a signature received. This release procedure does not authorize automatic correspondence.

## Approval must match the exact source candidate

`release-status.json` begins with gates unset. Leave them unset until the represented actions are complete:

| Field | Required evidence |
|---|---|
| `externalPetitionAligned: true` | Joshua applied and verified description, letter, subscription settings and confirmation |
| `petitionVerifiedAt` | Actual verification timestamp |
| `petitionVerifiedBy` | Person performing verification |
| `publicationApproved: true` | Joshua explicitly approved this concrete release |
| `approvedBy` | Person granting approval |
| `approvedSourceDigest` | Fingerprint of the approved source candidate |

After source edits, generated assets and documentation are final:

```sh
node scripts/release-check.mjs --fingerprint
```

Record the returned fingerprint with real verification and approval information, then check:

```sh
npm run release:check
```

The digest covers Git-listed tracked and nonignored untracked source files, including binary assets. It excludes `release-status.json`. Text line endings are normalized. Ignored `dist/` and `.qa/` files are outside this source digest; record ZIP hashes separately. Ensure intended candidate files are tracked in the final commit so CI sees the same inputs.

Unset gates and mismatched digests must fail. Never copy approval to a changed candidate or enter an approval just to pass the check. The script checks recorded assertions; it cannot independently verify Action Network or authenticate consent. After source changes, rebuild, review and obtain approval for the new digest. Recheck the exact final main tree before deployment.

## Hosting migration order

**Switch Pages from branch publishing to GitHub Actions before merging Astro into main.** Otherwise the legacy Jekyll branch publisher can try to publish the replacement source tree.

Joshua's ordered steps:

1. Verify the starting state, preserve recovery artifacts/source/configuration and complete local and CI review.
2. Apply and verify the external petition package. Record explicit candidate approval and digest. Decide the disposition of PRs #139 and #147.
3. In **Settings → Pages**, change the build/deployment source to **GitHub Actions**, preserving the custom domain and HTTPS configuration. This is an external settings change, not an already-completed agent action.
4. Confirm legacy branch publishing is disabled. Then merge the reviewed Astro candidate into main through the chosen review procedure.
5. Confirm CI passes on resulting main and its source digest matches approval. If merged changes alter it, return to review and approval.
6. Manually dispatch **Release to GitHub Pages**, `.github/workflows/pages-release.yml`, on **main**. Its build job is restricted to `refs/heads/main` and runs the release gate, shared-copy check and full validation before uploading the artifact.
7. Observe deployment and verify the actual live content. Record workflow run, deployed commit, source digest, archive hashes and time.

The audit workflow runs on pull requests and selected pushes but does not deploy. The Pages workflow has only `workflow_dispatch`; merging alone does not dispatch Astro. Its deploy job uses the `github-pages` environment, `pages: write` and `id-token: write`. Do not assume an environment approval rule exists without inspecting GitHub settings.

## Post-release smoke checks

Check the live domain rather than relying only on a successful workflow:

- HTTPS and canonical domain; home, agency dossiers and brief show the intended release.
- Search returns results; document filters, record URLs, PDFs, text downloads and previews work.
- Representative legacy routes and fragments resolve, including the former one-page brief and historical downloads.
- Current amounts retain dates and stages; historical PDFs match their recorded hashes or an explicitly reviewed privacy revision with both hashes preserved.
- Action Network text, direct link and subscription disclosure agree with the approved package. Joshua performs any authorized test submission himself.
- Keyboard/mobile navigation, both themes, print, no-JavaScript reading, sitemap, RSS and social metadata behave as expected.

Record failures and their scope. A corrective source change requires validation and a new approval digest before another release.

Lab budgets and browser checks are not real-user measurements. LCP ≤2.5s, INP ≤200ms and CLS ≤0.1 are goals; the candidate cannot claim field performance without sufficient field evidence. This release adds no analytics tracker. Review available public field data later only if enough observations exist, identifying its time window.

## Roll back content and hosting deliberately

Joshua authorizes and performs external recovery actions if production has a material failure that cannot be promptly corrected.

1. Stop further manual deployments. Record the failed run, digest and observed failure; preserve the failed artifact for diagnosis.
2. Choose a verified known-good artifact. For legacy recovery, check the saved hash of `.qa/legacy-site-2050a39.zip` and preserve its matching source.
3. Choose a recovery mechanism explicitly:
   - **Keep Actions hosting:** deploy the verified legacy static artifact through a reviewed recovery workflow. The current Astro workflow rebuilds current source; it does not automatically deploy an arbitrary recovery ZIP.
   - **Restore branch publishing:** restore the complete known-good legacy Jekyll source on main using a reviewable recovery commit, then restore Pages to main / root. Do not enable branch publishing while main still contains only the Astro replacement.
4. Preserve or restore domain and HTTPS settings, confirm the active publishing mechanism and observe the recovery deployment.
5. Repeat live smoke checks, record the recovered version and explain the incident. Keep the rebuild candidate and evidence corrections for a reviewed repair.

A rollback must carry forward the reviewed privacy corrections in `src/data/download-revisions.json`; blindly restoring an older public PDF can re-expose its removed identifier. Keep the original recovery artifact private and build a sanitized rollback candidate before publication.

Restoring a site artifact does not undo external Action Network edits. Reconcile discrepancies explicitly; do not automatically restore superseded petition claims. Approval fields should describe the next intended candidate, never masquerade as evidence that rollback or publication has already occurred.
