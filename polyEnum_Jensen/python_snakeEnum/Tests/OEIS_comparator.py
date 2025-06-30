import sys
import os
import time

# Add the path to python_implementation/ explicitly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests  # type: ignore
from enumerator import PolyominoEnumerator

# from https://oeis.org/A182644/list
# I added the empty snake polyomino
counts = [1,1,2,6,14,34,82,198,470,1122,2662,6334,14970,35506,83734,198086,466314,1100818,2587634,6097830,14316402,33687146,79008870,185677006,435098774,1021404998,2391646494,5609151738,13125214770,30757286802,71928506630]

# n = 19 program runtime: 223s
for n in [11]:

    poly_enum = PolyominoEnumerator(n)
    start_time = time.time()
    gf = poly_enum.run()
    time_diff = time.time() - start_time

    # enumerate only coefficients whose exponents are lower than n
    # print(f"\nGenerating function: {gf}")
    print(f"n = {n}")
    print(f"program runtime: {time_diff}")

    # Verify the program
    if list(gf.terms.values()) == counts[:n+1]:
        print(gf)
        print("Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A182644/list \n")
    assert list(gf.terms.values()) == counts[:n+1],\
        "a_n coefficients do not match OEIS coefficients at https://oeis.org/A182644/list"
    # # Line by line verification
    # for i, coeff in enumerate(gf.terms.values()):
    #     if i > n:
    #         break
    #     if coeff == counts[i]:
    #         print(f"{i}: {coeff} COUNTED CORRECTLY")
    #     else:
    #         print(f"{i}: count={counts}, coeff={coeff} COUNTED INCORRECTLY")
