import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from binascii import unhexlify

p = 9739
a = 497
b = 1768
E = EllipticCurve(GF(p), [a, b])

x = 4726

nB = 6534

rhs = (x^3 + a*x + b) % p

y = power_mod(rhs, (p + 1) // 4, p)

Qa = E(x, y)

S = nB * Qa

k = hashlib.sha1(str(S[0]).encode()).digest()[:16]

iv = unhexlify('cd9da9f1c60925922377ea952afc212c')
ciphertext = unhexlify('febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8')
cipher = AES.new(k, AES.MODE_CBC, iv)

flag = unpad(cipher.decrypt(ciphertext), 16).decode()

print(flag)
