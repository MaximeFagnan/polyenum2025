st(gf.terms.values()) == counts[:n+1]:
        print("Verification: a_n coefficients match OEIS coefficients at https://oeis.org/A001168/b001168.txt\n")
    assert list(gf.terms.values()) == counts[:n+1],\
        "