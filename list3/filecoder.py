# -*- coding: utf-8 -*-

import codecs
import sys
import lib.keystore as ks

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Util import Padding

id2mode_var = {
    '0': AES.MODE_CBC,
    '1': AES.MODE_CTR,
    '2': AES.MODE_GCM,
}

mode_str2id = {
    'cbc': '0',
    'ctr': '1',
    'gcm': '2',
}

sentinel = object()
keystore = None


def encode(mode, file_path, output_path=sentinel):
    mode_id = mode_str2id.get(mode)
    cipher = aes_cipher(mode_id=mode_id)
    output_path = '.'.join([file_path, keystore.key_id, 'aes']) if output_path is sentinel else output_path
    with codecs.open(file_path, mode='rb') as file:
        encrypted = cipher.encrypt(file.read() if mode_id is not '0' else Padding.pad(file.read(), AES.block_size, style='iso7816'))
    with codecs.open(output_path, mode='wb') as file:
        file.write(encrypted)


def decode(file_path):
    cipher = aes_cipher()
    with codecs.open(file_path, mode='rb') as file:
        decrypted = cipher.decrypt(file.read())

    with codecs.open(file_path.replace('.'.join(['', keystore.key_id, 'aes']), ''), mode='wb') as file:
        try:
            file.write(Padding.unpad(decrypted, AES.block_size, style='iso7816'))
        except ValueError:
            file.write(decrypted)


def aes_cipher(mode_id=sentinel):
    if mode_id is sentinel:  # decode mode
        args = decode_tuple()
        return AES.new(args[0], mode=args[1], iv=args[2]) if args[3] is '0' \
            else AES.new(args[0], mode=args[1], counter=Counter.new(64, args[2])) if args[3] is '1' \
            else AES.new(args[0], mode=args[1], nonce=args[2])
    else:  # encode mode
        key = get_random_bytes(32)
        if mode_id is '0':
            iv = get_random_bytes(16)
            keystore.save_key(mode_id, iv + b'-----' + key)
            return AES.new(key, id2mode_var.get(str(mode_id)), iv=iv)
        if mode_id is '1':
            nonce = get_random_bytes(8)
            counter = Counter.new(64, nonce)
            keystore.save_key(mode_id, nonce + b'-----' + key)
            return AES.new(key, id2mode_var.get(str(mode_id)), counter=counter)
        if mode_id is '2':
            nonce = get_random_bytes(16)
            keystore.save_key(mode_id, nonce + b'-----' + key)
            return AES.new(key, id2mode_var.get(str(mode_id)), nonce=nonce)


def decode_tuple():
    key_tuple = keystore.load_key()
    if key_tuple is None:
        sys.exit("File cannot be processed without key, program will now exit")
    mode_id = key_tuple[0][:key_tuple[0].find('.')]
    return key_tuple[1].partition(b'-----')[2], \
        id2mode_var.get(mode_id), \
        key_tuple[1].partition(b'-----')[0], mode_id


def main():
    if len(sys.argv) >= 4:
        file_path = sys.argv[1]
        keystore_path = sys.argv[2]
        key_id = sys.argv[3]
        mode = None
        output_path = None
        if len(sys.argv) == 5:
            mode = sys.argv[4]
        if len(sys.argv) == 6:
            mode = sys.argv[4]
            output_path = sys.argv[5]
    else:
        print('\n'.join(["Provide all arguments",
                         "   for encoding: <file_path> <keystore_path> <key_id> <mode in ('cbc', 'ctr', 'gcm')> "
                         "?<output_file>?",
                         "   for decoding: <file_path> <keystore_path> <key_id>"]))
        return

    global keystore
    keystore = ks.Keystore(keystore_path.strip('"'), key_id)
    decode(file_path) if mode is None \
        else encode(mode, file_path) if output_path is None \
        else encode(mode, file_path, output_path)


if __name__ == "__main__":
    main()
