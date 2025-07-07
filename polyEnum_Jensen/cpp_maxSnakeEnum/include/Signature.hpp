#pragma once
#include <iostream>
#include <stdlib.h>
#include <array>
#include <unordered_map>
#include <cstdint>
#include <cstddef> // for size_t
#include "RowEntry.hpp"
#include <cassert>
#include <ostream>


// Warning this, just setting a bigger row height might break mirror and == for uninitialized RowEntrys
constexpr int SIGNATURE_HEIGHT = 18; // Row height, needs to be changed to the specific height of a signature. 

// ---------------------------------------------------------
// Signature: represents the state of the boundary
// Contains up to SIGNATURE_HEIGHT RowEntry values, a height, and a cached hash
// ---------------------------------------------------------
struct Signature {
    std::array<RowEntry, SIGNATURE_HEIGHT> rows;
    int height;
    size_t cached_hash;
    //short int number_of_connected_components; Only useful at the end, overcalculation if we calculate for every sig.

    // Constructor initializes height and clears hash 
    // NOTE: THIS DOES NOT CREATE A HASH FOR THE SIGNATURE: UNSAFE!
    Signature(int h = 0) :
        height(h),
        cached_hash(0)//,
        //number_of_connected_components(0)
    {
        assert(h <= SIGNATURE_HEIGHT && "Too many row entries for Signature");
    }

    // blank signature
    static Signature blank(int height) {
        return Signature(std::vector<RowEntry>(height, RowEntry(0, false)));
    }

    // Overloaded constructor that receives a list of row_entries and computes hashes
    Signature(const std::vector<RowEntry>& row_entries)
        : height(static_cast<int>(row_entries.size())), cached_hash(0) {
        assert(row_entries.size() <= SIGNATURE_HEIGHT && "Too many row entries for Signature");
        assert(height <= SIGNATURE_HEIGHT && "Too many row entries for Signature");
        for (size_t i = 0; i < row_entries.size(); ++i) {
            rows[i] = row_entries[i];
        }
        compute_hash();
    }

    // Set the row at position `row` with state and leftOccupied flag
    void set_row(int row, uint8_t state, bool leftOccupied) {
        rows[row] = RowEntry(state, leftOccupied);
        // Lines to keep track of number of connected components from the get go.
        //if (state == 4 or state == 1 ) {
        //    number_of_connected_components += 1; //Starting a new component
        //    // Note that there is no safety for an invalid signature that has components that start and don't finish
        //}
    }

    // Retrieve the row at position `row`
    RowEntry get_row(size_t row) const {
        return rows[row];
    }

    // Retrieve all the row entries
    std::vector<RowEntry> get_row_entries() const {
        return std::vector<RowEntry>(rows.begin(), rows.begin() + height);
    }

    // Retrieve only the states
    std::vector<uint8_t> get_states() const {
        std::vector<uint8_t> states;
        for (int i = 0; i < height; ++i) {
            states.push_back(rows[i].state);
        }
        return states;
    }

    // Retrieve only the left_occupation
    std::vector<uint8_t> get_left_occupation() const {
        std::vector<uint8_t> left_occupation;
        for (int i = 0; i < height; ++i) {
            left_occupation.push_back(rows[i].leftOccupied);
        }
        return left_occupation;
    }

    // Boost-style hash combine
    // Mixes each row's 4-bit value into the final hash
    void compute_hash() {
        size_t h = 0;
        for (size_t i = 0; i < height; ++i) {
            const auto& r = rows[i];
            size_t entry = (r.state << 1) | r.leftOccupied;
            h = h ^ (entry + 0x9e3779b9 + (h << 6) + (h >> 2));
        }
        cached_hash = h;
    }

    bool is_connected() const {
        short nb_components = 0;
        for (int i = 0; i < height; i++) {
            int state = get_row(i).state;
            // go over all states and increase value when hitting an isolated component or when starting a component
            if (state == 1 or state == 4) {
                nb_components += 1;
                if (nb_components >= 2) return false;
            }
        }
        return nb_components == 1;
    }

    // Equality operator: compare row-by-row and height
    bool operator==(const Signature& other) const {
        if (height != other.height) return false;
        for (size_t i = 0; i < height; ++i) {
            const auto& a = rows[i];
            const auto& b = other.rows[i];
            if (a.state != b.state || a.leftOccupied != b.leftOccupied)
                return false;
        }
        return true;
    }

    Signature mirror_clone() const{
        // Swap the 2's and the 4's
        std::array<int, 5> state_swap = { 0, 1, 4, 3, 2 };
        Signature mirrored_sig = Signature(height);
        for (int i = height - 1; i >= 0; i--) {
            RowEntry row = rows[i];
            int state = state_swap[row.state];
            bool l_occupation = row.leftOccupied;
            mirrored_sig.set_row(height-1-i, state, l_occupation);
        }
        mirrored_sig.compute_hash();
        return mirrored_sig;
    }

};

std::ostream& operator<<(std::ostream& os, const Signature& sig) {
    os << "[Signature: height=" << sig.height << "]\n";
    for (int i = 0; i < sig.height; ++i) {
        const RowEntry& row = sig.get_row(i);
        os << "  Row " << i << ": (leftOccupied=" << (int)row.leftOccupied
            << ", state=" << (int)row.state << ")\n";
    }
    return os;
}

// ---------------------------------------------------------
// SignatureHasher: Custom hash functor to use with unordered_map
// ---------------------------------------------------------
// Custom hash functor
struct SignatureHasher {
    size_t operator()(const Signature& sig) const noexcept {
        return sig.cached_hash;
    }
};

