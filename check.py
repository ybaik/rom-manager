import json
from pathlib import Path
from common.fileio import XML_TAGS, read_xml, save_xml

JSON_TAG = [
    "path",
    "name",
    "desc",
    "image",
    "video",
    "marquee",
    "thumbnail",
    "manual",
    "rating",
    "releasedate",
    "release_year",
    "developer",
    "publisher",
    "genre",
    "family",
    "crc32",
    "md5",
    "sha256",
    "lang",
    "copyright",
    "serial",
    "localization",
    "loc_release_date",
    "loc_url",
]


def main():
    console_model = "megadrive"

    # json loading
    json_path = Path("roms") / console_model / "gamelist_backup.json"
    json_data = json.load(open(json_path, encoding="utf-8"))

    save_xml(json_data, "gamelist.xml")

    # Sort and write
    # json_path = "gamelist.json"
    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(dict(sorted(json_new.items())), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
