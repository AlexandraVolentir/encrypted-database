# encrypted-database
A tool that permits performing CRUD operations on a database that manages the location of encrypted files.

The files are stored on a disk encrypted in a known location and the metadata about the encryption method etc will be kept in a database.
The tool will permit adding a file into the database, reading a file from the database + erasing a file from the database.

The algorithm used for encryption is RSA and we don't utilize any other helping libraries for making the encryption algorithm.


requirements:
pip install mongo