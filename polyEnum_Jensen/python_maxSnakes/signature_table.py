# SignatureTable
# ==============
#
# This class manages a collection of (Signature, GeneratingFunction) pairs during the execution
# of Iwan Jensen's polyomino enumeration algorithm.
#
# The table represents the current state of the dynamic programming process:
# it associates each unique boundary Signature with its corresponding GeneratingFunction.
# This class is wrapper for the dictionary with an added symmetry merging optimization function

from signature import Signature
from signatureCounter_pair import SignatureCounter_pair

class SignatureTable:
    def __init__(self):
        self.mapping = {}

    def add(self, pair: SignatureCounter_pair):
        if pair.signature in self.mapping:
            self.mapping[pair.signature] += pair.maxAreaCount
        else:
            self.mapping[pair.signature] = pair.maxAreaCount

    # convenience function
    def items(self):
        return self.mapping.items()

    def __repr__(self, multiline = False):
        return "\n".join(f"{sig.__repr__(multiline = multiline)} -> {ar_count}" for sig, ar_count in self.mapping.items())

    def merge_mirrored_signatures(self):
        new_mapping = {}
        seen = set()

        for sig, area_counter in self.mapping.items():
            if sig in seen:
                continue

            mirrored_sig = sig.mirrored()
            seen.add(sig)
            seen.add(mirrored_sig)

            if mirrored_sig in self.mapping and mirrored_sig != sig:
                merged_area_counter = area_counter + self.mapping[mirrored_sig]
                new_mapping[sig] = merged_area_counter
            else:
                new_mapping[sig] = area_counter  # either symmetric or mirror not present

        self.mapping = new_mapping