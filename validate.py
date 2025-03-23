import json
import shutil
from pathlib import Path
from common.checksum import calculate_crc32, calculate_checksums
from common.tags import CONSOLE_MODELS, JSON_TAG
from common.fileio import read_xml, save_xml


def check_key_name(data, base_dir):
    for k, v in data.items():
        path = v["path"].replace("./", "")

        if "filename" not in v:
            print(f"{k}: filename is not found")
            continue

        filename = v["filename"]
        # if not file_name.endswith(".zip"):
        #     v["filename"] = file_name

        # if not file_name.endswith(".zip"):
        #     if v["lang"] == "jp":
        #         print(file_name)

        # md5 check
        # checksum = calculate_checksums(str(base_dir / path), filename)
        # if checksum["md5"] != v["md5"]:
        #     print(checksum["md5"])
        #     print(f"{k}: md5 is not match")

        if "releaseyear" in v and "releasedate" in v:
            print(f"Release year and release date are both found: {k}")

        # file check
        # for tag in ["image", "video", "marquee", "thumbnail", "manual"]:
        #     if tag not in v:
        #         continue
        #     path = base_dir / v[tag]
        #     if not path.exists():
        #         print(f"{k}: {tag} file is not found")
        #         v.pop(tag)
        #         continue


def main():
    base_dir = Path("c:/emul/roms")

    console_model = "megadrive"
    if not console_model in CONSOLE_MODELS:
        print(f"Console model {console_model} not supported")
        return

    xml_path = Path("roms") / console_model / "gamelist.xml"
    # xml_path = base_dir / console_model / "gamelist.xml"
    if not xml_path.exists():
        print(f"XML file {xml_path} not found")
        return
    xml_data = read_xml(xml_path)

    # Load a json file
    json_path = Path("roms") / console_model / "gamelist.json"
    if json_path.exists():
        json_data = json.load(open(json_path, encoding="utf-8"))
    else:
        print(f"JSON file {json_path} not found")
        return

    # Check key name
    check_key_name(json_data, base_dir / console_model)

    # new_json_data = dict()
    # for k, v in json_data.items():
    #     new_json_data[k] = dict()
    #     for tag in JSON_TAG:
    #         if tag in v:
    #             new_json_data[k][tag] = v[tag]

    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(dict(sorted(new_json_data.items())), f, ensure_ascii=False, indent=4)
    return

    # Compare the number of key items
    if len(xml_data.keys()) > len(json_data.keys()):
        print(f"XML file {xml_path} has more keys than JSON file {json_path}")
    if len(xml_data.keys()) < len(json_data.keys()):
        print(f"JSON file {json_path} has more keys than XML file {xml_path}")

    # Compare keys
    diff_keys = set(xml_data.keys()) - set(json_data.keys())
    if len(diff_keys) > 0:
        print(f"XML file {xml_path} has extra keys: {diff_keys}")
        return
    diff_keys = set(json_data.keys()) - set(xml_data.keys())
    if len(diff_keys) > 0:
        print(f"JSON file {json_path} has extra keys: {diff_keys}")
        return

    # Common item comparison
    for k, v in json_data.items():
        if k in xml_data:
            xml_item = xml_data[k]
            for tag in v.keys():
                if tag not in xml_item:
                    continue

                if xml_item[tag] != v[tag]:
                    print(f"{k} {tag} is not match")
                    continue

                # Check image file
                # if tag in ["image", "marquee", "thumbnail", "manual"]:
                #     img_file = v[tag]

        # # Check rom file
        # rom_file = v["rom_name"]
        # rom_path = base_dir / k / rom_file
        # if not rom_path.exists():
        #     print(f"{rom_file} is not found")
        #     continue

        # # Check image file
        # img_file = v["image"]
        # img_path = base_dir / k / img_file
        # if not img_path.exists():
        #     print(f"{img_file} is not found")
        #     continue

        # # Check crc32
        # crc32 = calculate_crc32(rom_path)
        # if crc32 != v["crc32"]:
        #     print(f"{k} crc32 is not match")

        # # Check md5 and sha256
        # checksums = calculate_checksums(rom_path)
        # if checksums["md5"] != v["md5"]:
        #     print(f"{k} md5 is not match")
        # if checksums["sha256"] != v["sha256"]:
        #     print(f"{k} sha256 is not match")

    # Sort and write
    # json_path = "gamelist.json"
    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(dict(sorted(json_new.items())), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
