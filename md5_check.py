import zlib
import hashlib

from pathlib import Path
from common.checksum import read_data
from common.rom_info import get_nes_info, get_md_info


def print_info(rom_path, checksums):
    rom_name = rom_path.name
    md5 = checksums["md5"]
    print(f"ROM mdf / name: {md5} / {rom_name}")


def main():

    rom_type = "megadrive"

    src_dir = Path("c:/emul/roms/megadrive")
    src_rom_path = src_dir / "Valis III (Japan).zip"

    src_rom_name = None
    if src_rom_path.suffix == ".zip":
        src_rom_name = src_rom_path.stem + ".md"

    # Read data
    data = read_data(str(src_rom_path), src_rom_name)
    if data is None:
        print(f"Read data error: {src_rom_path}")
        return

    # CRC32

    crc32 = zlib.crc32(data)
    print(f"CRC32: {crc32:08x}")

    # Check md5 and sha256
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    print(f"md5: {md5_hash.hexdigest()}")

    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    print(f"sha256: {sha256_hash.hexdigest()}")

    if rom_type == "megadrive":
        get_md_info(data)


if __name__ == "__main__":
    main()
