from signature import Signature
from transitions_table import TRANSITION_TABLE

class SignatureGFPair:
    def __init__(self, signature, generating_function):
        self.signature = signature
        self.generating_function = generating_function

    # def __eq__(self, other):
    #     return self.signature == other.signature

    # def __hash__(self):
    #     return hash(self.signature)

    def __repr__(self):
        return f"{self.signature} -> {self.generating_function}"

    def __add__(self, other):
        assert self.signature == other.signature, "Signatures must match for addition"
        new_generating_function = self.generating_function + other.generating_function
        return SignatureGFPair(self.signature, new_generating_function)

    def transition(self, row, modify_to):
        lower = self.signature.states[row]
        upper = self.signature.states[row-1] if row > 0 else 0
        key = (modify_to, lower, upper)

        if key not in TRANSITION_TABLE:
            return None  # skip invalid transitions

        operation, new_lower, new_upper = TRANSITION_TABLE[key]

        if operation == "impossible":
            return None  # no valid transition

        # Copy the old signature and modify it
        new_signature = None
        new_states = list(self.signature.states)
        touched_top = self.signature.touches_top
        touched_bottom = self.signature.touches_bottom
        if row == 0 and modify_to == 1:
            touched_top = True
        if row == len(new_states) - 1 and modify_to == 1:
            touched_bottom = True
        new_gf = self.generating_function.clone()
        if modify_to == 1:
            new_gf.multiply_by_x()
            if new_gf.is_empty(): return None   # too big of a polyomino to track growth.

        # blank operation, just change states and nothing else
        if operation == "blank":
            new_states[row] = new_lower
            if row > 0:
                new_states[row-1] = new_upper

            new_signature = Signature(new_states, touched_top, touched_bottom)

        # over-line operation
        elif operation == "over-line":
            new_states[row] = new_lower  # which is 0

            if lower == 2:
                count_2 = 1
                count_4 = 0
                for i in range(row-1, -1, -1):
                    if new_states[i] == 2:
                        count_2 += 1
                    if new_states[i] == 4:
                        count_4 += 1
                    """If we find a '3' and the current nesting counts match
                    (minus one for the removed 2), then we can turn it into 2"""
                    if new_states[i] == 3  and (count_2-1 == count_4):
                        new_states[i] = 2 # it becomes the new 'first' site in the chain
                        break
                    """ If the count balances, then we just hit a balancing '4'
                    and there are only 2 cells connected to the signature"""
                    if count_2 == count_4:
                        new_states[i] = 1 # this is now an isolated occupied site
                        break

            elif lower == 4:
                count_4 = 1
                count_2 = 0
                for i in range(row+1, len(new_states)):
                    if new_states[i] == 2:
                        count_2 += 1
                    if new_states[i] == 4:
                        count_4 += 1
                    """If we find a '3' and the current nesting counts match
                    (minus one for the removed 2), then we can turn it into 2"""
                    if new_states[i] == 3  and (count_4-1 == count_2):
                        new_states[i] = 4 # it becomes the new 'first' site in the chain
                        break
                    """ If the count balances, then we just hit a balancing '2'
                    and there are only 2 cells connected to the signature"""
                    if count_2 == count_4:
                        new_states[i] = 1 # this is now an isolated occupied site
                        break
            new_signature = Signature(new_states, touched_top, touched_bottom)

        # hat operation
        elif operation == "hat":
            assert row > 0, "Should not be doing hat if row = 0"

            if new_states[row] in {2,3}:
                new_states[row] = new_lower
                new_states[row - 1] = 3  # upper site becomes intermediate

                # Scan upward from to find the matching 4
                count_2 = 0
                count_4 = 0
                for i in range(row-1,-1,-1):
                    if new_states[i] == 2:
                        count_2 += 1
                    elif new_states[i] == 4:
                        count_4 += 1
                        if (count_2 + 1) == count_4:
                            new_states[i] = 3  # last site also becomes intermediate
                            break

            if new_states[row] == 4 :
                new_states[row] = 3 # new site becomes intermediary

                # Scan downwards to find the matching 2
                count_2 = 0
                count_4 = 0
                for i in range(row+1,len(new_states)):
                    if new_states[i] == 2:
                        count_2 += 1
                        if count_2 == (count_4 + 1):
                            new_states[i] = 3  # first site also becomes intermediate
                            break
                    elif new_states[i] == 4:
                        count_4 += 1
            new_signature = Signature(new_states, touched_top, touched_bottom)

        # add operation
        assert operation != "add", "Add operation should not be reached because we manage it in control loop."

        # Return new pair
        assert new_signature is not None, "New signature should not be None"
        return SignatureGFPair(new_signature, new_gf)
