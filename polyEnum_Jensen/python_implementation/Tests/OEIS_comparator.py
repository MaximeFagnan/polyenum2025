import sys
import os
import time

# Add the path to python_implementation/ explicitly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests  # type: ignore
from enumerator import PolyominoEnumerator

n=23 # Change as desired....
# 17 is executed in more or less 3.5 seconds on computer.
# 19 is executed in more or less 9.6 seconds on computer.
# 21 is executed in more or less 31 seconds on computer.
# 23 is executed in more or less 104 seconds on computer.
# Without pruning for empty signatures: 29 is executed in more or less 90 minutes (5400 seconds) on computer. Pruning could shave 1/4 to 1/3 of time off.

def fetch_fixed_polyomino_counts(n_max):
    """
    Fetch the fixed polyomino counts from OEIS (A001168) up to n_max.
    Returns a list counts[1..n_max].
    """
    url = "https://oeis.org/A001168/b001168.txt"
    resp = requests.get(url)
    resp.raise_for_status()

    counts = [None] * (n_max + 1)
    for line in resp.text.splitlines():
        if line.startswith("#"):
            continue
        parts = line.split()
        if not parts:
            continue
        i, val = int(parts[0]), int(parts[1])
        if i <= n_max:
            counts[i] = int(val)
    return counts

poly_enum = PolyominoEnumerator(n)
start_time = time.time()
gf = poly_enum.run()
time_diff = time.time() - start_time

# enumerate only coefficients whose exponents are lower than n
print(f"\nGenerating function: {gf}")
print(f"program runtime: {time_diff}")

# Verify the program
counts = fetch_fixed_polyomino_counts(n)
if list(gf.terms.values()) == counts[:n+1]:
    print("Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt\n")
assert list(gf.terms.values()) == counts[:n+1],\
    "a_n coefficients do not match OEIS coefficients at https://oeis.org/A001168/b001168.txt"
# # Line by line verification
# for i, coeff in enumerate(gf.terms.values()):
#     if i > n:
#         break
#     if coeff == counts[i]:
#         print(f"{i}: {coeff} COUNTED CORRECTLY")
#     else:
#         print(f"{i}: {coeff} COUNTED INCORRECTLY")