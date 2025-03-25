from pathlib import Path
from common.checksum import calculate_crc32, calculate_checksums
from common.rom_info import get_nes_info


def print_info(rom_path, checksums):
    rom_name = rom_path.name
    md5 = checksums["md5"]
    print(f"ROM mdf / name: {md5} / {rom_name}")


def main():

    src_dir = Path("c:/emul/roms/nes")
    dst_dir = Path("c:/emul/roms/nes")

    src_rom_path = src_dir / "Contra (Japan).nes"
    dst_rom_path = dst_dir / "Contra (Japan).nes"

    src_rom_name = None
    if src_rom_path.suffix == ".zip":
        src_rom_name = src_rom_path.stem + ".nes"

    dst_rom_name = None
    if dst_rom_path.suffix == ".zip":
        dst_rom_name = dst_rom_path.stem + ".nes"

    # Check md5 and sha256
    src_checksums = calculate_checksums(str(src_rom_path), src_rom_name)
    if src_checksums is not None:
        print(src_checksums["md5"])
        print(src_checksums["sha256"])
        get_nes_info(src_rom_path)
    dst_checksums = calculate_checksums(str(dst_rom_path), dst_rom_name)
    if dst_checksums is not None:
        print(dst_checksums["md5"])
        print(dst_checksums["sha256"])
        get_nes_info(dst_rom_path)

    if src_checksums["md5"] != dst_checksums["md5"]:
        print("md5 mismatch")
        print_info(src_rom_path, src_checksums)
        print_info(dst_rom_path, dst_checksums)
    else:
        print("md5 match")


if __name__ == "__main__":
    main()
