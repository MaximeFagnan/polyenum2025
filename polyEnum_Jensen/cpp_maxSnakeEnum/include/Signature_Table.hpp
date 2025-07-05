#ifndef SIGNATURE_TABLE_HPP
#define SIGNATURE_TABLE_HPP

#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>
#include <sstream>
#include "signature.hpp"
#include "MaxAreaCounter.hpp"

// Already implemented
//// Optional: specialize std::hash for Signature if using unordered_map
//namespace std {
//    template <>
//    struct hash<Signature> {
//        std::size_t operator()(const Signature& sig) const {
//            return sig.hash(); // assumes Signature has a hash() method
//        }
//    };
//}

class SignatureTable {
private:
    std::unordered_map<Signature, MaxAreaCount, SignatureHasher> mapping;

public:
    void add(const Signature& sig, const MaxAreaCount& count) {
        if (mapping.count(sig)) {
            mapping[sig] = mapping[sig] + count;
        }
        else {
            mapping[sig] = count;
        }
        
    }

    //// This does not seem safe... probably should not use thi
    //const std::unordered_map<Signature, MaxAreaCount, SignatureHasher>& items() const {
    //    return mapping;
    //}


    void merge_mirrored_signatures() {
        std::unordered_map<Signature, MaxAreaCount,SignatureHasher> new_mapping;
        std::unordered_set<Signature,SignatureHasher> seen;

        for (const auto& entry : mapping) {
            const Signature& sig = entry.first;
            const MaxAreaCount& count = entry.second;
            
            //skip seen signatures (and their mirrors)
            if (seen.count(sig)>0) continue;

            Signature mirrored = sig.mirror_clone();
            seen.insert(sig);
            seen.insert(mirrored);

            if (mapping.count(mirrored) > 0 and !(mirrored==sig)) {
                new_mapping[sig] = count + mapping[mirrored];
            }
            else {
                new_mapping[sig] = count;
            }
        }

        mapping = std::move(new_mapping);
    }
};

#endif // SIGNATURE_TABLE_HPP