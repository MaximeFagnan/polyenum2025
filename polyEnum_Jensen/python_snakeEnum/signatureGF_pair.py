from signature import Signature
from transitions_table import TRANSITION_TABLE

class SignatureGFPair:
    def __init__(self, signature, generating_function):
        self.signature = signature
        self.generating_function = generating_function

    def __repr__(self):
        return f"{self.signature} -> {self.generating_function}"

    def __add__(self, other):
        assert self.signature == other.signature, "Signatures must match for addition"
        new_generating_function = self.generating_function + other.generating_function
        return SignatureGFPair(self.signature, new_generating_function)

    def transition(self, row, modify_to):
        sig: Signature = self.signature
        lower = sig.states[row]
        upper = sig.states[row-1] if row > 0 else 0
        
        # check transition in transition table
        key = (modify_to, lower, upper)
        if key not in TRANSITION_TABLE:
            return None  # skip invalid transitions
        else:
            operation, new_lower, new_upper = TRANSITION_TABLE[key]

        if operation == "impossible":
            return None  # no valid transition
        
        # check degree validity before proceding
        if modify_to == 1:
            # The following four lines show the 4 cells A,B,C,D that can influence degrees of Lower (L) and Upper (U).
            #   A
            #  BU
            # CL
            #  D
            lower_deg = 0
            upper_deg = 0
            if row >=2 and sig.states[row-2]: #cell A
                upper_deg +=1
            if row >= 1 and sig.predecessor_occupation[row-1]: # cell B
                lower_deg+=1
                upper_deg+=1
            if sig.predecessor_occupation[row]: # cell C
                lower_deg+=1
            if row + 1 < sig.length and sig.states[row+1] > 0 : # cell D
                lower_deg += 1 
            # degrees only matter if the cells are occupied
            if upper>=1 and upper_deg >=2 :
                return None
            if lower>=1 and lower_deg >=2 :
                return None 

        # Copy the old signature and modify it
        new_signature = None
        new_states = list(sig.states)
        touched_top = sig.touches_top
        touched_bottom = sig.touches_bottom
        # update edge touching      
        if row == 0 and modify_to == 1:
            touched_top = True
        if row == len(new_states) - 1 and modify_to == 1:
            touched_bottom = True
        # update gf
        new_gf = self.generating_function.clone()
        if modify_to == 1:
            new_gf.multiply_by_x()
            if new_gf.is_empty(): return None   # too big of a polyomino to track growth.
        # update predecessor_occupation
        new_predecessor_occupation = list(sig.predecessor_occupation)
        new_predecessor_occupation[row] = True if lower>=1 else False

        # blank operation, just change states and nothing else
        if operation == "blank":
            new_states[row] = new_lower
            if row > 0:
                new_states[row-1] = new_upper

            new_signature = Signature(new_states, new_predecessor_occupation, touched_top, touched_bottom)

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
            new_signature = Signature(new_states, new_predecessor_occupation, touched_top, touched_bottom)

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
            new_signature = Signature(new_states, new_predecessor_occupation, touched_top, touched_bottom)

        # add operation
        assert operation != "add", "Add operation should not be reached because we manage it in control loop."

        # Return new pair
        assert new_signature is not None, "New signature should not be None because those cases should return right away"
        return SignatureGFPair(new_signature, new_gf)
