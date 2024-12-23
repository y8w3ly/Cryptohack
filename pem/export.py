from Crypto.PublicKey import RSA

with open('./key.pem', 'r') as f:
	key = f.read()

public = RSA.import_key(key)

n = public.n

e = public.e

print(e,'   ||  ',n)
