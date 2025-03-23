from pathlib import Path
from common.checksum import calculate_crc32, calculate_checksums


def print_info(rom_path, checksums):
    rom_name = rom_path.name
    md5 = checksums["md5"]
    print(f"ROM mdf / name: {md5} / {rom_name}")


def main():

    src_rom_path = Path("c:/emul/roms/megadrive/Gley.Lancer.Kor.bin")
    dst_rom_path = Path(
        "c:/emul/roms/megadrive_test/Advanced Busterhawk Gley Lancer (Japan).md"
    )

    # Check md5 and sha256
    src_checksums = calculate_checksums(str(src_rom_path))
    dst_checksums = calculate_checksums(str(dst_rom_path))

    if src_checksums["md5"] != dst_checksums["md5"]:
        print("md5 mismatch")
        print_info(src_rom_path, src_checksums)
        print_info(dst_rom_path, dst_checksums)
    else:
        print("md5 match")


if __name__ == "__main__":
    main()
