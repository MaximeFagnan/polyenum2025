# SignatureTable
# ==============
#
# This class manages a collection of (Signature, GeneratingFunction) pairs during the execution
# of Iwan Jensen's polyomino enumeration algorithm.
#
# The table represents the current state of the dynamic programming process:
# it associates each unique boundary Signature with its corresponding GeneratingFunction.
# This class is wrapper for the dictionary with an added symmetry merging optimization function

from signatureGF_pair import SignatureGFPair

class SignatureTable:
    def __init__(self):
        self.mapping = {}

    def add(self, pair: SignatureGFPair):
        if pair.signature in self.mapping:
            self.mapping[pair.signature] += pair.generating_function
        else:
            self.mapping[pair.signature] = pair.generating_function

    # convenience function
    def items(self):
        return self.mapping.items()

    def __repr__(self, multiline = False):
        return "\n".join(f"{sig.__repr__(multiline = multiline)} -> {gf}" for sig, gf in self.mapping.items())

    def merge_mirrored_signatures(self):
        new_mapping = {}
        seen = set()

        for sig, gf in self.mapping.items():
            if sig in seen:
                continue

            mirrored_sig = sig.mirrored()
            seen.add(sig)
            seen.add(mirrored_sig)

            if mirrored_sig in self.mapping and mirrored_sig != sig:
                merged_gf = gf + self.mapping[mirrored_sig]
                new_mapping[sig] = merged_gf
            else:
                new_mapping[sig] = gf  # either symmetric or mirror not present

        self.mapping = new_mapping