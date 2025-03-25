import hashlib
import binascii


def crc32(filename):
    buf = open(filename, "rb").read()
    hash = binascii.crc32(buf) & 0xFFFFFFFF
    return "%08X" % hash


def get_nes_info(path):
    with open(path, "rb") as f:
        data = f.read()

    rom_info = dict()

    if len(data) < 0x80:
        return None

    # NES 2.0
    check = data[:3].decode()
    if check in ["NES"] and (data[3] == 0x1A or data[3] == 0x00):
        # iNES
        if data[3] == 0x00:
            rom_info["rom_type"] = "Wii U VC"  # modified iNES

        if data[7] & 0x0C == 0x08:  # mapper_hi
            size = data[4] * 16384 + data[5] * 8192 + (data[9] << 8) * 16384
            print(size)
            print(1)

    # Not NES 2.0
    if data[7] & 0x0C == 0x00:  # mapper_hi
        if data[12] == 0 and data[13] == 0 and data[14] == 0 and data[15] == 0:
            # Definitely iNES
            idx = data[7] & 3
            if idx == 1:
                rom_info["rom_format"] = "iNES"
                rom_info["rom_system"] = "VS. System"
            elif idx == 2:
                rom_info["rom_format"] = "iNES"
                rom_info["rom_system"] = "PlayChoice-10"
            else:
                # TODO: What if both are set?
                rom_info["rom_format"] = "iNES"
                rom_info["rom_system"] = "NES / Famicom"

    print(rom_info)
    return rom_info


def get_md_info(path):
    with open(path, "rb") as f:
        data = f.read()

    rom_info = dict()

    if len(data) < 0x200:
        return None

    # Check for Sega CD
    # text = ""
    # for i in range(0x10, 0x10+0x10):
    #     text += str(data[i])
    # print(text)

    # for a plane binary ROM
    if len(data) < 0x300:
        return None

    # Check for SMD format (Mega Drive only)
    check = data[0x100 : 0x100 + 4].decode()
    if check != "SEGA":
        if data[1] == 3 and data[8] == 0xAA and data[9] == 0xBB and data[10] == 6:
            rom_info["rom_type"] = "MD"
            rom_info["cart_type"] = "SMD"
            print(rom_info)
            return rom_info

    # Check for BIN format
    check = data[0x100 : 0x100 + 16].decode()
    print([check])
    if check in ["SEGA MEGA DRIVE ", "SEGA_MEGA_DRIVE ", "SEGA GENESIS    "]:
        rom_type = "MD"
        cart_type = "BIN"
        copyright = data[0x110 : 0x110 + 16].decode()
        title_domestic = data[0x120 : 0x120 + 48].decode("cp932")
        title_export = data[0x150 : 0x120 + 48].decode("cp1252")
        serial = data[0x180 : 0x180 + 14].decode()

        rom_info["rom_type"] = rom_type
        rom_info["cart_type"] = cart_type
        rom_info["copyright"] = copyright.rstrip()
        rom_info["title"] = title_domestic.rstrip()
        rom_info["title_export"] = title_export
        rom_info["serial"] = serial.rstrip()
        print(rom_info)
        return rom_info
    return None


def get_rom_info(path, tag):

    hash_info = dict()

    # crc32
    hash_info["crc32"] = crc32(path)

    # md5
    with open(path, "rb") as f:
        data = f.read()
        hash = hashlib.md5(data).hexdigest()
        hash_info["md5"] = hash

    # sha256
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        hash_info["sha256"] = sha256_hash.hexdigest()

    # rom info
    if tag == "NES":
        rom_info = get_nes_info(path)
    elif tag == "MD":
        rom_info = get_md_info(path)
    else:
        return None

    rom_info.update(hash_info)
    print(rom_info)
    return rom_info
