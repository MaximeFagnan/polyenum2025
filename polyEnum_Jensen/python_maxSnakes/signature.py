class Signature:

    #This initializer makes a signature from a set of states and occupation status for predecessors, it supposes that:
        # these states are correct
    def __init__(self, states, predecessor_occupation = None):
        self.length = len(states)
        self.states = tuple(states)
        if predecessor_occupation is not None:
            assert len(states) == len(predecessor_occupation)
            self.predecessor_occupation = tuple(predecessor_occupation)
        else:
            self.predecessor_occupation = tuple([False])*self.length

    # # Turns out we never have to clone a signature (it should be immutable anyways)
    # def clone(self):
    #     return Signature(self.states, self.touches_top, self.touches_bottom)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Signature), f"Comparing a signature with a/an {type(other)} object"
        if hash(self) != hash(other):
            return False
        return (self.states == other.states and
                self.predecessor_occupation == other.predecessor_occupation)

    def __hash__(self):
        if not hasattr(self, '_hash'):
            self._hash = hash((self.states, self.predecessor_occupation))
        return self._hash

    def __repr__(self, multiline : bool = True) -> str:
        repr_list = []
        for i in range(self.length):
            state_str = str(self.states[i])
            pred_symbol = "X" if self.predecessor_occupation[i] else "0"
            repr_list.append(f"{pred_symbol} {state_str}")
        return "\n".join(repr_list) if multiline else " ".join(repr_list)

    def is_connected(self):
        # assumes correct state nesting with a 4 being seen before a 2.
        count = 0
        for state in self.states:
            if state==1:
                count += 1
                if count>1:
                    return False
            elif state == 4:
                count += 1
                if count>1:
                    return False
        return count == 1

    # # I don't think that we need to add a signature in this version of the alg because we don't have a global gf.
    # def can_add(self, row):
    #     """ Check if this signature's transition is a valid "add" transition
    #     when setting row to 0."""
    #     # quick check, not likely to be true
    #     if self.states[row] != 1:
    #         return False
    #     for row_index, state in enumerate(self.states):
    #         if row_index == row:
    #             pass # already verified
    #         else:
    #             if state != 0:
    #                 return False
    #     # The signature needs to touch the bottom and the top, will be ignored later
    #     return self.touches_top and self.touches_bottom

    def mirrored(self):
        # Swap 2 ↔ 4 to preserve matching semantics when vertically flipped
        state_swap_dictionnary = {0: 0, 1: 1, 2: 4, 3: 3, 4: 2}
        mirrored_states = [state_swap_dictionnary[state] for state in reversed(self.states)]
        # Switch order of predecessors.
        mirrored_predecessor_occupation = tuple(reversed(self.predecessor_occupation))
        return Signature(mirrored_states, mirrored_predecessor_occupation)