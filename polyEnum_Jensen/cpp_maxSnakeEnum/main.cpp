#include "include/Signature.hpp"
#include <cassert>
#include "include/transition_table.hpp"
#include "include/MaxAreaCounter.hpp"
#include "include/SignatureCounter_pair.hpp"

// functions described below
void signature_map_manipulation_example();
void test_mirror_clone_lookup();
void test_signature_vector_constructor();
void test_maxAreaCounter();
void test_signature_transition();


int main() {
    //signature_map_manipulation_example();
    //test_mirror_clone_lookup();
    //test_signature_vector_constructor();
    //test_maxAreaCounter();
    //test_signature_transition();

    return 0;
}


void signature_map_manipulation_example(){
    // Create an unordered_map with Signature as key and size_t as value
    std::unordered_map<Signature, size_t, SignatureHasher> sig_map;

    // Example: build a signature of height 3
    Signature sig(3);
    sig.set_row(0, 4, false);  // Row 0: state 1, left not occupied
    sig.set_row(1, 3, true);   // Row 1: state 3, left occupied
    sig.set_row(2, 2, false);  // Row 2: state 0, left not occupied

    sig.compute_hash();  // Must be called before inserting into the map!

    // Insert into the map with count = 42
    Signature mirror_1 = sig.mirror_clone();
    sig_map[mirror_1] = 170;
    Signature possible_clone = Signature(3);
    possible_clone.set_row(0, 4, false);  // Row 0: state 1, left not occupied
    possible_clone.set_row(1, 3, true);   // Row 1: state 3, left occupied
    possible_clone.set_row(2, 2, false);  // Row 2: state 0, left not occupied
    possible_clone.compute_hash();

    /*for (int i=0; i<3; i++){
        std::cout << "mirror_1       state: " << int(mirror_1.get_row(i).state) << "\n";
        std::cout << "possible clone state: " << int(possible_clone.get_row(i).state) << "\n";
        std::cout << "mirror_1       occ: " << bool(mirror_1.get_row(i).leftOccupied) << "\n";
        std::cout << "possible clone occ: " << bool(possible_clone.get_row(i).leftOccupied) << "\n";

        std::cout << "hashes: " << mirror_1.cached_hash << " vs " << possible_clone.cached_hash << "\n";
    }*/
}

void test_mirror_clone_lookup() {
    // Create original signature
    Signature sig1(3);
    sig1.set_row(0, 1, true);
    sig1.set_row(1, 3, true);
    sig1.set_row(2, 4, false);
    sig1.compute_hash();

    Signature sig2(3);
    sig2.set_row(0, 2, false);
    sig2.set_row(1, 3, true);
    sig2.set_row(2, 1, true);
    sig2.compute_hash();

    // Insert into map
    std::unordered_map<Signature, size_t, SignatureHasher> sig_map;
    sig_map[sig1] = 999;

    // Generate mirror
    Signature mirrored = sig1.mirror_clone();
    mirrored.compute_hash(); // Required for map lookup
    sig_map[mirrored] = 2;

    // Check if mirrored is found in map
    if (sig_map.count(sig2)) {
        std::cout << " Mirror found in map \n";
    }
    else {
        std::cout << " Mirror not found in map.\n";
    }

    for (int i = 0; i < 3; i++) {
        std::cout << "sig2     state: " << int(sig2.get_row(i).state) << "\n";
        std::cout << "mirrored state: " << int(mirrored.get_row(i).state) << "\n";
        std::cout << "sig 2    occ: " << bool(sig2.get_row(i).leftOccupied) << "\n";
        std::cout << "mirror   occ: " << bool(mirrored.get_row(i).leftOccupied) << "\n";

        std::cout << "hashes: " << sig2.cached_hash << " vs " << mirrored.cached_hash << "\n";
    }
}

void test_signature_vector_constructor() {
    std::vector<RowEntry> input = {
        RowEntry(1, false),
        RowEntry(2, true),
        RowEntry(3, false)
    };

    Signature sig(input);

    // Check height
    assert(sig.height == static_cast<int>(input.size()));

    // Check each row
    for (size_t i = 0; i < input.size(); ++i) {
        RowEntry actual = sig.get_row(i);
        assert(actual == input[i]);
    }

    std::vector<uint8_t> states = sig.get_states();

    for (size_t i = 0; i < input.size(); ++i) {
        std::cout << int(states[i]) << int(input[i].state) << "\n";
        assert(states[i] == input[i].state), "wow";
    }

    std::cout << "test_signature_vector_constructor passed.\n";
}

void test_maxAreaCounter() {
    MaxAreaCount a(5, 3);
    MaxAreaCount b(4, 10);
    MaxAreaCount c = a + b; // c = a (because a.max_area > b.max_area)
    c.increase_max_area();  // Only c changes

    std::cout << "a: " << a.max_area << "\n"; // still 5
    std::cout << "c: " << c.max_area << "\n"; // now 6
}


void test_signature_transition() {
    // Construct original signature: "43012042"
    std::vector<RowEntry> row_entries = {
        {4, true}, // row 0 (bottom-most)
        {3, false},
        {0, false},
        {1, false},
        {2, true},
        {0, false},
        {4, false},
        {2, false}  // row 7 (top-most)
    };
    Signature sig(row_entries);

    // Initialize MaxAreaCount with area = 25
    MaxAreaCount mac = MaxAreaCount(25,17);

    SignatureCounterPair scp(sig, mac);

    // Test transition at row = 4 (index of the red 't') with modify_to = 1 (add a cell)
    std::optional<SignatureCounterPair> result = scp.transition(4, 0);

    if (!result.has_value()) {
        std::cout << "Transition returned nullopt (invalid or pruned)." << std::endl;
        return;
    }

    // Print the resulting signature
    const Signature& new_sig = result->signature;
    std::cout << "New Signature Row Entries (top to bottom):" << std::endl;
    for (int i = 0; i < new_sig.height; ++i) {
        const RowEntry& row = new_sig.get_row(i);
        std::cout << "Row " << i << ": (leftOccupied=" << (int)row.leftOccupied
            << ", state=" << (int)row.state << ")" << std::endl;
    }

    // Print new max area
    std::cout << "NEW Max Area: " << result->maxAreaCount << std::endl <<std::endl;
    

    //old sig
    std::cout << "OLD Signature Row Entries (top to bottom):" << std::endl;
    for (int i = 0; i < sig.height; ++i) {
        const RowEntry& row = sig.get_row(i);
        std::cout << "Row " << i << ": (leftOccupied=" << (int)row.leftOccupied
            << ", state=" << (int)row.state << ")" << std::endl;
    }

    // Print old max area
    std::cout << "OLD Max Area: " << scp.maxAreaCount << std::endl;
}