from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from gmpy2 import gcd
from Crypto.Util.number import inverse

ct = open("keys_and_messages/21.ciphertext").read()
key = open("keys_and_messages/21.pem").read()
public = RSA.import_key(key)
n = public.n
e = public.e
for i in range(1,51):
    n2 = RSA.import_key(open(f"keys_and_messages/{i}.pem").read()).n
    if gcd(n,n2)==1:
        continue
    else :
        p =gcd(n,n2)

q = n//p
phi = (p-1)*(q-1)
d = inverse(e,phi)
key = RSA.construct((n,e,int(d)))
cipher = PKCS1_OAEP.new(key)
flag = cipher.decrypt(bytes.fromhex(ct))
print(flag)