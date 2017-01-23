import sys

from Crypto.Hash import SHA256

from common import byte_size
from key import PublicKey, PrivateKey


def encrypt(message, public_key):
    if not isinstance(public_key, PublicKey):
        raise AttributeError('public_key is not PublicKey instance, you have to use PublicKey for encrypting')

    length = byte_size(public_key.n)

    b_message = message.encode()

    parts = [b_message[i:i + length] for i in range(0, len(b_message), length)]

    ciphertext = b''

    for part in parts:
        int_part = int.from_bytes(part, byteorder=sys.byteorder)
        encrypted = public_key.encrypt(int_part)
        block = encrypted.to_bytes(length, byteorder=sys.byteorder)
        ciphertext += block

    return ciphertext


def decrypt(ciphertext, private_key, crt=True):
    if not isinstance(private_key, PrivateKey):
        raise AttributeError('private_key is not PrivateKey instance, you have to use PrivateKey for decrypting')

    length = byte_size(private_key.n)

    parts = [ciphertext[i:i + length] for i in range(0, len(ciphertext), length)]

    message = b''

    for part in parts:
        int_part = int.from_bytes(part, byteorder=sys.byteorder)
        decrypted = private_key.decrypt_with_blind(int_part, crt=crt)
        block = decrypted.to_bytes(length, byteorder=sys.byteorder)
        message = b''.join([message, block])

    return message.rstrip(b'\x00')


def sign(message, private_key):
    if not isinstance(private_key, PrivateKey):
        raise AttributeError('private_key is not PrivateKey instance, you have to use PrivateKey for signing')

    length = byte_size(private_key.n)

    b_message = message.encode()
    b_hash = _byte_hash(b_message)

    parts = [b_hash[i:i + length] for i in range(0, len(b_hash), length)]

    signature = b''

    for part in parts:
        int_part = int.from_bytes(part, byteorder=sys.byteorder)
        encrypted = private_key.encrypt_with_blind(int_part)
        block = encrypted.to_bytes(length, byteorder=sys.byteorder)
        signature += block

    return signature


def _byte_hash(message):
    h = SHA256.new()
    block_size = h.block_size

    parts = [message[i:i + block_size] for i in range(0, len(message), block_size)]

    for part in parts:
        h.update(part)

    return h.digest()


def verify_signature(message, signature, public_key):
    if not isinstance(public_key, PublicKey):
        raise AttributeError('public_key is not PublicKey instance, you have to use PublicKey for encrypting')

    length = byte_size(public_key.n)

    parts = [signature[i:i + length] for i in range(0, len(signature), length)]

    b_hash_signature = b''

    for part in parts:
        int_part = int.from_bytes(part, byteorder=sys.byteorder)
        decrypted = public_key.decrypt(int_part)
        block = decrypted.to_bytes(length, byteorder=sys.byteorder)
        b_hash_signature = b''.join([b_hash_signature, block])

    b_hash_signature = b_hash_signature.rstrip(b'\x00')

    b_message = message.encode()
    b_hash_message = _byte_hash(b_message)

    if b_hash_message != b_hash_signature:
        raise ValueError('Signature does not match message!')

    print('The message authentication with signature was successful!')

    return True
