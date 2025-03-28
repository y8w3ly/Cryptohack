from Crypto.PublicKey import RSA

key = open("pek.pem").read()
print(RSA.import_key(key).d)
