# Transition table for Jensen's polyomino enumeration algorithm.
# keys: (modify_to, lower, upper)
# values: (operation, new_lower, new_upper)
TRANSITION_TABLE = {
    # modify_to = 0 (unoccupied cell)
    (0, 0, 0): ("blank", 0, 0),
    (0, 0, 1): ("blank", 0, 1),
    (0, 0, 2): ("blank", 0, 2),
    (0, 0, 3): ("blank", 0, 3),
    (0, 0, 4): ("blank", 0, 4),

    (0, 1, 0): ("impossible", 0, 0), #add operation verified in control loop, otherwise it's invalid
    (0, 1, 1): ("impossible", 0, 0),
    (0, 1, 2): ("impossible", 0, 0),
    (0, 1, 3): ("impossible", 0, 0),
    # (0, 1, 4): ("impossible", 0, 0), # should never reach this state

    (0, 2, 0): ("over-line", 0, 0),
    (0, 2, 1): ("over-line", 0, 1),
    (0, 2, 2): ("over-line", 0, 2),
    (0, 2, 3): ("blank", 0, 2),
    (0, 2, 4): ("blank", 0, 1),

    (0, 3, 0): ("blank", 0, 0),
    (0, 3, 1): ("blank", 0, 1),
    (0, 3, 2): ("blank", 0, 2),
    (0, 3, 3): ("blank", 0, 3),
    (0, 3, 4): ("blank", 0, 4),

    (0, 4, 0): ("over-line", 0, 0),
    (0, 4, 1): ("over-line", 0, 1),
    (0, 4, 2): ("over-line", 0, 2),
    (0, 4, 3): ("over-line", 0, 3),
    # (0, 4, 4): ("impossible", 0, 0), # should never reach this state

    # modify_to = 1 (occupied cell)
    (1, 0, 0): ("blank", 1, 0),
    (1, 0, 1): ("blank", 2, 4),
    (1, 0, 2): ("blank", 2, 3),
    (1, 0, 3): ("blank", 3, 3),
    (1, 0, 4): ("blank", 3, 4),

    (1, 1, 0): ("blank", 1, 0),
    (1, 1, 1): ("blank", 2, 4),
    (1, 1, 2): ("blank", 2, 3),
    (1, 1, 3): ("blank", 3, 3),
    # (1, 1, 4): ("impossible", 0, 0), # should never reach this state

    (1, 2, 0): ("blank", 2, 0),
    (1, 2, 1): ("blank", 2, 3),
    (1, 2, 2): ("hat", 2, 3),
    (1, 2, 3): ("impossible", 2, 3),
    (1, 2, 4): ("impossible", 2, 4),

    (1, 3, 0): ("blank", 3, 0),
    (1, 3, 1): ("blank", 3, 3),
    (1, 3, 2): ("hat", 3, 3),
    (1, 3, 3): ("impossible", 3, 3),
    (1, 3, 4): ("impossible", 3, 4),

    (1, 4, 0): ("blank", 4, 0),
    (1, 4, 1): ("blank", 3, 4),
    (1, 4, 2): ("blank", 3, 3),
    (1, 4, 3): ("hat", 3, 3),
    # (1, 4, 4): ("impossible", 0, 0) # should never reach this state
}
