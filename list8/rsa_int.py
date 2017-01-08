from list8 import common


def assert_all_int(variables, names):
    for (var, name) in variables, names:
        if not isinstance(var, int):
            raise TypeError('%s is not an integer' % name)
        if var < 0:
            raise ValueError('%s is negative, only non-negative arguments are valid' % name)
    return


def encrypt_int(message, key, n):
    assert_all_int([message, key, n],['message', 'key', 'n'])

    if message > n:
        raise OverflowError('Message %i is too big for n %i' % (message, n))

    return common.fast_mod_pow(message, key, n)


def decrypt_int(ciphertext, key, n):
    assert_all_int([ciphertext, key, n], ['ciphertext', 'key', 'n'])

    return common.fast_mod_pow(ciphertext, key, n)
