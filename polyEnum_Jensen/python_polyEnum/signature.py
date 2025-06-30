class Signature:

    #This initializer makes a signature from a set of states, it supposes that
        # these states are correct
    def __init__(self, states, touches_top = False, touches_bottom = False):
        self.length = len(states)
        self.states = tuple(states)
        self.touches_top : bool = touches_top 
        self.touches_bottom: bool = touches_bottom
        self._hash = self.compute_hash()

    # # Turns out we never have to clone a signature (it should be immutable anyways)
    # def clone(self):
    #     return Signature(self.states, self.touches_top, self.touches_bottom)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Signature):
            return False
        if self._hash != other._hash:
            return False
        return (self.states == other.states and
                self.touches_top == other.touches_top and
                self.touches_bottom == other.touches_bottom)

    def compute_hash(self):
        base_hash = hash(self.states)
        flags_hash = (self.touches_top << 1) | self.touches_bottom
        return hash((base_hash, flags_hash))

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self, multiline : bool = True) -> str:
        repr_list = []

        touch_top_symbol = ""
        if self.touches_top:
            if multiline:
                touch_top_symbol = "↧"
            else:
                touch_top_symbol = "↦"
        touch_bottom_symbol = ""
        if self.touches_bottom:
            if multiline:
                touch_bottom_symbol = "↥"
            else:
                touch_bottom_symbol = "↤"

        # states[0] + touches_top flag
        if multiline:
            repr_list.append(f"{self.states[0]}{touch_top_symbol}")
        else:
            repr_list.append(f"{touch_top_symbol}{self.states[0]}")
        # states[1:-1] on one line
        repr_list += list(map(str, self.states[1:-1]))
        # states[-1] + touches_bottom flag
        if self.length > 1:
            repr_list.append(f"{self.states[-1]}{touch_bottom_symbol}")

        if multiline:
            return "\n".join(repr_list)
        else:
            return " ".join(repr_list)

    def can_add(self, row):
        """ Check if this signature's transition is a valid "add" transition
        when setting row to 0."""
        # quick check, not likely to be true
        if self.states[row] != 1:
            return False
        for row_index, state in enumerate(self.states):
            if row_index == row:
                pass # already verified
            else:
                if state != 0:
                    return False
        # The signature needs to touch the bottom and the top
        return self.touches_top and self.touches_bottom

    def mirrored(self):
        # Swap 2 ↔ 4 to preserve matching semantics when vertically flipped
        swap = {0: 0, 1: 1, 2: 4, 3: 3, 4: 2}
        mirrored_states = [swap[state] for state in reversed(self.states)]
        return Signature(mirrored_states, self.touches_bottom, self.touches_top)

    def calculate_n_add(self, column, row_after_kink):
        #column refers to which column is being worked on
        assert 0 <= row_after_kink < self.length

        # first calculate n_w, where n_w is number of cells to reach width=length
        n_w = 0
        for row, state in enumerate(self.states[:row_after_kink+1]):
            if row < row_after_kink:
                if state > 0:
                    n_w = self.length - column
                    break
            else:
                n_w = self.length - column + 1
                break #unnecessary because we truncated states

        # now calculate n_h which is necessary number of polyominoes to reach top and bottom
        n_h = 0
        if not self.touches_top:
            # find highest occupied cell
            for row, state in enumerate(self.states):
                if state > 0:
                    n_h += row
                    break
        if not self.touches_bottom:
            # find lowest occupied cell
            for row, state in enumerate(reversed(self.states)):
                if state > 0:
                    n_h += row
                    break

        # now calculate n_c which is the number of cells required to connect the different components
        n_c = 0
        # we could choose to have n_c be too small if it makes it simpler.