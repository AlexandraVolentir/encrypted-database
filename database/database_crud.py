import certifi
import hashlib
import os

# pip install pymongo
from pymongo import MongoClient

records = None
encryption_path = "/Users/volentiralexandra/Documents/enc/"
password = "VyJ2IDqlRdVBoHjS"


def md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def add_file_to_database(path, pk, sk):
    global encryption_path
    file_name = os.path.basename(path)
    abs_path = os.path.abspath(path)
    print(abs_path)
    if not abs_path:
        return path + "is an invalid path"

    if records.find_one({'file_name': file_name}):
        return "File \"" + file_name + "\" already exists in encrypted database"

    data = {
        'file_name': file_name,
        'hash': md5(file_name),
        'location': encryption_path + file_name,
        'pk': pk,
        'sk': sk
    }
    records.insert_one(data)
    return "File added successfully to encrypted db"


def remove_file_from_database(file_name):
    global records
    records.delete_one({'file_name': file_name})

    try:
        os.remove(encryption_path + file_name)
        return "Removal successful"
    except OSError:
        return "file doesnt exist"


def create_connection_to_database():
    global password
    global records

    client = MongoClient(
        "mongodb+srv://volentir:" + password + "@cluster0.orlskgk.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())

    db = client.get_database("encrypted_db")
    records = db.encrypted_file_data
