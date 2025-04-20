import requests

def fetch_encrypted_data():
    url = "http://aes.cryptohack.org/bean_counter/encrypt/"
    response = requests.get(url)
    return response.json()['encrypted']

def xor_bytes(byte_array1, byte_array2):
    return bytes(x ^ y for x, y in zip(byte_array1, byte_array2))

def main():
    png_header = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])
    encrypted_data = bytes.fromhex(fetch_encrypted_data())

    keystream = xor_bytes(png_header, encrypted_data[:len(png_header)])

    decrypted_data = xor_bytes(encrypted_data, keystream * (len(encrypted_data) // len(keystream)))

    with open('bean_counter.png', 'wb') as file:
        file.write(decrypted_data)

if __name__ == "__main__":
    main()
