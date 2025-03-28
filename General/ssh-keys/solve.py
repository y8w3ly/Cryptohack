from Crypto.PublicKey import RSA

with open("key.pem", "rb") as f:
    key = RSA.import_key(f.read())

n = key.n
print(n)
