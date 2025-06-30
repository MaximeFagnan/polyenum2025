import sys
import os

# Add the path to python_implementation/ explicitly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enumerator import PolyominoEnumerator
from generating_function import GeneratingFunction
from signature import Signature
from signatureGF_pair import SignatureGFPair
from signature_table import SignatureTable


# Testing cell
def test_signature_class():
    states = [4,0,4,3,2,0,2,0,1]
    signature_test1 = Signature(states)
    signature_test2 = Signature(states, True, True)

    print(signature_test1.__repr__(multiline = False))
# test_signature_class()

def test_signature_table():
    # Define some signatures
    sig1 = Signature([4, 3, 2], touches_top=True)
    sig2 = Signature([4, 3, 2], touches_top=True)  # equal to sig1
    sig3 = Signature([0, 1, 0], touches_top=True)

    # Define generating functions
    gf1 = GeneratingFunction({1: 2})
    gf2 = GeneratingFunction({2: 3})
    gf3 = GeneratingFunction({0: 5})

    # Create pairs
    pair1 = SignatureGFPair(sig1, gf1)
    pair2 = SignatureGFPair(sig2, gf2)  # same signature, should combine
    pair3 = SignatureGFPair(sig3, gf3)  # different signature

    # Initialize table and add
    table = SignatureTable()
    table.add(pair1)
    table.add(pair2)
    table.add(pair3)

    # Check the combined result for sig1
    combined = table.mapping[sig1]
    assert combined.terms == {1: 2, 2: 3}, f"Unexpected terms: {combined.terms}"

    # Check sig3 stored correctly
    assert table.mapping[sig3].terms == {0: 5}, "sig3 GF incorrect"

    # Optional: Print table
    print("Signature Table contents:")
    print(table.__repr__(multiline = True))

    print("✅ All tests passed.")
# test_signature_table()

def test_signature_transitions():
    # Test 1: Blank transition (0 -> 0, blank operation)
    sig = Signature([1, 0, 0], touches_top=True)
    gf = GeneratingFunction({1: 1})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=1, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [1, 0, 0]
    assert new_pair.generating_function.terms == {1: 1}

    # Test 2: Blank transition (2 -> 2, blank operation)
    sig = Signature([4, 3, 2])
    gf = GeneratingFunction({4: 7})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=1, modify_to=1)
    assert new_pair is not None
    assert new_pair.signature.states == [4, 3, 2]
    assert new_pair.generating_function.terms == {5: 7}

    # Test 3: Blank transition (0 -> 3, blank operation)
    sig = Signature([4, 0, 0, 2])
    gf = GeneratingFunction({6: 1})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=1, modify_to=1)
    assert new_pair is not None
    assert new_pair.signature.states == [4, 3, 0, 2]
    assert new_pair.generating_function.terms == {7: 1}

    # Test 4.1: Hat operation (upwards)
    sig = Signature([4, 0, 4, 3, 0, 2, 2], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({1: 1})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=6, modify_to=1)
    assert new_pair is not None
    assert new_pair.signature.states == [4, 0, 3, 3, 0, 3, 2]
    assert new_pair.generating_function.terms == {2: 1}  # multiplied by x

    # Test 4.2: Hat operation (downwards)
    sig = Signature([ 4, 3, 4, 3, 2, 0, 2], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({1: 2})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=2, modify_to=1)
    assert new_pair is not None
    assert new_pair.signature.states == [ 4, 3, 3, 3, 3, 0, 2]
    assert new_pair.generating_function.terms == {2: 2}

    # Test 5.1 : Over-line (upwards and turn to isolated)
    sig = Signature([4, 0, 4, 3, 2, 0, 2, 0], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({0: 5})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=6, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [1, 0, 4, 3, 2, 0, 0, 0]
    assert new_pair.generating_function.terms == {0: 5}

    # Test 5.2 : Over-line (upwards and change intermediate site)
    sig = Signature([4, 3, 3, 0, 4, 3, 2, 2, 0], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({0: 5})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=7, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [4, 3, 2, 0, 4, 3, 2, 0, 0]
    assert new_pair.generating_function.terms == {0: 5}

    #  Test 5.3: Over-line (downward and turn to isolated)
    sig = Signature([0, 0, 4, 0, 0, 2, 0, 0], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({0: 3})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=2, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [0, 0, 0, 0, 0, 1, 0, 0]
    assert new_pair.generating_function.terms == {0: 3}

    # Test 5.4: Over-line (downward and change intermediate site)
    sig = Signature([0, 0, 4, 3, 3, 2, 0, 0], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({0: 2})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=2, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [0, 0, 0, 4, 3, 2, 0, 0]
    assert new_pair.generating_function.terms == {0: 2}

    # Test 5.5: Over-line (downward and change intermediate site and nesting)
    sig = Signature([4, 0, 4, 3, 3, 2, 0, 3, 3, 2], touches_top=True, touches_bottom=True)
    gf = GeneratingFunction({0: 2})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=0, modify_to=0)
    assert new_pair is not None
    assert new_pair.signature.states == [0, 0, 4, 3, 3, 2, 0, 4, 3, 2]
    assert new_pair.generating_function.terms == {0: 2}

    # Test 6: Impossible case
    sig = Signature([1, 1, 1], touches_top=True)
    gf = GeneratingFunction({0: 2})
    pair = SignatureGFPair(sig, gf)
    result = pair.transition(row=1, modify_to=0)
    assert result is None

    print("✅ All signature transition tests passed.")
# test_signature_transitions()

def test_can_add():
    # Test 1: Valid add condition – only row 2 is 1
    sig = Signature([0, 0, 1, 0, 0], touches_top=True, touches_bottom=True)
    assert sig.can_add(2) == True, "Test 1 failed: should allow add at row 2"

    # Test 2: Invalid – multiple 1s
    sig = Signature([1, 0, 1, 0, 0], touches_top=True, touches_bottom=True)
    assert sig.can_add(2) == False, "Test 2 failed: should not allow add, multiple 1s"

    # Test 3: Invalid – 1 at wrong row
    sig = Signature([0, 0, 1, 0, 0], touches_top=True, touches_bottom=False)
    assert sig.can_add(1) == False, "Test 3 failed: should not allow add, 1 not at row 1"
    assert sig.can_add(2) == False, "Test 3 failed: should allow not add at row 2"

    print("✅ All can_add tests passed.")
# test_can_add()

def test_generating_function_min_exp_direct():
    # Test 1: Single term GF
    gf = GeneratingFunction({3: 5})
    assert gf.min_exp == 3, f"Expected min_exp = 3, got {gf.min_exp}"

    # Test 2: Multiple term GF
    gf = GeneratingFunction({5: 1, 2: 9, 9: 4})
    assert gf.min_exp == 2, f"Expected min_exp = 2, got {gf.min_exp}"
# test_generating_function_min_exp_direct()

def test_generating_function_min_exp_transition():
    # Test 3: Transition with multiply_by_x (occupied cell)
    sig = Signature([0, 1])
    gf = GeneratingFunction({1: 1})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=0, modify_to=1)  # should multiply GF by x
    assert new_pair is not None
    assert new_pair.generating_function.min_exp == 2, \
        f"Expected min_exp = 2, got {new_pair.generating_function.min_exp}"

    # Test 4: Transition with no x multiplication (empty cell)
    sig = Signature([4, 2])
    gf = GeneratingFunction({3: 1, 4: 3})
    pair = SignatureGFPair(sig, gf)
    new_pair = pair.transition(row=0, modify_to=0)
    assert new_pair is not None
    assert new_pair.generating_function.min_exp == 3, \
        f"Expected min_exp = 3, got {new_pair.generating_function.min_exp}"
# test_generating_function_min_exp_transition()