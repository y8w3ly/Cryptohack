p = 2^255 - 19
A = 486662
B = 1  # B = 1 for Curve25519 in Montgomery form
Fp = FiniteField(p)
E = EllipticCurve(Fp, [0, A, 0, 1, 0])  # Montgomery curve: By² = x³ + Ax² + x
Gx = Fp(9)
rhs = Gx^3 + A*Gx^2 + Gx
y_candidates = rhs.sqrt(all=True)
Gy = y_candidates[0]
G = E(Gx, Gy)
k = 0x1337c0decafe
n = k.nbits()
def montgomery_ladder(P, k):
    R0 = P
    R1 = 2*P
    for i in reversed(range(n - 1)):
        if (k >> i) & 1 == 0:
            R1 = R0 + R1
            R0 = 2 * R0
        else:
            R0 = R0 + R1
            R1 = 2 * R1
    return R0
Q = montgomery_ladder(G, k)
print(f"crypto{Q[0]}")
