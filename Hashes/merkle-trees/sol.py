from hashlib import sha256

def hash256(data):
    """Compute SHA256 hash of the input data."""
    return sha256(data).digest()

def merge_nodes(a, b):
    """Merge two nodes by concatenating and hashing."""
    return hash256(a + b)

def verify_merkle_tree(a_hex, b_hex, c_hex, d_hex, root_hex):
    """Verify if the computed root matches the given root."""
    # Convert hex strings to bytes
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    c = bytes.fromhex(c_hex)
    d = bytes.fromhex(d_hex)
    root = bytes.fromhex(root_hex)
    
    # Compute intermediate nodes
    left = merge_nodes(a, b)
    right = merge_nodes(c, d)
    
    # Compute the root
    computed_root = merge_nodes(left, right)
    
    # Return True if valid, False otherwise
    return computed_root == root

# Read and parse the output.txt data
challenges = []
with open("output.txt", "r") as f:
    for line in f:
        # Each line is a string representation of a list; evaluate it safely
        chal = eval(line.strip())
        challenges.append(chal)

# Verify each tree and collect bits
bits = []
for chal in challenges:
    a, b, c, d, root = chal
    is_valid = verify_merkle_tree(a, b, c, d, root)
    bits.append('1' if is_valid else '0')

# Convert binary string to ASCII flag
binary_string = ''.join(bits)
flag_int = int(binary_string, 2)
flag_hex = hex(flag_int)[2:]  # Remove '0x' prefix
flag = bytes.fromhex(flag_hex).decode('ascii')

print(flag)