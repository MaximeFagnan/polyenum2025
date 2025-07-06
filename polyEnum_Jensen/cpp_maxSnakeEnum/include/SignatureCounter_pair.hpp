#pragma once
#ifndef SIGNATURE_COUNTER_PAIR_HPP
#define SIGNATURE_COUNTER_PAIR_HPP

#include "Signature.hpp"
#include "MaxAreaCounter.hpp"
#include "transition_table.hpp"
#include <optional>
#include <cassert>

class SignatureCounterPair {
public:
	Signature signature;
	MaxAreaCount maxAreaCount;

	SignatureCounterPair(const Signature& sig, const MaxAreaCount& count):
		signature(sig),
		maxAreaCount(count)
	{
		// everything was initialized aleady in the topper.
	}
		
	SignatureCounterPair operator+(const SignatureCounterPair& other) const {
		// Dangerously assuming signatures are equal :O
		return SignatureCounterPair(signature, maxAreaCount + other.maxAreaCount);
	}

	std::optional<SignatureCounterPair> transition(int row, int modify_to) const {
		int lower = signature.get_row(row).state;
		int upper = row - 1 >= 0 ? signature.get_row(row-1).state : 0;
		TransitionKey key{ modify_to, lower, upper };
		
		// Not even in transition table should not happen
		assert(TRANSITION_TABLE.count(key) > 0), "Transition not even in table";

		auto [operation, new_lower, new_upper] = TRANSITION_TABLE.at(key);

		// Impossible operations return a nullptr;
		if (operation == Operation::Impossible) {
			return std::nullopt;
		}

		// degree constraint check if adding a cell
		if (modify_to == 1) {
			// The following shows the 4 cells A, B, C, D that can influence degrees of Lower(L) and Upper(U).
				//   A
				//  BU
				// CL
				//  D
			int lower_deg = 0;
			int upper_deg = 0;
			if (row >= 2 and signature.get_row(row - 2).state > 0) upper_deg++; // cell A
			if (row >= 1 and signature.get_row(row - 1).leftOccupied == 1) { // cell B
				upper_deg++;
				lower_deg++;
			}
			if (signature.get_row(row).leftOccupied == 1) lower_deg++; // cell C
			if (row + 1 < signature.height and signature.get_row(row + 1).state > 0) lower_deg++; // cell D
			//degree checks
			if (upper > 0 and upper_deg >= 2) return std::nullopt;
			if (lower > 0 and lower_deg >= 2) return std::nullopt; 
		}
		
		// We can now assert we have a valid transition and that we should do the transition with necessary modifications
		
		// Capture the states from old_signature and modify them according to operation
		std::vector<RowEntry> new_rowEntries = signature.get_row_entries();

		// firstly, update state behind kink with 1 or 0
		new_rowEntries[row].leftOccupied = lower > 0 ? 1 : 0;
		// secondly, get new maxAreaCounter and update if necessary
		MaxAreaCount new_maxAreaCounter = maxAreaCount.clone();
		if (modify_to > 0) new_maxAreaCounter.increase_max_area();

		//now go through all possible transitions
		if (operation == Operation::Blank) {
			// change upper and lower and ship it back;
			new_rowEntries[row].state = new_lower;
			if (row>0) new_rowEntries[row-1].state = new_upper;
			Signature new_signature = Signature(new_rowEntries);
			return SignatureCounterPair(new_signature, new_maxAreaCounter);
		}
		else if(operation == Operation::OverLine) {
			new_rowEntries[row].state = new_lower; //new_lower = 0 for overlining;
			// What did we write over? If it is a 4: look below,. If it is a 2: look above.
			if (lower == 2) {
				int count_2 = 1;
				int count_4 = 0;
				for (int i = row - 1; i >= 0; i--) {
					//if (new_rowEntries[i].state == 0 or == 1) pass;
					if (new_rowEntries[i].state == 2) count_2++;
					// hitting a 3 only matters if it is a 3 in the outer most component
					if (new_rowEntries[i].state == 3 and count_2 - 1 == count_4) {
						new_rowEntries[i].state = 2; //becomes the new lowest entry of component
						break;
					}
					if (new_rowEntries[i].state == 4) {
						count_4++;
						// matching 4 becomes an isolated component
						if (count_2 == count_4) {
							new_rowEntries[i].state = 1;
							break;
						}
					}
				}
			}

			else if (lower == 4) {
				int count_2 = 0;
				int count_4 = 1;
				for (int i = row + 1; i < new_rowEntries.size(); i++) {
					//if (new_rowEntries[i].state == 0 or == 1) pass;
					if (new_rowEntries[i].state == 2) {
						count_2++;
						// matching 2 becomes an isolated component
						if (count_2 == count_4) {
							new_rowEntries[i].state = 1;
							break;
						}
					}
					// hitting a 3 only matters if it is a 3 in the outer most component
					if (new_rowEntries[i].state == 3 and count_2 == count_4 - 1) {
						new_rowEntries[i].state = 4; //becomes the new lowest entry of component
						break;
					}
					if (new_rowEntries[i].state == 4) count_4++;
				}
			}
			// Overline operations complete.
			Signature new_signature = Signature(new_rowEntries);
			return SignatureCounterPair(new_signature, new_maxAreaCounter);
		}

		else if (operation == Operation::Hat) {
			// We are joining two pieces of the snake
			// assert row>0

			if (lower == 2 or lower == 3) {
				// We are connecting an inner component to an outer component. 
				new_rowEntries[row].state = new_lower;
				new_rowEntries[row - 1].state = 3; // bottom of inner component becomes an intermediate state
				// We now want to go change the top of the inner component to a 3.
				int count_2 = 0;
				int count_4 = 0;
				for (int i = row - 1; i >= 0; i--) {
					if (new_rowEntries[i].state == 2) count_2++;
					else if (new_rowEntries[i].state == 4) {
						count_4++;
						if (count_2 + 1 == count_4) {
							new_rowEntries[i].state = 3; //uppermost innercomponent site becomes intermediate site
							break;
						}
					}
				}

			}
			else if (lower == 4) {
				//connecting two overlapping components, but need to go removing inner 2 that is lower
				new_rowEntries[row].state = 3; // new site is an intermediary
				//scan downwards for matching 2 to become a 3
				int count_2 = 0;
				int count_4 = 0;
				for (int i = row + 1; i < new_rowEntries.size(); i++) {
					if (new_rowEntries[i].state == 2) {
						count_2++;
						if (count_2 == count_4 + 1) {
							new_rowEntries[i].state = 3;
							break;
						}
					}
					else if (new_rowEntries[i].state == 4) count_4++;
				}
			}
			//modified everything according to hat operation
			Signature new_signature = Signature(new_rowEntries);
			return SignatureCounterPair(new_signature, new_maxAreaCounter);
		}
		// Return logic inside every operation type logic.
		// You should have met your operation by now.
		std::cout << "We have a problem, operation type is " << static_cast<int>(operation);
	}

};

#endif