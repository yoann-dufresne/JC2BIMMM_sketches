
def xorshift64(x):
    # Max 64-bits uint used to disallow the integer to grow behind 64 bits.
    mask = 18446744073709551615

    # xorshift 64
    x = (x ^ (x << 13)) & mask
    x = (x ^ (x >> 7))
    x = (x ^ (x << 17)) & mask
    return x
