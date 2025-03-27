from Crypto.Util.number import inverse

n = [5,11,17]
N = 935
a = [2,3,5]

def crt(n,N,a):
  x = 0
  for i in range(len(n)):
      ai = a[i]
      ni = N//n[i]
      x += ai * ni * inverse(ni,n[i])
  return x
x = crt(n,N,a)
print(f'x = {x}')
print(f'a = {x%N}') 


