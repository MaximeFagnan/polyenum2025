#pragma once

#include <cstdint>

// ---------------------------------------------------------
// RowEntry: A compact 4-bit structure
// 3 bits for the state (0 to 4), 1 bit for leftOccupied
// ---------------------------------------------------------
struct RowEntry {
    uint8_t state : 3;
    uint8_t leftOccupied : 1;

    RowEntry(uint8_t s = 0, bool left = false)
        : state(s), leftOccupied(left ? 1 : 0) {}

    bool operator==(const RowEntry& other) const {
        return state == other.state && leftOccupied == other.leftOccupied;
    }
};
