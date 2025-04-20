from Crypto.Cipher import AES
import hashlib
import random

with open("words") as f:
    words = [w.strip() for w in f.readlines()]

FLAG = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"   # Encrypted FLAG => to decrypt

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}

import codecs
f = ""
for word in words:
  passHash = hashlib.md5(word.encode()).hexdigest()
  dec = decrypt(FLAG, passHash)
  try:
      f = codecs.decode(dec['plaintext'],'hex').decode('ascii')
      print(f)
      break
  except:
      continue
