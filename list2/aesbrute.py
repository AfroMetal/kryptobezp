# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64
import sys
import time
import codecs
import itertools

__chars = '0123456789abcdef'


def __bruteforce(charset, length):
    return itertools.chain(''.join(x) for x in itertools.product(charset, repeat=length))


def isaccepted(char):
    return char.isprintable() | char.isspace()


def decrypt(ciphertextbase64, iv, key2, key1spacechars):
    ciphertext = (base64.b64decode(ciphertextbase64))

    for key1space in key1spacechars:
        print('Key space: ' + str(key1space) + '...')
        for key1suffix in __bruteforce(__chars, (64 - len(key2) - 1)):
            cipher = AES.new(bytes.fromhex(''.join([key1space, key1suffix, key2])),
                             AES.MODE_CBC,
                             IV=bytes.fromhex(iv))

            try:
                msg = cipher.decrypt(ciphertext).decode('utf-8').rstrip()
            except UnicodeDecodeError:
                continue

            if ((isaccepted(c)) for c in msg):
                key = ''.join([key1space, key1suffix, key2])
                with codecs.open('.'.join([key[:16], 'txt']), 'w', 'utf-8') as file:
                    file.write(' \n'.join([ciphertextbase64, iv, key, msg]))
                print(''.join(['Key: ', key, '\n', msg]))
                return msg
            else:
                continue

    print('Decryption failed.')
    return ''


def main():
    if len(sys.argv) == 5:
        decrypt(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    start = time.process_time()
    main()
    end = time.process_time()
    print('----------------- ' + str(end - start) + ' seconds')
