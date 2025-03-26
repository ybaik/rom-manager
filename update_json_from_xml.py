import json
from pathlib import Path
from common.fileio import read_xml
from common.tags import CONSOLE_MODELS, JSON_TAG


def main():
    console_model = "snes"

    if not console_model in CONSOLE_MODELS:
        print(f"Console model {console_model} not supported")
        return

    # xml_path = Path("m:/RetroBat/roms") / console_model / "gamelist.xml"
    xml_path = Path("roms") / console_model / "gamelist.xml"
    if not xml_path.exists():
        print(f"XML file {xml_path} not found")
        return
    xml_data = read_xml(xml_path)

    # Load a json file
    json_path = Path("roms") / console_model / "gamelist.json"

    if json_path.exists():
        json_data = json.load(open(json_path, encoding="utf-8"))
    else:
        json_data = dict()

    # Update a new json file
    json_new = dict()
    for k, v in xml_data.items():
        if k not in json_data:
            json_new[k] = dict()
            for tag in JSON_TAG:
                if tag in v:
                    json_new[k][tag] = v[tag]
        else:
            json_new[k] = json_data[k]
            for tag in JSON_TAG:
                json_item = json_data[k][tag] if tag in json_data[k] else ""
                xml_item = v[tag] if tag in v else ""

                if len(xml_item) and len(json_item) and xml_item != json_item:
                    print(f"{k} {tag} is not match")
                    continue
                if len(xml_item) and len(json_item) == 0:
                    json_new[k][tag] = xml_item

    # Sort and write
    json_path = Path("roms") / console_model / "gamelist.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(json_new.items())), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
