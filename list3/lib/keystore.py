# -*- coding: utf-8 -*-

import codecs
import os

from getpass import getpass
from Crypto.IO import PKCS8


class Keystore:

    def __init__(self, keystore_path, key_id):
        self.keystore_path = keystore_path
        self.key_id = key_id

    def save_to_keystore(self, wrapped_key):
        try:
            with codecs.open(os.path.sep.join([self.keystore_path, self.key_id]) + '.key', mode='xb') as file:
                file.write(wrapped_key)
        except FileExistsError as err:
            print(f"FileExistsError: key with id {self.key_id!s} already exists in keystore, choose another key; {err}")
            return
        except OSError:
            print(f"OSError: file {self.key_id!s}.txt in keystore cannot be opened")
            return
        print("Key saved successfully")

    def read_from_keystore(self):
        try:
            with codecs.open(os.path.sep.join([self.keystore_path, self.key_id]) + '.key', mode='rb') as file:
                return file.read()
        except OSError:
            print(f"OSError: file {self.key_id!s}.txt in keystore cannot be opened")
            return None

    def save_key(self, mode_id, private_key):
        key_oid = '.'.join([mode_id, self.key_id])
        passphrase = getpass(f"\nEnter passphrase for key with id {self.key_id!s}: ")
        wrapped_key = PKCS8.wrap(private_key,
                                 key_oid,
                                 passphrase=bytes(passphrase, 'utf-8'),
                                 protection=KEY_WRAPPER_ALG)
        self.save_to_keystore(wrapped_key)

    def load_key(self):
        passphrase = getpass(f"\nEnter passphrase for key with id {self.key_id!s}: ")
        wrapped_key = self.read_from_keystore()
        if wrapped_key is None:
            print("Key couldn't be retrieved from keystore")
            return None
        try:
            unwrapped = PKCS8.unwrap(wrapped_key, passphrase=bytes(passphrase, 'utf-8'))
        except ValueError as err:
            print(f"ValueError: problem decoding key file in keystore, check if the passphrase is correct; {err}")
            return None
        print("Key loaded successfully")
        return unwrapped

KEY_WRAPPER_ALG = 'scryptAndAES128-CBC'
