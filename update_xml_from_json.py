import json
from pathlib import Path
from common.tags import CONSOLE_MODELS
from common.fileio import save_xml


def main():
    console_model = "snes"
    if not console_model in CONSOLE_MODELS:
        print(f"Console model {console_model} not supported")
        return

    # Load json
    json_path = Path("roms") / console_model / "gamelist.json"
    json_data = json.load(open(json_path, encoding="utf-8"))

    # Save xml
    xml_path = Path("roms") / console_model / "gamelist.xml"
    save_xml(json_data, xml_path)


if __name__ == "__main__":
    main()
