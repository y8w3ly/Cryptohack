from sage.all import *

def gauss_reduction(v1, v2):
    while True:
        if v2.norm() < v1.norm():
            v1, v2 = v2, v1
        m = round((v1.dot_product(v2) / v1.dot_product(v1)))
        if m == 0:
            return v1, v2
        v2 = v2 - m * v1

v = vector(ZZ, [846835985, 9834798552])
u = vector(ZZ, [87502093, 123094980])

b1, b2 = gauss_reduction(v, u)

print(b1.dot_product(b2))
