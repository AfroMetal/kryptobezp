import common


def assert_all_int(variables, names):
    for (var, name) in zip(variables, names):
        if not isinstance(var, int):
            raise TypeError('%s is not an integer' % name)
        if var < 0:
            raise ValueError('%s is negative, only non-negative arguments are valid' % name)
    return


def encrypt_int(message, key, n):
    assert_all_int([message, key, n],['message', 'key', 'n'])

    if common.byte_size(message) > common.byte_size(n):
        raise OverflowError('Message size %i is too big for n size %i' % (len(message), len(n)))

    return common.fast_mod_pow(message, key, n)


def decrypt_int(ciphertext, key, n):
    assert_all_int([ciphertext, key, n], ['ciphertext', 'key', 'n'])

    return common.fast_mod_pow(ciphertext, key, n)


def decrypt_int_crt(ciphertext, d_p, d_q, p, q, q_inv):
    assert_all_int([ciphertext, d_p, d_q, p, q], ['ciphertext', 'd_p', 'd_q', 'p', 'q'])

    m1 = common.fast_mod_pow(ciphertext, d_p, p)
    m2 = common.fast_mod_pow(ciphertext, d_q, q)

    h = int((q_inv*(m1 - m2)) % p)
    return m2 + h*q
