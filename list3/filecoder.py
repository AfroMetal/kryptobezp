# -*- coding: utf-8 -*-

import sys
import jks

from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding

string2mode = {
    'cbc': AES.MODE_CBC,
    'ctr': AES.MODE_CTR,
    'gcm': AES.MODE_GCM,
}

sentinel = object()


def encode(mode, key, file_path, output_path=sentinel):
    cipher = aes_encoder(mode, key)
    output_path = '.'.join([file_path, 'aes']) if output_path is sentinel else output_path
    with open(file_path, mode='rb') as file:
        encrypted = cipher.encrypt(file.read() if mode != 'cbc'
                                   else Padding.pad(file.read(), AES.block_size, style='iso7816'))
    with open(output_path, mode='wb') as file:
        file.write((cipher.iv if mode == 'cbc' else cipher.nonce) + encrypted)
    print("\nFile was successfully encoded into " + output_path)


def decode(mode, key, file_path):
    with open(file_path, mode='rb') as file:
        file_bytes = file.read()
        cipher = aes_decoder(mode, key, file_bytes[:16] if mode != 'ctr' else file_bytes[:8])
        try:
            decrypted = cipher.decrypt(file_bytes[16:] if mode != 'ctr' else file_bytes[8:])
        except ValueError:
            print("\nThere was problem with decryption, make sure proper key and mode of operation is provided, "
                  "program will now close")
            return
    output_path = file_path.replace('.aes', '')
    with open(output_path, mode='wb') as file:
        try:
            file.write(Padding.unpad(decrypted, AES.block_size, style='iso7816'))
        except ValueError:
            file.write(decrypted)
    print("\nFile was successfully decoded into " + output_path)


def aes_encoder(mode, key):
    if mode == 'cbc':
        iv = get_random_bytes(16)
        return AES.new(key, string2mode.get(mode), iv=iv)
    if mode == 'ctr':
        nonce = get_random_bytes(8)
        return AES.new(key, string2mode.get(mode), nonce=nonce)
    if mode == 'gcm':
        nonce = get_random_bytes(16)
        return AES.new(key, string2mode.get(mode), nonce=nonce)


def aes_decoder(mode, key, nonce):
    try:
        if mode == 'cbc':
            return AES.new(key, string2mode.get(mode), iv=nonce)
        if mode == 'ctr':
            return AES.new(key, string2mode.get(mode), nonce=nonce)
        if mode == 'gcm':
            return AES.new(key, string2mode.get(mode), nonce=nonce)
    except ValueError:
        print("\nThere was problem with decryption, make sure proper mode of operation is provided, "
              "program will now close")

"""
def get_key():
    key_tuple = keystore.load_key()
    if key_tuple is None:
        sys.exit("File cannot be processed without key, program will now exit")
    return key_tuple[1]
"""


def main():
    if len(sys.argv) >= 6:
        file_path = sys.argv[2]
        keystore_path = sys.argv[3]
        key_id = sys.argv[4]
        mode = sys.argv[5]
        output_path = None
        if sys.argv[1] == 'encode' and len(sys.argv) == 7:
            output_path = sys.argv[6]
        if sys.argv[1] == 'decode' and not str(file_path).endswith('.aes'):
            print("\nOnly *.aes files are supported for decryption, program will now close")
            return
    else:
        print('\n'.join(["Provide all arguments",
                         "-for encoding: encode <file_path> <keystore_path> <key_id> <mode in ('cbc', 'ctr', 'gcm')> "
                         "[output_file]",
                         "-for decoding: decode <file_path> <keystore_path> <key_id> <mode in ('cbc', 'ctr', 'gcm')>"]))
        return

    keystore = None
    while keystore is None:
        try:
            keystore_password = getpass("Enter passphrase for keystore: ")
            keystore = jks.KeyStore.load(keystore_path, keystore_password, False)
        except jks.KeystoreSignatureException:
            print("Wrong passphrase, keystore cannot be opened, try again")
        except jks.BadKeystoreFormatException \
                or jks.UnsupportedKeystoreVersionException \
                or jks.DuplicateAliasException:
            print("\nThere was problem with the keystore, program will now close")
            return

    key = keystore.entries[key_id]
    while not key.is_decrypted():
        key_password = getpass("Enter passphrase for key: ")
        try:
            key.decrypt(key_password)
        except jks.DecryptionFailureException or ValueError:
            print("Wrong passphrase, key cannot be decrypted, try again")
        except jks.UnexpectedAlgorithmException:
            print("\nThere was problem with the key, program will now close")
            return

    if sys.argv[1] == "encode":
        encode(mode, key.key, file_path) if output_path is None \
            else encode(mode, key.key, file_path, output_path)
    elif sys.argv[1] == "decode":
        decode(mode, key.key, file_path)
    else:
        print("\nFirst argument is invalid, accepted arguments are 'encode' and 'decode'")
        return

if __name__ == "__main__":
    main()
