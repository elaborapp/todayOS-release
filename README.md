# todayOS Release Assets

Public download assets for todayOS.

- Website: https://today-os.app
- Press Kit: https://github.com/ethanhuang13/todayOS-release/releases/download/presskit-2026/todayOS-PressKit-2026.zip

## In-app release notes

`releases/manifest.json` identifies the latest public version and lists release-note versions in display order. Each version has one JSON document per todayOS app locale under `releases/<version>/<locale>.json`.

`releases/catalogs/<locale>.json` is the generated, localized read model used by the app. It keeps app launch fetching constant as version history grows. Edit the version documents, then regenerate the catalogs with `scripts/bootstrap_release_notes.py`.

Release documents keep every App Store changelog item in `sections`. `releaseDate` is calendar-date metadata used for the localized subtitle; there is no separately authored summary field. The initial unpublished format remains schema version `1`.

The first catalog was bootstrapped from public App Store release notes. Future entries can be edited into product-focused summaries without changing the app schema.
