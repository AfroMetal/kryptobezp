import logging

from Crypto.IO import PEM
from Crypto.PublicKey import RSA
from Crypto.Util import number

import common
import rsa_int

log = logging.getLogger(__name__)
EXPONENT = 65537


class AbstractKey:

    __slots__ = (
        'n',
        'e'
    )

    def __init__(self, n, e):
        self.n = n
        self.e = e

    def blind(self, message, r):
        return (message * pow(r, self.e, self.n)) % self.n

    def unblind(self, blinded_message, r):
        return (common.mod_inv(r, self.n) * blinded_message) % self.n


class PrivateKey(AbstractKey):

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
        super().__init__(n, e)
        self.d = d
        self.p = p
        self.q = q

        log.debug("calculating PrivateKey values...")

        self.d_p = int(d % (p-1))
        self.d_q = int(d % (q-1))
        self.q_inv = common.mod_inv(q, p)

        log.debug("PrivateKey ready")

    def __getitem__(self, key):
        return getattr(self, key)

    def encrypt_with_blind(self, message):
        r = number.getRandomNBitInteger(self.n.bit_length() - 1)
        blinded_message = self.blind(message, r)
        ciphertext = rsa_int.encrypt_int(blinded_message, self.d, self.n)

        return self.unblind(ciphertext, r)

    def decrypt_with_blind(self, ciphertext, crt=True):
        r = number.getRandomNBitInteger(self.n.bit_length() - 1)
        blinded_ciphertext = self.blind(ciphertext, r)

        if crt:
            message = self._decrypt_crt(blinded_ciphertext)
        else:
            message = self._decrypt_simple(blinded_ciphertext)

        return self.unblind(message, r)

    def _decrypt_simple(self, ciphertext):
        message = rsa_int.decrypt_int(ciphertext, self.d, self.n)

        return message

    def _decrypt_crt(self, ciphertext):
        message = rsa_int.decrypt_int_crt(ciphertext, self.d_p, self.d_q, self.p, self.q, self.q_inv)

        return message

    def save_pem(self, filename, passphrase=None):
        try:
            key = RSA.construct((self.n, self.e, self.d, self.p, self.q), consistency_check=True)
        except ValueError:
            raise ValueError('Consistency check when creating Crypto.PublicKey.RSA key failed')
        key_bytes = key.exportKey(passphrase=passphrase)

        with open(filename, 'w') as file:
            file.write(PEM.encode(key_bytes, marker='RSA PRIVATE KEY'))

        return key_bytes


class PublicKey(AbstractKey):

    __slots__ = (
        'n',  # pq
        'e',  # prime that is coprime with phi_n
    )

    def __init__(self, n, e):
        super().__init__(n, e)

        log.debug("PublicKey ready")

    def __getstate__(self):
        return self.n, self.e

    def encrypt(self, message):
        ciphertext = rsa_int.encrypt_int(message, self.e, self.n)

        return ciphertext

    def decrypt(self, ciphertext):
        message = rsa_int.decrypt_int(ciphertext, self.e, self.n)

        return message

    def save_pem(self, filename, passphrase=None):
        try:
            key = RSA.construct((self.n, self.e), consistency_check=True)
        except ValueError:
            raise ValueError('Consistency check when creating Crypto.PublicKey.RSA key failed')
        key_bytes = key.exportKey(passphrase=passphrase)

        with open(filename, 'w') as file:
            file.write(PEM.encode(key_bytes, marker='RSA PUBLIC KEY'))

        return key_bytes


def generate_p_q(len_bits, safe=True):
    if safe and len_bits < 1024:
        raise ValueError('len_bits=%i is too small, len_bits should be at least 1024' % len_bits)

    if len_bits % 128 != 0:
        raise ValueError('len_bits must be multiple of 128')

    p = number.getStrongPrime(len_bits)
    q = number.getStrongPrime(len_bits, e=p)

    return max(p, q), min(p, q)


def generate_e_d(p, q, exp):
    phi_n = (p-1)*(q-1)

    d = common.mod_inv(exp, phi_n)

    if (exp*d) % phi_n != 1:
        raise ValueError('e=%i and d=%i don\'t give ed = 1 mod phi_n=%i' % (exp, d, phi_n))

    return exp, d


def generate_keys(len_bits, exp=EXPONENT, safe=True):
    while True:
        p, q = generate_p_q(len_bits, safe=safe)
        try:
            e, d = generate_e_d(p, q, exp=exp)
            break
        except ValueError:
            pass

    return p, q, e, d


def get_keys(len_bits, exp=EXPONENT, safe=True):
    p, q, e, d = generate_keys(len_bits, exp=exp, safe=safe)
    n = p*q

    return PublicKey(n, e), PrivateKey(n, e, d, p, q)


def load_pem(filename, passphrase=None):
    with open(filename, 'r') as file:
        pem_string = file.read()

    pem_tuple = PEM.decode(pem_string)
    key = RSA.import_key(pem_tuple[0], passphrase=passphrase)

    if pem_tuple[1] == 'RSA PUBLIC KEY':
        return PublicKey(key.n, key.e)
    elif pem_tuple[1] == 'RSA PRIVATE KEY':
        return PrivateKey(key.n, key.e, key.d, key.p, key.q)
    else:
        raise AttributeError('PEM block marker is invalid, should be "RSA PUBLIC KEY" or "RSA PRIVATE KEY"')

__all__ = ['PublicKey', 'PrivateKey', 'get_keys']
