from Crypto.PublicKey import RSA

with open("key.der", "rb") as f:
    key = RSA.import_key(f.read())

# Extract the modulus (n)
n = key.n
print(n)
