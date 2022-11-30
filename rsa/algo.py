import random as rand
import time

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
    print("Plaintext:\n", message)

    enc = encrypt(pk, message)
    enc_message = ''.join(map(lambda x: str(x), enc))
    print("Encrypted:", enc_message)
    path = "files/" + file_name
    file = open(path, "w")
    file.write(enc_message)
    file.close()
    print()


def decrypt_file(file_name, pk, sk):
    path = "files/" + file_name

    enc = get_file_content(path)
    start = time.time()
    dec = decrypt(sk, enc)
    end = time.time()
    print("Decrypted:\n", dec)
    print("Decryption time:", end - start)

    print()