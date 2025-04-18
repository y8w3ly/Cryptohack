import json
import numpy as np
from Crypto.Util.number import long_to_bytes

traces = np.array(json.load(open('collected_data.txt')), dtype=float)
avg_leak = traces.mean(axis=0)
sorted_vals = np.sort(avg_leak)
gaps = np.diff(sorted_vals)
idx = np.argmax(gaps)
threshold = (sorted_vals[idx] + sorted_vals[idx+1]) / 2
bits = (avg_leak > threshold).astype(int).tolist()
bits.reverse()
d = 0
for b in bits:
    d = (d << 1) | b
flag = long_to_bytes(d, (len(bits) + 7) // 8)
print(flag.decode())

