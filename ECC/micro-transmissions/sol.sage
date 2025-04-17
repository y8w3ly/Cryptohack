from factordb import factordb
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad

#Our p is unknown
#p = getPrime(pbits)
#a = 1
#b = 4
#E = EllipticCurve(GF(p), [a,b])

#We can easily find the p from the output.txt:
#99061670249353652702595159229088680425828208953931838069069584252923270946291
p = 99061670249353652702595159229088680425828208953931838069069584252923270946291
a = 1
b = 4
E = EllipticCurve(GF(p), [a,b])

#The generator :
G=E(43190960452218023575787899214023014938926631792651638044680168600989609069200 , 20971936269255296908588589778128791635639992476076894152303569022736123671173)

#From the output we have a_x and b_x: 
#a_x = [na]G[0] na is unknown
a_x = 87360200456784002948566700858113190957688355783112995047798140117594305287669
#b_x = [nb]G[0] nb is unknown
b_x = 6082896373499126624029343293750138460137531774473450341235217699497602895121
#===============LOOOK HERE==========

# 3lach 3andi assertion error hnaya : assert (G = E.gens()[0]) ? the challenge is solved btw

#==================================
B = E.lift_x(b_x)
#Here we must get the na:
A = E.lift_x(a_x)
#we will use the pohling hellman method which is based on crt
o = G.order()
n = factordb.FactorDB(o)
n.connect()
factors = n.get_factor_list()[:8]
n = []
r = []
m = 1
for mod in factors:
    g2 = G*(o//mod)
    q2 = A*(o//mod)
    rem = discrete_log(q2, g2, operation='+')
    r.append(rem)
    n.append(mod)
    m *= mod
na = crt(r, n)
#now when having n we just need to calculate the secret and the rest is clear
S = na*B
sha1 = hashlib.sha1()
sha1.update(str(S[0]).encode('ascii'))
key = sha1.digest()[:16]
iv = bytes.fromhex("ceb34a8c174d77136455971f08641cc5")
ct = bytes.fromhex("b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453")
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct),16).decode()
print(pt)