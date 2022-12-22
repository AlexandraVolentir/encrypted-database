from rsa.algo import *
from database.database_crud import *


def main():
    """
    Here is called the main function of the app
    """

    create_connection_to_database()
    run_app()


if __name__ == '__main__':
    main()
