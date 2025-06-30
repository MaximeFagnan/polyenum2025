import sys
import os
import time

# Add the path to python_implementation/ explicitly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests  # type: ignore
from enumerator import PolyominoEnumerator

for n in [23,25,27,29,31]:
    # n=23 # Change as desired....
    # 17 is executed in more or less 3.5 seconds on computer.
    # 19 is executed in more or less 9.6 seconds on computer.
    # 21 is executed in more or less 31 seconds on computer.
    # n = 23
    # program runtime: 95.09101414680481
    # Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt

    # n = 25
    # program runtime: 332.99668741226196 (5.5 mins)
    # Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt

    # n = 27
    # program runtime: 1113.291049003601 (19mins)
    # Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt

    # n = 29
    # program runtime: 3613.1580436229706 (1h)
    # Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt

    # n = 31
    # program runtime: 11418.793110847473 (3h10)
    # Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt


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
    # print(f"\nGenerating function: {gf}")
    print(f"n = {n}")
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