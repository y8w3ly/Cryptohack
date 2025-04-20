import hashlib
import json
from Crypto.Cipher import AES

def main():
    # Load data from data.json
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    pub_key = [bytes.fromhex(s) for s in data['public_key']]
    message1 = data['message'].encode()
    signature1 = [bytes.fromhex(s) for s in data['signature']]
    iv = bytes.fromhex(data['iv'])
    enc = bytes.fromhex(data['enc'])
    
    # Compute data_hash1 and data_hash2
    data_hash1 = hashlib.sha256(message1).digest()
    data_hash2 = hashlib.sha256(b"Sign for flag").digest()
    
    h1 = list(data_hash1)
    h2 = list(data_hash2)
    
    # Check if all h2[i] <= h1[i]
    for i in range(len(h1)):
        if h2[i] > h1[i]:
            raise ValueError(f"h2[{i}] > h1[{i}], cannot forge signature")
    
    # Forge signature2
    signature2 = []
    for i in range(len(signature1)):
        current = signature1[i]
        delta = h1[i] - h2[i]
        for _ in range(delta):
            current = hashlib.sha256(current).digest()
        signature2.append(current)
    
    # Extract AES key (first byte of each signature element)
    aes_key = bytes([s[0] for s in signature2])
    
    # Decrypt the flag
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(enc)
    
    # Remove PKCS#7 padding
    padding_length = flag[-1]
    flag = flag[:-padding_length]
    
    print(flag.decode())

if __name__ == "__main__":
    main()