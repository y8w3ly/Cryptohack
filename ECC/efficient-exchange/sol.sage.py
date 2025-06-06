

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_9739 = Integer(9739); _sage_const_497 = Integer(497); _sage_const_1768 = Integer(1768); _sage_const_4726 = Integer(4726); _sage_const_6534 = Integer(6534); _sage_const_3 = Integer(3); _sage_const_1 = Integer(1); _sage_const_4 = Integer(4); _sage_const_0 = Integer(0); _sage_const_16 = Integer(16)
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from binascii import unhexlify

p = _sage_const_9739 
a = _sage_const_497 
b = _sage_const_1768 
E = EllipticCurve(GF(p), [a, b])

x = _sage_const_4726 

nB = _sage_const_6534 

rhs = (x**_sage_const_3  + a*x + b) % p

y = power_mod(rhs, (p + _sage_const_1 ) // _sage_const_4 , p)

Qa = E(x, y)

S = nB * Qa

k = hashlib.sha1(str(S[_sage_const_0 ]).encode()).digest()[:_sage_const_16 ]

iv = unhexlify('cd9da9f1c60925922377ea952afc212c')
ciphertext = unhexlify('febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8')
cipher = AES.new(k, AES.MODE_CBC, iv)

flag = unpad(cipher.decrypt(ciphertext), _sage_const_16 ).decode()

print(flag)

