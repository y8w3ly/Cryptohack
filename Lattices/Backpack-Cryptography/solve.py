from Crypto.Util.number import *
from sage.all import *

def solve_backpack(numbers, sumv):
    n = len(numbers)
    L = matrix.zero(n + 1)
    for row, x in enumerate(numbers):
        L[row, row] = 2
        L[row, -1] = x
    L[-1, :] = 1
    L[-1, -1] = sumv
    res = L.LLL()
    for i in range(n):
        now = res[i][:-1]
        # print(now)
        fail = False
        answer = 0
        for i in range(n):
            if now[i] == -1:
                answer |= 1 << i
            elif now[i] != 1:
                fail = True
                break
        if not fail:
            return answer
    return -1

with open('output.txt', 'r') as f:
    publicKey = eval(f.readline().split(':')[-1])
    encrypted = eval(f.readline().split(':')[-1])

m = solve_backpack(publicKey, encrypted)
flag  = long_to_bytes(m).decode()
print(flag)
