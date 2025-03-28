import math
from decimal import *
from sage.all import *

getcontext().prec = int(100)

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]

Matrice = Matrix(ZZ, 24, 24)
#I wasted a lot of time since i thought the flag length was 27(same as PRIMES), didn't know that crypto{???????????????} has the same length.
for i in range(23):
    Matrice[i, i] = 1
    Matrice[i, 23] = math.floor(Decimal(PRIMES[i]).sqrt() * int(16**64))
Matrice[23, 23] = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433

res = Matrice.BKZ()
flag = ""
print(res)
for i in range(23):
    #I don't understand why all values are negative
    flag += chr(-res[0][i])
print(flag)
