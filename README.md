# todayOS Release Assets

Public download assets for todayOS.

- Website: https://today-os.app
- Press Kit: https://today-os.app/press-kit.html

## In-app release notes

`releases/manifest.json` identifies the latest public version and lists release-note versions in display order.

`releases/catalogs/<locale>.json` is the canonical localized release-note source used by the app. Each catalog contains the complete ordered version history for one todayOS app locale, keeping app launch fetching constant as history grows.

Each catalog release keeps every App Store changelog item in `sections`. `releaseDate` is calendar-date metadata used for the localized subtitle; there is no separately authored summary field. The initial unpublished format remains schema version `1`.

The first catalog was bootstrapped from public App Store release notes with `scripts/bootstrap_release_notes.py`. The script remains a reconstruction helper; edit catalogs directly for future product-focused release copy without changing the app schema.
