import certifi
import os
from pymongo import MongoClient
from global_data import GlobalData
from errors.errors import *
from utils.utils import md5


def add_file_to_database(path, enc_path, pk, sk, enc_method="rsa"):
    """
    Inserts the file and its info (location, hash, encryption method, keys) in mongodb
    using the insert_one method on the current records after verifying that it doesn't already
    exist in the database

    :param enc_path: path for encryption
    :param enc_method: method of encryption (rsa by default)
    :param path: absolute path of the encrypted file
    :param pk: public key (n, e)
    :param sk: secret key (n, d)
    :return: message of the successful/unsuccessful course of the adding operation
    """

    file_name = os.path.basename(path)
    abs_path = os.path.abspath(path)

    if not abs_path:
        return path + "is an invalid path"

    count = GlobalData.records.count_documents({'file_name': file_name})
    try:
        if count >= 1:
            raise DuplicateFileNameDatabase
    except DuplicateFileNameDatabase:
        return False

    data = {
        'file_name': file_name,
        'hash': md5(path),
        'location': enc_path,
        'enc_method': enc_method,
        'n': str(pk[0]),
        'e': str(pk[1]),
        'd': str(sk[1])
    }

    GlobalData.records.insert_one(data)
    print("[db] File \"" + file_name + "\" successfully added")
    return True


def delete_file_from_database(file_name):
    """
    Removes the file first from mongodb atlas (with delete_one method),
    then from the system with os.remove()

    :param file_name: file name to eb removed from the system and from database
    :return: Success message/ error message
    """
    if not os.path.isdir(GlobalData.encryption_path):
        print("encryption path specified in global_data.py invalid, change and try again")
        return
    GlobalData.records.delete_one({'file_name': file_name})

    try:
        os.remove(GlobalData.encryption_path + file_name)
        print("[db] File \"" + file_name + "\" successfully deleted")

    except OSError:
        print("[db] Unable to delete \"" + file_name + "\"from encrypted db. File doesn't exist or I/O err")
        return


def get_records():
    return GlobalData.records


def create_connection_to_database():
    """
    Creates the connection with mongodb atlas, using the connection string
    and stores all the dictionaries in the records variable
    :return: None
    """

    try:
        client = MongoClient(
            "mongodb+srv://volentir:" + GlobalData.password + "@cluster0.orlskgk.mongodb.net/?retryWrites=true&w"
                                                              "=majority",
            tlsCAFile=certifi.where())

        db = client.get_database("encrypted_db")
        GlobalData.records = db.encrypted_file_data

    except ConnectionError:
        exit(0)

