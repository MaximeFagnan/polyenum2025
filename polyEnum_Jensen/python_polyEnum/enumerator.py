# This is the polyomino enumerator class.
# initialize with a given n for which you want to enumerate and call the run
# method to get back the generating function of coefficients a_i up to i=n
from signature import Signature
from signatureGF_pair import SignatureGFPair
from signature_table import SignatureTable
from generating_function import GeneratingFunction


class PolyominoEnumerator:
    def __init__(self, n):
        self.n = n
        self.w_max = (n + 1) // 2 # might be issue for odd n's ?
        self.total_gf = GeneratingFunction({0:1},n+1)
        # self.run()

    def run(self) -> GeneratingFunction:
        self.total_gf = GeneratingFunction({0:1},self.n+1) # reset gf
        for w in range(1,self.w_max+1):
            self.run_for_w(w)
        # print(self.total_gf)
        return self.total_gf

    def run_for_w(self, w) -> None:
        # signature table with only an empty signature of height w
        initial_signature = Signature([0]*w)
        initial_gf = GeneratingFunction({0:1},self.n+1)
        initial_pair = SignatureGFPair(initial_signature, initial_gf)
        table = SignatureTable()
        table.add(initial_pair)

        L_max = 2*self.w_max - w + 1
        # for every necessary column
        for col in range(1, L_max + 1):
            # Just make sure you flush out the all 0 signature after first row
            if col == 2:
                table.mapping.pop(initial_signature)
            # Symmetry pruning proposed by Gill Barequet and Gil Ben-Shachar (2024)
            table.merge_mirrored_signatures()
            # Move the kink down row by row
            for row in range(w):
                # make a new table
                new_table = SignatureTable()
                for sig, gf in table.items():

                    #first, add an occupied cell, update signature table
                    sig_gf = SignatureGFPair(sig, gf)
                    new_pair = sig_gf.transition(row, 1)
                    if new_pair is not None:
                        new_table.add(new_pair)

                    # Second, add an unoccupied cell
                    # Option 1: It seals a valid polyomino
                    if sig.can_add(row):
                        length = col-1
                        if length < w:
                            pass # ignore based on symmetry
                        elif length == w:
                            self.total_gf += gf
                        elif length > w:
                            self.total_gf += gf + gf # double based on symmetry

                    # Option 2: It does not create a valid polyomino, update signature table
                    else:
                        new_pair = sig_gf.transition(row, 0)
                        if new_pair is not None:
                            new_table.add(new_pair)

                # Update the signatureGF table after every move of the kink
                table = new_table
        return # Does not return anything since the total_gf is a parameter of the class directly