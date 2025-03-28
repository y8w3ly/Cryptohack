from Crypto.Util.number import *
from sage.all import *

with open('output.txt') as f:
    q, h = eval(f.readline().split(':')[-1])
    encrypted = eval(f.readline().split(':')[-1])

v = vector((1, h))
u = vector((0, q))

while True:
    if v * v < u * u:
        u, v = v, u
    m = ceil((u * v) / (u * u))
    if not m:
        break
    v -= m * u
f, g = u
# assert f * f < q and g * g < q

def decrypt(q, h, f, g, e):
    if g < 0:
        f, g = -f, -g
    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return m

flag = decrypt(q, h, f, g, encrypted)

print(long_to_bytes(flag).decode())
