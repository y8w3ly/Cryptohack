

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_497 = Integer(497); _sage_const_1768 = Integer(1768); _sage_const_9739 = Integer(9739); _sage_const_815 = Integer(815); _sage_const_3190 = Integer(3190); _sage_const_1829 = Integer(1829); _sage_const_0 = Integer(0)
import hashlib
#E:Y2=X3+497X+1768mod9739,G:(1804,5368)
a = _sage_const_497 
b = _sage_const_1768 
p = _sage_const_9739 
E = EllipticCurve(GF(p),[a,b])
G = E(_sage_const_815 ,_sage_const_3190 )
n=_sage_const_1829 
S = n*G
s = str(S[_sage_const_0 ])
print(f"crypto{{{hashlib.sha1(s.encode()).hexdigest()}}}")

