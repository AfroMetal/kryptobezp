# -*- coding: utf-8 -*-

import codecs
import sys
import lib.keystore as ks

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding

string2mode = {
    'cbc': AES.MODE_CBC,
    'ctr': AES.MODE_CTR,
    'gcm': AES.MODE_GCM,
}

sentinel = object()
keystore = None


def encode(mode, file_path, output_path=sentinel):
    cipher = aes_encoder(mode)
    output_path = '.'.join([file_path, keystore.key_id, 'aes']) if output_path is sentinel else output_path
    with codecs.open(file_path, mode='rb') as file:
        encrypted = cipher.encrypt(file.read() if mode != 'cbc' else Padding.pad(file.read(), AES.block_size, style='iso7816'))
    with codecs.open(output_path, mode='wb') as file:
        file.write((cipher.iv if mode == 'cbc' else cipher.nonce) + encrypted)


def decode(mode, file_path):
    with codecs.open(file_path, mode='rb') as file:
        file_bytes = file.read()
        cipher = aes_decoder(mode, file_bytes[:16] if mode != 'ctr' else file_bytes[:8])
        decrypted = cipher.decrypt(file_bytes[16:] if mode != 'ctr' else file_bytes[8:])
    with codecs.open(file_path.replace('.'.join(['', keystore.key_id, 'aes']), ''), mode='wb') as file:
        try:
            file.write(Padding.unpad(decrypted, AES.block_size, style='iso7816'))
        except ValueError:
            file.write(decrypted)


def aes_encoder(mode):
    key = get_random_bytes(32)
    keystore.save_key(key)
    if mode == 'cbc':
        iv = get_random_bytes(16)
        return AES.new(key, string2mode.get(mode), iv=iv)
    if mode == 'ctr':
        nonce = get_random_bytes(8)
        return AES.new(key, string2mode.get(mode), nonce=nonce)
    if mode == 'gcm':
        nonce = get_random_bytes(16)
        return AES.new(key, string2mode.get(mode), nonce=nonce)


def aes_decoder(mode, nonce):
    key = get_key()
    if mode == 'cbc':
        return AES.new(key, string2mode.get(mode), iv=nonce)
    if mode == 'ctr':
        return AES.new(key, string2mode.get(mode), nonce=nonce)
    if mode == 'gcm':
        return AES.new(key, string2mode.get(mode), nonce=nonce)


def get_key():
    key_tuple = keystore.load_key()
    if key_tuple is None:
        sys.exit("File cannot be processed without key, program will now exit")
    return key_tuple[1]


def main():
    if len(sys.argv) >= 6:
        file_path = sys.argv[2]
        keystore_path = sys.argv[3]
        key_id = sys.argv[4]
        mode = sys.argv[5]
        output_path = None
        if len(sys.argv) == 7 and sys.argv[1] == 'encode':
            output_path = sys.argv[6]
    else:
        print('\n'.join(["Provide all arguments",
                         "-for encoding: encode <file_path> <keystore_path> <key_id> <mode in ('cbc', 'ctr', 'gcm')> "
                         "?<output_file>?",
                         "-for decoding: decode <file_path> <keystore_path> <key_id> <mode in ('cbc', 'ctr', 'gcm')>"]))
        return

    global keystore
    keystore = ks.Keystore(keystore_path.strip('"'), key_id)

    if sys.argv[1] == "encode":
        encode(mode, file_path) if output_path is None else encode(mode, file_path, output_path)
    elif sys.argv[1] == "decode":
        decode(mode, file_path)
    else:
        print("\nFirst argument is invalid, accepted arguments are 'encode' and 'decode'")
        return

if __name__ == "__main__":
    main()
