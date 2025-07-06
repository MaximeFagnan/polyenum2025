#pragma once
#ifndef TRANSITION_TABLE_HPP
#define TRANSITION_TABLE_HPP

#include <string>
#include <map>
#include <tuple>

enum class Operation {
    Blank,
    Hat,
    OverLine,
    Impossible
};

struct TransitionKey {
    int modify_to;
    int lower;
    int upper;

    // Required for std::map
    bool operator<(const TransitionKey& other) const {
        return std::tie(modify_to, lower, upper) < std::tie(other.modify_to, other.lower, other.upper);
    }
};

struct TransitionValue {
    Operation op; // e.g., "blank", "hat", "over-line", "impossible"
    int new_lower;
    int new_upper;
};

const std::map<TransitionKey, TransitionValue> TRANSITION_TABLE = {
    {{0, 0, 0}, {Operation::Blank, 0, 0}},
    {{0, 0, 1}, {Operation::Blank, 0, 1}},
    {{0, 0, 2}, {Operation::Blank, 0, 2}},
    {{0, 0, 3}, {Operation::Blank, 0, 3}},
    {{0, 0, 4}, {Operation::Blank, 0, 4}},

    {{0, 1, 0}, {Operation::Impossible, 0, 0}},
    {{0, 1, 1}, {Operation::Impossible, 0, 0}},
    {{0, 1, 2}, {Operation::Impossible, 0, 0}},
    {{0, 1, 3}, {Operation::Impossible, 0, 0}},
    // No ADD operation

    {{0, 2, 0}, {Operation::OverLine, 0, 0}},
    {{0, 2, 1}, {Operation::OverLine, 0, 1}},
    {{0, 2, 2}, {Operation::OverLine, 0, 2}},
    {{0, 2, 3}, {Operation::Blank, 0, 2}},
    {{0, 2, 4}, {Operation::Blank, 0, 1}},

    {{0, 3, 0}, {Operation::Blank, 0, 0}},
    {{0, 3, 1}, {Operation::Blank, 0, 1}},
    {{0, 3, 2}, {Operation::Blank, 0, 2}},
    {{0, 3, 3}, {Operation::Blank, 0, 3}},
    {{0, 3, 4}, {Operation::Blank, 0, 4}},

    {{0, 4, 0}, {Operation::OverLine, 0, 0}},
    {{0, 4, 1}, {Operation::OverLine, 0, 1}},
    {{0, 4, 2}, {Operation::OverLine, 0, 2}},
    {{0, 4, 3}, {Operation::OverLine, 0, 3}},
    // impossible state here

    {{1, 0, 0}, {Operation::Blank, 1, 0}},
    {{1, 0, 1}, {Operation::Blank, 2, 4}},
    {{1, 0, 2}, {Operation::Blank, 2, 3}},
    {{1, 0, 3}, {Operation::Blank, 3, 3}},
    {{1, 0, 4}, {Operation::Blank, 3, 4}},

    {{1, 1, 0}, {Operation::Blank, 1, 0}},
    {{1, 1, 1}, {Operation::Blank, 2, 4}},
    {{1, 1, 2}, {Operation::Blank, 2, 3}},
    {{1, 1, 3}, {Operation::Blank, 3, 3}},
    // impossible state here

    {{1, 2, 0}, {Operation::Blank, 2, 0}},
    {{1, 2, 1}, {Operation::Blank, 2, 3}},
    {{1, 2, 2}, {Operation::Hat, 2, 3}},
    {{1, 2, 3}, {Operation::Impossible, 2, 3}},
    {{1, 2, 4}, {Operation::Impossible, 2, 4}},

    {{1, 3, 0}, {Operation::Blank, 3, 0}},
    {{1, 3, 1}, {Operation::Blank, 3, 3}},
    {{1, 3, 2}, {Operation::Hat, 3, 3}},
    {{1, 3, 3}, {Operation::Impossible, 3, 3}},
    {{1, 3, 4}, {Operation::Impossible, 3, 4}},

    {{1, 4, 0}, {Operation::Blank, 4, 0}},
    {{1, 4, 1}, {Operation::Blank, 3, 4}},
    {{1, 4, 2}, {Operation::Blank, 3, 3}},
    {{1, 4, 3}, {Operation::Hat, 3, 3}},
    // impossible state here
};

#endif 