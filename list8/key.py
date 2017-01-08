import logging

from Crypto.Util import number
from list8 import common
from list8 import rsa_int

log = logging.getLogger(__name__)
EXPONENT = 65537


class PrivateKey:

    __slots__ = (
        'n',        # pq
        'e',        # prime that is coprime with phi_n
        'd',        # e^-1 mod phi_n
        'p',        # larger prime
        'q',        # smaller prime
        'd_p',      # d mod p-1
        'd_q',      # d mod q-1
        'q_inv',    # q^-1 mod p
    )

    def __init__(self, n, e, d, p, q):
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q

        self.d_p = int(d % (p-1))
        self.d_q = int(d % (q-1))
        self.q_inv = common.mod_inv(q, p)

    def __getitem__(self, key):
        return getattr(self, key)

    def encrypt(self, message):
        ciphertext = rsa_int.encrypt_int(message, self.d, self.n)
        return ciphertext

    def decrypt(self, ciphertext):
        message = rsa_int.decrypt_int(ciphertext, self.d, self.n)


class PublicKey:
    __slots__ = (
        'n',  # pq
        'e',  # prime that is coprime with phi_n
    )

    def __init__(self, n, e):
        self.n = n
        self.e = e

    def __getitem__(self, key):
        return getattr(self, key)

    def __getstate__(self):
        return self.n, self.e


def generate_p_q(len_bits, safe=True):
    if safe and len_bits < 1024:
        raise ValueError('len_bits=%i is too small, len_bits should be at least 1024' % len_bits)

    if len_bits % 128 != 0:
        raise ValueError('len_bits must be multiple of 128')

    p = number.getStrongPrime(len_bits)
    q = number.getStrongPrime(len_bits, e=p)

    return max(p, q), min(p, q)
