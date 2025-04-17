from Crypto.Util.number import isPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

p = 310717010502520989590157367261876774703
a = 2
b = 3
E = EllipticCurve(GF(p),[a,b])

b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = E(b_x,b_y)

g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
G = E(g_x,g_y)

iv = bytes.fromhex("07e2628b590095a5e332d397b8a59aa7")
ct = bytes.fromhex("8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af")

#This is [n]G : Point(x=280810182131414898730378982766101210916, y=291506490768054478159835604632710368904)
nG = E(280810182131414898730378982766101210916,291506490768054478159835604632710368904)

#Now having G and nG ig we should get the n just from here.
n = G.discrete_log(nG)
S = n*B
sha1 = hashlib.sha1()
sha1.update(str(S[0]).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct),16)
print(pt.decode())