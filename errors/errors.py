class ConnectionToMongoDbError(Exception):
    """Raised when the connection is impossible"""

    def __init__(self, message="Unable to connect to the database. "
                               "Either the cluster doesnt exist, either you don't have "
                               "access to it, or your internet connection is not working. Try again later"):
        self.message = message
        super().__init__(self.message)


class DuplicateFileNameDatabase(Exception):
    """Raised when there are duplicate file names in the databse"""

    def __init__(self, message="File already exists in the database"):
        self.message = message
        super().__init__(self.message)
