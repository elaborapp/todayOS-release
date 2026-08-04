#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


VERSIONS = ["2026.2", "2026.1"]
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


def parse_release_notes(value: str) -> tuple[str, list[dict[str, object]]]:
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

    summary = next(item for section in sections for item in section["items"])
    for section in sections:
        items = section["items"]
        if items and items[0] == summary:
            section["items"] = items[1:]
            break
    sections = [section for section in sections if section["items"]]
    return summary, sections


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

    for version in VERSIONS:
        version_directory = args.output / version
        version_directory.mkdir(parents=True, exist_ok=True)
        for locale, source_locale in LOCALE_SOURCES.items():
            source_path = args.source / version / source_locale / "ios.json"
            source = json.loads(source_path.read_text(encoding="utf-8"))
            summary, sections = parse_release_notes(source["whatsNew"])
            release = {
                "schemaVersion": 1,
                "version": version,
                "locale": locale,
                "summary": summary,
                "sections": sections,
            }
            (version_directory / f"{locale}.json").write_text(
                json.dumps(release, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )


if __name__ == "__main__":
    main()
