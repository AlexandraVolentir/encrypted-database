from rsa.algo import *
from database.database_crud import *


def main():
    create_connection_to_database()
    test_rsa_algo()


if __name__ == '__main__':
    main()
