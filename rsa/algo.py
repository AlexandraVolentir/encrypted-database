import random as rand

from database.database_crud import *
from global_data import GlobalData


def check_if_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
    return True


def get_prime_number(length_in_bits):
    primes = [i for i in range(0, length_in_bits) if check_if_prime(i)]
    return rand.choice(primes)


# Euclid's algorithm for determining the greatest common divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Extended Euclidean algorithm
def extended_gcd(a, b):
    # return (g, x, y) such that a*x + b*y = g = gcd(a, b)
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def modular_inverse(a, b):
    g, x, _ = extended_gcd(a, b)
    return x % b


def strong_exponent(phi):
    return rand.randrange(1, phi)


def weak_exponent(phi):
    return rand.randrange(1, 2 ** 32 - 1)


def generate_key_pair(p, q):
    n = p * q

    # Phi is the totient of n
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are co-prime
    e = weak_exponent(phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are co-prime
    g = gcd(e, phi)
    while g != 1:
        e = weak_exponent(phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = modular_inverse(e, phi)

    # Return public and private key pair
    return (n, e), (n, d)


def encrypt(public_key, plaintext):
    n, key = public_key
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(private_key, ciphertext):
    n, key = private_key
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)


def get_file_content(filename):
    try:
        data = open(filename).read()
        return data
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print("Couldn't get the content of ", filename)


def encrypt_file(f_abs_path):
    pk, sk = generate_key_tuples()
    message = get_file_content(f_abs_path)

    enc = encrypt(pk, message)
    # print("enc: ", enc)
    enc_message = ','.join(map(lambda x: str(x), enc))
    # print("Encrypted:", enc_message)
    enc_path = GlobalData.encryption_path + os.path.basename(f_abs_path)
    # if not not os.path.isfile(os.path.abspath(GlobalData.encryption_path)):
    #     print("file doesnt exist")
    #     return
    add_file_to_database(f_abs_path, enc_path, pk, sk)
    try:
        with open(enc_path, "w") as f:
            f.write(enc_message)
            f.close()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print("Couldn't open file for writing encrypted message")
    print()


def decrypt_file(file_name):
    """
    Decrypts the file using the rsa algorithm

    :param file_name: the file name to be found among the stored encrypted files and db names
    :param pk: public key tuple
    :param sk: secret key tuple
    :return: None
    """

    record = GlobalData.records.find_one({'file_name': file_name})
    sk = (int((record['n'])), int(record['d']))

    counter = GlobalData.records.count_documents({'file_name': file_name})

    if counter > 1:
        print("Unable to do decrpyption... Too many files with same name detected")
        return

    path = record['location']
    encrypted_message = get_file_content(path)
    enc_strings = encrypted_message.split(",")
    enc = [eval(i) for i in enc_strings]
    dec = decrypt(sk, enc)

    print("Decrypted:", dec)
    # print()


def generate_key_tuples():
    length_in_bits = 1024
    p = get_prime_number(length_in_bits)
    q = get_prime_number(length_in_bits)

    while p == q:
        q = get_prime_number(length_in_bits)

    pk, sk = generate_key_pair(p, q)

    # print("pk: ", pk, "sk", sk)
    return pk, sk


def test_rsa_algo():
    """
    Generates the keys on 1024 using p and q
    calls to encrypt and decrypt functions to test the functionality
    :return:
    """

    f_abs_path = "files/sample_files_enc/lucian_blaga.txt"

    encrypt_file(f_abs_path)

    # pk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # sk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # print("pk1", pk)
    decrypt_file("lucian_blaga.txt")
    delete_file_from_database("lucian_blaga.txt")


def run_app():
    while True:
        inp = input('1 - encrypt, 2 - decrypt, 3 - delete, q - quit')
        if inp.__eq__("1"):
            path = input("Please write/paste the file path")
            encrypt_file(path)

        else:
            print(f'You entered {password}')
            break
