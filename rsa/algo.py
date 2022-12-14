import random as rand
import time
from app import *
import os
from database.database_crud import *

encryption_path = "/Users/volentiralexandra/Documents/enc/"


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
    data = open(filename).read()
    return data


def encrypt_file(file_name, pk, sk):
    message = get_file_content(file_name)

    enc = encrypt(pk, message)
    print("enc: ", enc)
    enc_message = ','.join(map(lambda x: str(x), enc))
    # print("Encrypted:", enc_message)
    path = encryption_path + os.path.basename(file_name)
    # if not not os.path.isfile(os.path.abspath(encryption_path)):
    #     print("file doesnt exist")
    #     return
    print(path)
    with open(path, "w") as f:
        f.write(enc_message)
        f.close()
    print()


def decrypt_file(file_name, pk, sk):
    path = encryption_path + file_name
    encrypted_message = get_file_content(path)
    enc_strings = encrypted_message.split(",")
    enc = [eval(i) for i in enc_strings]
    dec = decrypt(sk, enc)

    print("Decrypted:", dec)
    # print()


def test_rsa_algo():
    global records
    length_in_bits = 512
    p = get_prime_number(length_in_bits)
    q = get_prime_number(length_in_bits)

    while p == q:
        q = get_prime_number(length_in_bits)

    pk, sk = generate_key_pair(p, q)
    print("pk: ", pk, "sk", sk)
    f_name = "files/files_for_encryption/mary_oliver.txt"

    encrypt_file(f_name, pk, sk)
    # pk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # sk1 = records.find_one({'file_name': os.path.basename(f_name)})
    # print("pk1", pk)
    decrypt_file("mary_oliver.txt", pk, sk)
