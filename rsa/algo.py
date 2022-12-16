import random as rand

from database.database_crud import *
from global_data.global_data import GlobalData


def check_if_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
    return True


def get_prime_number(length_in_bits):
    primes = [i for i in range(0, length_in_bits) if check_if_prime(i)]
    return rand.choice(primes)


def compute_gcd(a, b):
    """Euclid's algo for computing the greatest common divisor"""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(nr1, nr2):
    """

    :param nr1: fist number
    :param nr2: second number
    :return:
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while nr1 != 0:
        (q, nr1), nr2 = divmod(nr2, nr1), nr1
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return nr2, x0, y0


def compute_modular_inverse(nr1, nr2):
    g, x, _ = extended_gcd(nr1, nr2)
    return x % nr2


def strong_exponent(phi):
    return rand.randrange(1, phi)


def compute_weak_exp():
    return rand.randrange(1, 2 ** 32 - 1)


def gen_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = compute_weak_exp()
    g = compute_gcd(e, phi)
    while g != 1:
        e = compute_weak_exp()
        g = compute_gcd(e, phi)
    d = compute_modular_inverse(e, phi)
    return (n, e), (n, d)


def encrypt(pk, text):
    n, key = pk
    list_of_ciphered_elements = [pow(ord(c), key, n) for c in text]
    return list_of_ciphered_elements


def decrypt(sk, text):
    n, key = sk
    plain = [chr(pow(c, key, n)) for c in text]
    return ''.join(plain)


def get_file_content(filename):
    try:
        data = open(filename).read()
        return data
    except EnvironmentError:  # parent of IOError, OSError
        print("Couldn't get the content of ", filename)


def encrypt_file(f_abs_path):
    if not os.path.isdir(GlobalData.encryption_path):
        print("encryption path specified in global_data.py invalid, change and try again")
        return
    if not os.path.isfile(f_abs_path):
        print("Invalid path.")
        return

    pk, sk = generate_key_tuples()
    message = get_file_content(f_abs_path)
    enc = encrypt(pk, message)
    enc_message = ','.join(map(lambda x: str(x), enc))
    enc_path = GlobalData.encryption_path + os.path.basename(f_abs_path)

    if not add_file_to_database(f_abs_path, enc_path, pk, sk):
        print("File already exists in db, unable to encrypt")
    try:
        with open(enc_path, "w") as f:
            f.write(enc_message)
            f.close()
    except EnvironmentError:  # parent of IOError, OSError
        print("Couldn't open file for writing encrypted message")


def decrypt_file(file_name):
    """
    Decrypts the file using the rsa algorithm

    :param file_name: the file name to be found among the stored encrypted files and db names
    :return: None
    """

    if not os.path.isdir(GlobalData.encryption_path):
        print("encryption path specified in global_data.py invalid, change and try again")
        return
    record = GlobalData.records.find_one({'file_name': file_name})
    sk = (int((record['n'])), int(record['d']))

    counter = GlobalData.records.count_documents({'file_name': file_name})

    if counter > 1:
        print("Unable to do decryption... Too many files with same name detected")
        return

    path = record['location']
    encrypted_message = get_file_content(path)
    enc_strings = encrypted_message.split(",")
    enc = [eval(i) for i in enc_strings]
    dec = decrypt(sk, enc)
    print("Decrypted:", dec)


def generate_key_tuples():
    length_in_bits = 1024
    p = get_prime_number(length_in_bits)
    q = get_prime_number(length_in_bits)

    while p == q:
        q = get_prime_number(length_in_bits)

    pk, sk = gen_key_pair(p, q)
    return pk, sk


def run_app():
    while True:
        inp = input('1 - store, 2 - read, 3 - delete, q - quit\n')
        if inp.__eq__("1"):
            path = input("Please enter the path of the file to store: \n")
            encrypt_file(path)

        elif inp.__eq__("2"):
            f_name = input("Please enter the name of the file to read: \n")
            decrypt_file(f_name)

        elif inp.__eq__("3"):
            f_name = input("Please enter the name of the file to delete: \n")
            delete_file_from_database(f_name)

        elif inp.__eq__("q"):
            print("Goodbye")
            break
        else:
            print("unknown command, try again")
        print()
