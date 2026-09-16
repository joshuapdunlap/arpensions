# Astro banknote editorial rebuild

Approved implementation specification: the user's September 15, 2026 plan in this task.

## Deliverables

1. Reconcile the public evidence, narrative, source exhibits, letters, and policy brief with the September productions; produce a claim/publication matrix and an external petition revision package.
2. Migrate all existing public routes, PDFs, and fragments to Astro, TypeScript, validated Markdown and JSON collections, and GitHub Pages Actions.
3. Elevate API's pine/teal/jade banknote identity, League Spartan/Mulish/Plex typography, mobile usability, document previews, and light/dark presentation.
4. Add agency dossiers, Pagefind search, source filtering, dated updates, corrections, accessible diagrams, and resilient action paths.
5. Verify evidence arithmetic, provenance, compatibility, accessibility, mobile behavior, performance, and release/rollback readiness.

## Constraints

Pension reform is the primary objective. Treasury is a separately governed comparison. APERS has a $25M September 7 position; ATRS funding completed January 2 and includes the $9.9M February 17 security. Updated September 16: $84.9M is a conditional historical calculation combining different dates, not a confirmed floor; $125M substitutes full ATRS manager funding. Both depend on the Treasury projected-maturity and no-other-changes assumptions. Treasury's extra $10M payment remains processing evidence.

Preserve original evidence and historical public downloads. Publish only reviewed derivatives. Source images are literal rendered pages or rectangular crops with captions outside. No invented testimony, primary evidence, individual votes, adoption, sponsorship, or settlement. No analytics, CMS, new supporter database, paid service, or automatic correspondence.

Local work ends in a tested release candidate. Joshua applies external petition changes and approves publication. GitHub Pages production and security settings remain an explicit release step.

## Interface ownership

- Content task: src/content/pages/**/*.md, src/data/investigation.json, src/data/publication-matrix.json, docs/petition-revision.md.
- Main task: Astro configuration, layouts/components/styles/pages, browser interactions, collection schema, validation/tests, migration and release tools.
- Source task: reviewed source assets and source metadata/transcripts, after the content interface is fixed.

Pages use frontmatter: title, description, permalink, section (optional), eyebrow (optional), template (article/policy/evidence/agency/action/updates/people), agency (optional), sourceIds (array), reviewedAt, updatedAt. Body is plain Markdown with HTML allowed, no Liquid and no imports. All routes end with / except /404.html.

investigation.json uses sources as an object keyed by stable source ID; each source has title, agency, date, locator, originalFile, recordUrl, assetUrl (optional), summary, treatment. Other top-level keys: reviewedAt, financialRecords, agencies, policy, timeline, accountComposition, requirements. Main will add build-time validation. Keep legacy source IDs.

## Acceptance

All legacy routes/downloads/fragments; source/hash and truthful arithmetic tests; mobile 320/390/768 and desktop 1280/1536; both themes; reduced motion; keyboard navigation; no-JS reading; all public links; petition fallback; Pagefind search/filter/share state; source previews; print; metadata/RSS/sitemap; self-hosted assets; no sensitive files in output.

Initial compressed first-party JS <=50KB home, <=100KB evidence; shared compressed CSS <=40KB. Aim for LCP <=2.5s, INP <=200ms and CLS <=0.1; lab results are not field measurements.
