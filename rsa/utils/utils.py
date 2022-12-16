import hashlib


def md5(file_path):
    """
    Computes the md5 message digest algo giving a 128-bit hash value
    :param file_path: path of the file
    :return: the digest
    """

    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()
