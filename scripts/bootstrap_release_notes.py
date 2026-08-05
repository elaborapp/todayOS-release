#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


VERSIONS = ["2026.2", "2026.1", "2026"]
RELEASE_DATES = {
    "2026": "2026-06-29",
    "2026.1": "2026-07-13",
    "2026.2": "2026-07-27",
}
LOCALE_SOURCES = {
    "ar": "ar-SA",
    "bn": "bn-BD",
    "da": "da",
    "de": "de-DE",
    "en": "en-US",
    "en-AU": "en-AU",
    "en-CA": "en-CA",
    "en-GB": "en-GB",
    "en-IN": "en-US",
    "es": "es-ES",
    "fi": "fi",
    "fr": "fr-FR",
    "hi": "hi",
    "id": "id",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "nb": "no",
    "nl": "nl-NL",
    "pl": "pl",
    "pt-BR": "pt-BR",
    "ru": "ru",
    "sv": "sv",
    "th": "th",
    "tr": "tr",
    "ur": "ur-PK",
    "zh-Hans": "zh-Hans",
    "zh-Hant": "zh-Hant",
}
INITIAL_RELEASE_ITEMS = {
    "ar": "todayOS متاح الآن رسميًا!",
    "bn": "todayOS আনুষ্ঠানিকভাবে প্রকাশিত হয়েছে!",
    "da": "todayOS er officielt udgivet!",
    "de": "todayOS ist offiziell verfügbar!",
    "en": "todayOS is officially available!",
    "en-AU": "todayOS is officially available!",
    "en-CA": "todayOS is officially available!",
    "en-GB": "todayOS is officially available!",
    "en-IN": "todayOS is officially available!",
    "es": "¡todayOS ya está disponible oficialmente!",
    "fi": "todayOS on julkaistu virallisesti!",
    "fr": "todayOS est officiellement disponible !",
    "hi": "todayOS आधिकारिक रूप से उपलब्ध है!",
    "id": "todayOS resmi tersedia!",
    "it": "todayOS è ufficialmente disponibile!",
    "ja": "todayOS が正式リリース！",
    "ko": "todayOS가 정식 출시되었습니다!",
    "nb": "todayOS er offisielt lansert!",
    "nl": "todayOS is officieel beschikbaar!",
    "pl": "todayOS jest już oficjalnie dostępny!",
    "pt-BR": "todayOS está oficialmente disponível!",
    "ru": "todayOS официально доступен!",
    "sv": "todayOS är officiellt lanserat!",
    "th": "todayOS เปิดตัวอย่างเป็นทางการแล้ว!",
    "tr": "todayOS resmen kullanıma sunuldu!",
    "ur": "todayOS باضابطہ طور پر دستیاب ہے!",
    "zh-Hans": "todayOS 正式上线！",
    "zh-Hant": "todayOS 正式上架！",
}


def parse_release_notes(value: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    for paragraph in value.strip().split("\n\n"):
        lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if not lines:
            continue
        title = None
        if not lines[0].startswith("- "):
            title = lines.pop(0).rstrip("：:")
        items = [line.removeprefix("- ").strip() for line in lines]
        if items:
            sections.append({"title": title, "items": items})
    return sections


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", default=Path("releases"), type=Path)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schemaVersion": 1,
        "latestVersion": VERSIONS[0],
        "appStoreURL": "https://apps.apple.com/app/id6764528281",
        "versions": VERSIONS,
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    localized_releases = {locale: [] for locale in LOCALE_SOURCES}
    for version in VERSIONS:
        version_directory = args.output / version
        version_directory.mkdir(parents=True, exist_ok=True)
        for locale, source_locale in LOCALE_SOURCES.items():
            if version == "2026":
                sections = [{"title": None, "items": [INITIAL_RELEASE_ITEMS[locale]]}]
            else:
                source_path = args.source / version / source_locale / "ios.json"
                source = json.loads(source_path.read_text(encoding="utf-8"))
                sections = parse_release_notes(source["whatsNew"])
            release = {
                "schemaVersion": 1,
                "version": version,
                "locale": locale,
                "releaseDate": RELEASE_DATES[version],
                "sections": sections,
            }
            localized_releases[locale].append(release)
            (version_directory / f"{locale}.json").write_text(
                json.dumps(release, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    catalogs_directory = args.output / "catalogs"
    catalogs_directory.mkdir(parents=True, exist_ok=True)
    for locale, releases in localized_releases.items():
        catalog = {
            "schemaVersion": 1,
            "locale": locale,
            "releases": releases,
        }
        (catalogs_directory / f"{locale}.json").write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
