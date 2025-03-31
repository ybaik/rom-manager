import os
import zlib
import hashlib
import zipfile


def calculate_crc32(file_path):
    """
    Calculates the CRC-32 checksum of a file.

    :param file_path: Path to the file for which to calculate the CRC-32 checksum.
    :return: CRC-32 checksum as a hexadecimal string.
    """
    try:
        # Ensure the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Initialize CRC-32 checksum
        crc32_checksum = 0

        # Open the file in binary mode and read it in chunks
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(65536), b""):
                crc32_checksum = zlib.crc32(chunk, crc32_checksum)

        # Convert the checksum to a hexadecimal string
        hex_checksum = f"{crc32_checksum:08x}"
        return hex_checksum

    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def calculate_checksums(zip_file_path, target_file_name=None, zip_disable=False):
    """
    Calculates the MD5 and SHA-256 checksums of a file.

    :param file_path: Path to the file for which to calculate the checksums.
    :return: A dictionary containing the MD5 and SHA-256 checksums as hexadecimal strings.
    """
    try:
        # Ensure the file exists
        if not os.path.isfile(zip_file_path):
            raise FileNotFoundError(f"The file {zip_file_path} does not exist.")

        if zip_file_path.endswith(".zip") and not zip_disable:
            if target_file_name is None:
                return dict()
            with zipfile.ZipFile(zip_file_path, "r") as zip_file:
                with zip_file.open(target_file_name, "r") as target_file:
                    file_data = target_file.read()
                    md5_checksum = hashlib.md5(file_data).hexdigest()
                    sha256_checksum = hashlib.sha256(file_data).hexdigest()
                    return {"md5": md5_checksum, "sha256": sha256_checksum}
        else:
            # Initialize hash objects
            md5_hash = hashlib.md5()
            sha256_hash = hashlib.sha256()

            # Open the file in binary mode and read it in chunks
            with open(zip_file_path, "rb") as file:
                for chunk in iter(lambda: file.read(65536), b""):
                    md5_hash.update(chunk)
                    sha256_hash.update(chunk)

            # Get the hexadecimal digest of the checksums
            md5_checksum = md5_hash.hexdigest()
            sha256_checksum = sha256_hash.hexdigest()

            return {"md5": md5_checksum, "sha256": sha256_checksum}

    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None
