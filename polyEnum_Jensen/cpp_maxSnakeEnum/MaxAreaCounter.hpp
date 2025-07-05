#ifndef MAX_AREA_COUNT_HPP
#define MAX_AREA_COUNT_HPP

#include <iostream>

struct MaxAreaCount {
    int max_area = 0;
    int nb_configs = 0;

    MaxAreaCount() = default;
    MaxAreaCount(int max_area_, int nb_configs_)
        : max_area(max_area_), nb_configs(nb_configs_) {
    }

    MaxAreaCount operator+(const MaxAreaCount& other) const {
        // "this" and "other" objects are constants, so we are actualy returning a copy. 
        if (max_area > other.max_area) {
            return *this;
        }
        else if (max_area < other.max_area) {
            return other;
        }
        else {
            return MaxAreaCount(max_area, nb_configs + other.nb_configs);
        }
    }

    void increase_max_area() {
        ++max_area;
    }

    MaxAreaCount clone() const {
        return MaxAreaCount(max_area, nb_configs);
    }

    friend std::ostream& operator<<(std::ostream& os, const MaxAreaCount& mac) {
        os << "Max area: " << mac.max_area
            << "\nNumber of configurations: " << mac.nb_configs;
        return os;
    }
};

#endif // MAX_AREA_COUNT_HPP
