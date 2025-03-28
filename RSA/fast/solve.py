from Crypto.PublicKey import RSA
from factordb.factordb import FactorDB
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import long_to_bytes as l2b, inverse

key = open("key.pem").read()
ct = open("ciphertext.txt", "r").read()

public = RSA.import_key(key)
n = public.n
e = public.e
fdb = FactorDB(n)
fdb.connect()
factors = fdb.get_factor_list()
p, q = factors[0], factors[1]
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
flag = cipher.decrypt(bytes.fromhex(ct))
print(flag)