import random as rand
import time
import certifi

# from Crypto.Util import number

# pip install pymongo
from pymongo import MongoClient
from rsa.algo import *


def test_rsa_algo():
    length_in_bits = 512
    p = get_prime_number(length_in_bits)
    q = get_prime_number(length_in_bits)

    while p == q:
        q = get_prime_number(length_in_bits)

    pk, sk = generate_key_pair(p, q)
    print("pk: ", pk, "sk", sk)

    encrypt_file('plaintext.txt', pk, sk)
    # decrypt_file('../plaintext.txt', pk, sk)


def test_connection_to_db():

    sample_data = {
        'file_name': 'new_file',
        'hash': '123',
        'location': '/Users/volentiralexandra/Documents/enc',
        'pk': '1'
    }

    client = MongoClient("mongodb+srv://volentir:VyJ2IDqlRdVBoHjS@cluster0.orlskgk.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client.get_database("encrypted_db")
    # print(client)
    records = db.encrypted_file_data

    # count documents
    nr = records.count_documents({})
    print("nr", nr)

    # create a new document
    records.insert_one(sample_data)

def main():
    # test_rsa_algo()
    test_connection_to_db()


if __name__ == '__main__':
    main()
