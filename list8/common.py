def fast_pow(a, b):
    result = 1
    while b:
        if b & 0x1:
            result *= a
        a *= a
        b >>= 1
    return int(result)


def fast_mod_pow(a, b, n):
    result = 1
    while b:
        if b & 0x1:
            result = (result*a) % n
        a = (a*a) % n
        b >>= 1
    return int(result)


def extended_gcd(b, n):
    x, lx = 1, 0
    y, ly = 0, 1

    while n != 0:
        q, b, n = b // n, n, b % n
        x, lx = lx, x - q*lx
        y, ly = ly, y - q*ly

    return b, x, y


def mod_inv(b, n):
    g, x, _ = extended_gcd(b, n)

    if g != 1:
        raise ValueError('%i and %i are not relatively prime numbers, divider is %i' % (b, n, g))

    return x % n


def crt(a_values, m_values):
    M = 1
    x = 0

    for m_i in m_values:
        M *= m_i

    for (a_i, m_i) in zip(a_values, m_values):
        M_i = M // m_i
        y_i = mod_inv(M_i, m_i)

        x = (x + a_i*M_i*y_i) % M

    return x
