#pragma once

#include "Signature.hpp"
#include "MaxAreaCounter.hpp"
#include "transition_table.hpp"
#include "SignatureCounter_pair.hpp"
#include "Signature_Table.hpp"
#include <optional>
#include <cassert>

class Enumerator {
public:
	int b;
	int h;
	int min_bound = 0;
	MaxAreaCount total_mac = MaxAreaCount(0, 1);  // total max_area_counter

	// statistics about the counting
	std::vector<std::vector<int>> signature_after_cell;         // signature_after_cell[col][row]         number before pruning
	std::vector<std::vector<int>> pruned_signatures_after_cell; // pruned_signatures_after_cell[col][row] pruned to min/max bound
	std::vector<int> pruned_due_to_vert_symmetry;				// pruned_due_to_vert_symmmetry[col]      pruned to vert symmetry trick after column
	
    // Square constructor for the enumerator
	Enumerator(int n)
		: b(n), h(n),
		signature_after_cell(std::vector<std::vector<int>>(h, std::vector<int>(b, 0))),
		pruned_signatures_after_cell(std::vector<std::vector<int>>(h, std::vector<int>(b, 0))),
		pruned_due_to_vert_symmetry(std::vector<int>(b,0))  {
		min_bound = determine_min_bound(b, h);
	}

    void run() {
        // first signature is blank with a count of 1
        Signature initial_signature = Signature::blank(h);
        MaxAreaCount initial_mac = MaxAreaCount(0, 1);
        SignatureCounterPair initial_pair = SignatureCounterPair(initial_signature, initial_mac);
        SignatureTable table = SignatureTable();
        table.add(initial_signature, initial_mac);

        // for every necessary column (1 to b)
        for (int col = 1; col <= b; col++) {
            // Symmetry pruning proposed by Gill Barequet and Gil Ben-Shachar (2024) but before by Donald Knuth (see Jensen email exchange on Donald Knuth website)
            int size_before_merge = table.items().size();
            table.merge_mirrored_signatures();
            int size_after_merge = table.items().size();
            pruned_due_to_vert_symmetry[col-1] = size_before_merge - size_after_merge;
            
            //cell after cell for rows 0 to h-1
            for (int row = 0; row < h; row++) {
                // make a new table
                SignatureTable new_table = SignatureTable();
                // for every signature in the table, add up to two signatures in new_table
                for (const auto& [sig, mac] : table.items()) {
                    SignatureCounterPair current_SigMacPair = SignatureCounterPair(sig, mac);
                    for (int modify_to = 0; modify_to <= 1; modify_to++) {
                        std::optional<SignatureCounterPair> possible_transitionned_sig_mac = current_SigMacPair.transition(row, modify_to);
                        if (possible_transitionned_sig_mac.has_value()) {
                            const SignatureCounterPair& post_trans_sig_mac = possible_transitionned_sig_mac.value();
                            if (should_prune(post_trans_sig_mac, col, row)) {
                                pruned_signatures_after_cell[col-1][row]++;
                               /* std::cout << "[PRUNE] col=" << col << " row=" << row
                                    << " area=" << post_trans_sig_mac.maxAreaCount.max_area
                                    << " signature=" << post_trans_sig_mac.signature << "\n";*/
                            }
                            else {
                                new_table.add(post_trans_sig_mac.signature, post_trans_sig_mac.maxAreaCount);
                            }
                        }
                    }
                }
                // update the table
                table = std::move(new_table);
                signature_after_cell[col- 1][row] = table.items().size();
            }
        }

        // Congratulations! We ran the program for every cell with no problem!
        
        // Add signatures to the total count if they are connected
        for (const auto& [sig, mac] : table.items()) {
            if (sig.is_connected()) {
                total_mac = total_mac + mac;
            }
        }
    }

    // Use my constructions to find the area of a big snake and use it as a minimal bound
    int determine_min_bound(int b, int h) {
        assert(b > 0 && h > 0 && "b and h must be > 0");

        if (b == h) {
            int n = b;
            const std::vector<int> oeis_min_bound = {
                1, 1, 3, 7, 11, 17, 24, 33, 42, 53, 64, 77, 92, 107, 123, 142, 162, 182
            };

            if (n < (int)oeis_min_bound.size()) {
                return oeis_min_bound[n];
            }
            else {
                // Based on construction for n >= 18
                int k = n / 6;
                int r = n - 6 * k;
                int inner_6x6_square_area = 24;

                int base_construction_k = 2;
                int k_diff = k - base_construction_k;
                int base_construction_area = -1;
                int outer_addition = 88 + 8 * r;

                switch (r) {
                case 0:
                    base_construction_area = 205 - 24;
                    k_diff--; // base_construction_k = 3
                    break;
                case 1:
                    base_construction_area = 107;
                    break;
                case 2:
                    base_construction_area = 122;
                    break;
                case 3:
                    base_construction_area = 142;
                    break;
                case 4:
                    base_construction_area = 162;
                    break;
                case 5:
                    base_construction_area = 182;
                    break;
                default:
                    assert(false && "n = 6k + r, with 0 <= r <= 5. Invalid r.");
                }

                return base_construction_area
                    + (k_diff * outer_addition)
                    + (k_diff * k_diff) * inner_6x6_square_area;
            }
        }
        else {
            assert(false && "Only implemented for b == h (square shapes)");
        }
        return -1; // Should never reach here
    }

    // maximum fill in a rectangle of width w, height h
    int conjectured_23_fill_area(int w, int h) const {
        // firstly, make sure h>=w
        if (w > h) {
            int temp = w;
            w = h;
            h = temp;
        }
        if (w == 0) return 0;
        if (w == 1 || (w == 2 && h == 2)) {
            return w * h;
        }
        else if (w == 2 && h % 2 == 1 && h >= 3) {
            return (3 * w * h + 2) / 4;
        }
        else if (w == 2 && h % 2 == 0 && h >= 4) {
            return (3 * w * h) / 4;
        }
        else if (w == 3 || (w % 3 == 0 && h % 3 == 0)) {
            return (2 * w * h + 6) / 3;
        }
        else if (w >= 4 && h % 3 == w % 3 && w % 3 != 0) {
            return (2 * w * h + 4) / 3;
        }
        else {
            return (2 * w * h + 2) / 3;
        }
    }

    bool should_prune(const SignatureCounterPair& pair, int col, int row) const {
        const Signature& sig = pair.signature;
        int sig_max_area = pair.maxAreaCount.max_area;

        // Incomplete column removal technique
        bool column_incomplete = (row < h - 1);
        // Count how many cells lie above the kink that are still occupied
        int area_above_kink = 0;
        if (column_incomplete) {
            for (int i = row; i >= 0; i--) {
                if (sig.get_row(i).state != 0) area_above_kink++;
            }
        }
        int sig_area_in_rect = sig_max_area - area_above_kink;
        // Determine remaining width w of incomplete rectangle
        int w = column_incomplete ? (b - (col - 1)) : (b - col);
        if (w == 0) return false; // Final cell, don't prune and don't cause error.
        int conject_area = conjectured_23_fill_area(w, h);

        /* 
        New pruning methods can be added :
            * split in 2 rectangles for conj 2/3 along where the kink is (especially if kink is 3 rows above/below bottom or top of signature
            * Calculate maximum number of cells of deg 1 that can be put to the right of the signture (considering only degree of cells) and 2/3 fill according to that
        */
        
        return sig_area_in_rect + conject_area < min_bound;
    }

};