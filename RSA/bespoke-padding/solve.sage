from Crypto.Util.number import *
from pwn import remote

r = remote("socket.cryptohack.org",13386)

r.sendlineafter(b"Come back as much as you want! You'll never get my flag.",b'{"option":"get_flag"}')
print(r.recvline())
exit(0)


N = 6689395968128828819066313568755352659933786163958960509093076953387786003094796620023245908431378798689402141767913187865481890531897380982752646248371131
c1 = 3179086897466915481381271626207192941491642866779832228649829433228467288272857233211003674026630320370606056763863577418383068472502537763155844909495261
c2 = 6092690907728422411002652306266695413630015459295863614266882891010434275671526748292477694364341702119123311030726985363936486558916833174742155473021704



for r in range(256):
    R.<X> = PolynomialRing(Zmod(N))

    f1 = (X) ^ 5 - c2
    f2 = (X*256 + r) ^ 5 - c1

    def my_gcd(a, b): 
        return a.monic() if b == 0 else my_gcd(b, a % b)

    f = my_gcd(f1, f2)
    print(f)
    flag = f.coefficients()[0]

    flag = int(flag) * inverse(-1, N) % N
    if b'AKASEC' in long_to_bytes(int(flag)):
        print(long_to_bytes(int(flag)))
