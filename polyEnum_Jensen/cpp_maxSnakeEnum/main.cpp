#include "include/Signature.hpp"

// ---------------------------------------------------------
// Example usage of signature
// ---------------------------------------------------------
int main() {
    // Create an unordered_map with Signature as key and size_t as value
    std::unordered_map<Signature, size_t, SignatureHasher> sig_map;

    // Example: build a signature of height 3
    Signature sig(3);
    sig.set_row(0, 1, false);  // Row 0: state 1, left not occupied
    sig.set_row(1, 3, true);   // Row 1: state 3, left occupied
    sig.set_row(2, 0, false);  // Row 2: state 0, left not occupied

    sig.compute_hash();  // Must be called before inserting into the map!

    // Insert into the map with count = 42
    sig_map.insert(std::pair<const Signature,size_t>(sig,42));

    auto it = sig_map.find(sig);
    // Try to find it again
    if (it != sig_map.end()) {
        std::cout << "Found: " << it->first.height << " -> " << it->second << std::endl;
    }
    else {
        std::cout << "Key not found!" << std::endl;
    }

    std::cout << sig_map.max_size();

    return 0;
}