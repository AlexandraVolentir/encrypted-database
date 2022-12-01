import random as rand
import time
from rsa.algo import *
from database.database_crud import *


def test_rsa_algo():
    global records
    length_in_bits = 512
    p = get_prime_number(length_in_bits)
    q = get_prime_number(length_in_bits)

    while p == q:
        q = get_prime_number(length_in_bits)

    pk, sk = generate_key_pair(p, q)
    print("pk: ", pk, "sk", sk)
    f_name = "files/plaintext.txt"
    print("rec", records)
    encrypt_file(f_name, pk, sk)
    # pk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # sk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # print("pk1", pk)
    decrypt_file('plaintext.txt', pk, sk)


def test_con_to_db():
    # print(add_file_to_database("files/plaintext.txt", "2", "3"))
    # remove_file_from_database("plaintext.txt")
    test_rsa_algo()


def main():

    create_connection_to_database()
    test_con_to_db()


if __name__ == '__main__':
    main()
