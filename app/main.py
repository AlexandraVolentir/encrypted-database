import random as rand
import time
from rsa.algo import *
from database.database_crud import *


def test_con_to_db():
    # print(add_file_to_database("files/plaintext.txt", "2", "3"))
    # remove_file_from_database("plaintext.txt")
    test_rsa_algo()


def main():

    create_connection_to_database()
    test_con_to_db()


if __name__ == '__main__':
    main()
