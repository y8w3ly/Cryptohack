import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a,b])

G = E(479691812266187139164535778017 , 568535594075310466177352868412)
Gx = G.xy()[0]
Gy = G.xy()[1]
#P1 = (1110072782478160369250829345256 : 800079550745409318906383650948 : 1) which is [n_a]*G :
P1 = E(1110072782478160369250829345256 , 800079550745409318906383650948)
Qx = P1.xy()[0]
Qy = P1.xy()[1]
#P2 = (1290982289093010194550717223760 : 762857612860564354370535420319 : 1) which is [n_b]*G :
P2 = E(1290982289093010194550717223760 , 762857612860564354370535420319)

#The shared secret is n_b*P1 == n_a*P2 but we don't have n_a and n_b (but we know that they are <p)
print(G.order())#103686954799254136375814
#From https://github.com/elikaski/ECC_Attacks?tab=readme-ov-file#ECC-Attacks
Gn = G.order()
k = 1
while p^k % Gn != 1:
    k += 1
Ek = EllipticCurve(GF(p ^ k), [a, b])
Gk = Ek(G)
Qk = Ek(P1)
Rk = Ek.random_point()
m = Rk.order()
d = gcd(m, Gn)
Tk = (m // d) * Rk
assert Tk.order() == d
assert (Gn*Tk).is_zero() # Point INFINITY

# Using T, pair G and Q to integers g and q such that q=g^n (mod p^k)
g = Gk.weil_pairing(Tk, Gn)
q = Qk.weil_pairing(Tk, Gn)
n = q.log(g)
S = n*P2
s = S.xy()[0]
sha1 = hashlib.sha1()
sha1.update(str(s).encode('ascii'))
key = sha1.digest()[:16]
iv = bytes.fromhex("eac58c26203c04f68d63dc2c58d79aca")
ct = bytes.fromhex("bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d")
cipehr = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipehr.decrypt(ct),16)
print(pt.decode())