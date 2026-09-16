# September 16 privacy follow-through

After the first audit release, visual review found a broker-account field still visible on page 2 of the May 2025 purchase confirmation. The preceding redaction covered page 1. The OCR text did not represent the page 2 identifier, so the earlier text-based screen missed this raster-only occurrence.

The field is now removed from the image and any text in its rectangle. All 12 May pages and all nine November pages were visually reviewed for additional account/routing exposures; existing redactions and masked account suffixes remain. No other full account/routing number was identified in those 21 pages. This is a bounded review of these two files, not a certification of every hosted PDF or barcode.

Validation checks the reviewed redaction rectangles in rendered pixels and extracted text, in addition to whole-file hashes. This guard failed on the published page 2 and passes after the repair. All other May pages render pixel-identically to the preceding public version. The repaired file has 12 pages, no embedded attachments and no widgets. Its financial amounts, dates and rates remain readable. The original and intermediate hashes are preserved in `src/data/download-revisions.json`.

- Previous public May SHA-256: `7552ba6896690f7f5cd9b880f4ccbbf572bb104f99e2c617dd492801de59d5c4`.
- Repaired May SHA-256: `771c5a2cff1fdb485ac741cff1de361b9b57e8687512320cb98ef512a91368c1`.
- The November replacement remains `5c077bc09f1c9a2c8fd2767936ca495e6cfb3bad37b09c724c63675890d94561`.

This minimal privacy repair follows Joshua's instruction to deploy the audit fixes and continue implementing confirmed remaining fixes. It does not publish the separate ongoing provenance or legislative-development work. Prior downloaded copies and Git history remain outside this replacement's reach.
