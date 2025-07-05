#include <iostream>
#include <stdlib.h>
#include <array>
#include <unordered_map>
#include <cstdint>
#include <cstddef> // for size_t
#include "RowEntry.hpp"

// Warning this, just setting a bigger row height might break mirror and == for uninitialized RowEntrys
constexpr int SIGNATURE_HEIGHT = 16; // Row height of 16, needs to be changed to the specific height of a signature. 

// ---------------------------------------------------------
// Signature: represents the state of the boundary
// Contains up to SIGNATURE_HEIGHT RowEntry values, a height, and a cached hash
// ---------------------------------------------------------
struct Signature {
    std::array<RowEntry, SIGNATURE_HEIGHT> rows;
    size_t height;
    size_t cached_hash;

    // Constructor initializes height and clears hash
    Signature(size_t h = 0) : height(h), cached_hash(0) {}

    // Set the row at position `row` with state and leftOccupied flag
    void set_row(size_t row, uint8_t state, bool leftOccupied) {
        rows[row] = RowEntry(state, leftOccupied);
    }

    // Retrieve the row at position `row`
    RowEntry get_row(size_t row) const {
        return rows[row];
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
};

// ---------------------------------------------------------
// SignatureHasher: Custom hash functor to use with unordered_map
// ---------------------------------------------------------
// Custom hash functor
struct SignatureHasher {
    size_t operator()(const Signature& sig) const noexcept {
        return sig.cached_hash;
    }
};

