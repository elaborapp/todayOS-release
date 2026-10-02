# todayOS Release Assets

Public download assets for todayOS.

- Website: https://today-os.app
- Press Kit: https://today-os.app/press-kit.html

## In-app release notes

`releases/manifest.json` identifies the latest public version and lists release-note versions in display order.

`releases/catalogs/<locale>.json` is the canonical localized release-note source used by the app. Each catalog contains the complete ordered version history for one todayOS app locale, keeping app launch fetching constant as history grows.

Each catalog release keeps every App Store changelog item in `sections`. `releaseDate` is calendar-date metadata used for the localized subtitle; there is no separately authored summary field. The initial unpublished format remains schema version `1`.

The first catalog was bootstrapped from public App Store release notes with `scripts/bootstrap_release_notes.py`. The script remains a reconstruction helper; edit catalogs directly for future product-focused release copy without changing the app schema.

## CI

[Python security](.github/workflows/codeql.yml) uses CodeQL to scan the Python reconstruction helper for security issues. It runs when Python files or the workflow change in a pull request to `main` or a push to `main`, and can also be started manually from Actions. Documentation and release-note JSON changes alone do not trigger this scan.

The workflow has a 10-minute execution timeout and cancels older runs for the same PR or branch. GitHub runner queue time is separate from that timeout. CodeQL default setup must remain disabled so that this workflow controls scan triggers; there is no automatic weekly scan. This path-filtered workflow should not be configured as a required check for every PR.
