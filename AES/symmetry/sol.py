import requests
from binascii import unhexlify

# Fetch the encrypted flag
resp = requests.get("https://aes.cryptohack.org/symmetry/encrypt_flag/").json()
combined = resp['ciphertext']
iv      = unhexlify(combined[:32])
ct_flag = unhexlify(combined[32:])

# Ask for keystream by encrypting zeroes under the same IV
zeros = b'\x00' * len(ct_flag)
url = f"https://aes.cryptohack.org/symmetry/encrypt/{zeros.hex()}/{iv.hex()}/"
resp2 = requests.get(url).json()
keystream = unhexlify(resp2['ciphertext'])

# Recover and print the flag
flag = bytes(a ^ b for a, b in zip(ct_flag, keystream))
print(flag.decode())
