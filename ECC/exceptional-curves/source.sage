from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
import hashlib

FLAG = b'crypto{??????????????????????}'


def gen_public_key():
    private = randint(1, E.order() - 1)
    public = G * private
    return(public, private)


def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()[0]


def encrypt_flag(flag):
    # Bob's public key
    b_x = 0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38
    b_y = 0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf
    B = E(b_x, b_y)
    # Calculate shared secret
    A, nA = gen_public_key()
    print(f'Public Key: {A}')
    secret = shared_secret(B, nA)
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    # Prepare encryption to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data


# Curve params
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

# Define curve
E = EllipticCurve(GF(p), [a, b])

# Protect against Pohlig-Hellman Algorithm
assert is_prime(E.order())

# Create generator
G = E.gens()[0]
print(f'Generator: {G}')

encrypted_flag = encrypt_flag(FLAG)
print(encrypted_flag)
