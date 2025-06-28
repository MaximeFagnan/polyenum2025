class GeneratingFunction:
    def __init__(self, terms=None, max_degree = None, min_exp = None):
        self.terms = terms or {}  # {exponent: coefficient}
        self.max_degree = max_degree
        if min_exp is not None:
            self.min_exp = min_exp
        else:
            self.min_exp = min(self.terms) if self.terms else 0

    def __add__(self, other):
        assert self.max_degree == other.max_degree, "Mismatched degree bounds"
        result_terms = self.terms.copy()
        min_exp = min(self.min_exp, other.min_exp)
        for exp, coeff in other.terms.items():
            result_terms[exp] = result_terms.get(exp, 0) + coeff
        return GeneratingFunction(result_terms, self.max_degree, min_exp)

    def multiply_by_x(self):
        self.terms = {exp + 1: coeff for exp, coeff in self.terms.items()}
        # Delete last term if it's power is greater than max_degree
        if self.max_degree is not None and self.max_degree in self.terms:
            del self.terms[self.max_degree]
        self.min_exp += 1

    def __repr__(self):
        return " + ".join(f"{coeff}x^{exp}" for exp, coeff in sorted(self.terms.items()))

    def clone(self):
        return GeneratingFunction(self.terms.copy(), self.max_degree, self.min_exp)
    
    def is_empty(self):
        if len(self.terms) == 0: 
            return True
        else:
            return False

    # # We do not need to truncate because we dynamically manage max degree.
    # def truncate(self, max_n):
    #     """
    #     Remove all terms with exponent ≥ max_n (typically to keep area < n).
    #     This mutates the generating function in place.
    #     """
    #     self.terms = {exp: coeff for exp, coeff in self.terms.items() if exp < max_n}