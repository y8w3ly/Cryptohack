import hashlib
#E:Y2=X3+497X+1768mod9739,G:(1804,5368)
a = 497
b = 1768
p = 9739
E = EllipticCurve(GF(p),[a,b])
G = E(815,3190)
n=1829
S = n*G
s = str(S[0])
print(f"crypto{{{hashlib.sha1(s.encode()).hexdigest()}}}")
