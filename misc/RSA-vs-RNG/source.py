from Crypto.Util.number import *
import json

MOD = 2**512
A = 2287734286973265697461282233387562018856392913150345266314910637176078653625724467256102550998312362508228015051719939419898647553300561119192412962471189
B = 4179258870716283142348328372614541634061596292364078137966699610370755625435095397634562220121158928642693078147104418972353427207082297056885055545010537

FLAG = b'crypto{???????????????????????????}'

class PRNG:
    def __init__(self, seed):
        self.state = (seed % MOD)

    def get_num(self):
        self.state = (A * self.state + B) % MOD
        return self.state

    def get_prime(self):
        p = self.get_num()
        while not isPrime(p):
            p = self.get_num()
        return p

seed = getRandomRange(1, MOD)
rng = PRNG(seed)

P = rng.get_prime()
Q = rng.get_prime()

N = P * Q
E = 0x10001
pt = bytes_to_long(FLAG)
ct = long_to_bytes(pow(pt, E, N))

json.dump({
    'N': N,
    'E': E,
    'ciphertext': ct.hex()
}, open('flag.enc', 'w'))