import os
import time
from datetime import datetime
# This is the max snake class to enumerate number of maximal snakes in a bxh rectangle
from signature import Signature
from max_area_count import MaxAreaCount
from signatureCounter_pair import SignatureCounter_pair
from signature_table import SignatureTable
from max_area_count import MaxAreaCount


class maxSnake_Enumerator:
    def __init__(self, b, h):
        if h>b:
            b,h = h,b # set base to greater than height (less signatures)
        self.b = b
        self.h = h
        self.min_bound = self.det_min_bound()
        self.max_area_counter = MaxAreaCount(0,1)
        self.prune_count = {}
        self.signatures_per_column = {}
        self.vertical_symmetry_prune_count = {}
        # self.run()

    def run(self) -> MaxAreaCount:
        # reset max for every run
        self.max_area_counter = MaxAreaCount(0,1)
        h,b = self.h, self.b
        # signature table with only an empty signature of height w
        initial_signature = Signature([0]*h, [False]*h)
        initial_sig_counter = MaxAreaCount(0,1)
        initial_pair = SignatureCounter_pair(initial_signature, initial_sig_counter)
        table = SignatureTable()
        table.add(initial_pair)

        # for every necessary column
        for col in range(1, self.b+1):
            # Symmetry pruning proposed by Gill Barequet and Gil Ben-Shachar (2024) but before by Donald Knuth (see Jensen email exchange on Donald Knuth website)
            table.merge_mirrored_signatures()
            self.vertical_symmetry_prune_count[col-1] = self.signatures_per_column.get(col-1,2)-len(table.mapping)
            
            # Move the kink down row by row
            for row in range(h):
                # make a new table
                new_table = SignatureTable()
                for sig, maxAreaCount in table.items():
                    sig_count = SignatureCounter_pair(sig, maxAreaCount)
                    for to_modify in [0,1]:
                        if to_modify==0 and self.should_prune(sig_count,col,row):
                            self.prune_count[(col,row)] = self.prune_count.get((col,row),0)+1 # we pruned, let's count it
                            continue # do not even try the transition
                        # # This code would replace the pruning in the next section
                        # # It is better tu prune after determining if transition is valid (experimentally)
                        # elif to_modify == 1:
                        #     sig_count.maxAreaCount.increase_max_area()
                        #     if self.should_prune(sig_count,col,row):
                        #         self.prune_count[(col,row)] = self.prune_count.get((col,row),0)+1 # we pruned, let's count it
                        #         continue
                        #     sig_count.maxAreaCount.decrease_max_area()

                        new_pair = sig_count.transition(row, to_modify)
                        if new_pair is not None:
                            if to_modify==1 and self.should_prune(new_pair,col,row):
                                self.prune_count[(col,row)] = self.prune_count.get((col,row),0)+1 # we pruned, let's count it
                                continue # do not even try the transition
                            new_table.add(new_pair) # we did not prune
                            

                # Update the signatureGF table after every move of the kink
                table = new_table
            self.signatures_per_column[col] = len(table.mapping)
        # congrats! 

        
        # add to total count
        for sig, sig_max_area_counter in table.items():
            if sig.is_connected():
                # the max area counter should cumulate only max areas.
                self.max_area_counter += sig_max_area_counter

        return self.max_area_counter


    def det_min_bound(self):
        b, h = self.b, self.h
        assert b>=0 and h>=0, "b and h must be >=0"
        
        if b == h: # nxn square where n=b=h
            n = b
            oeis_min_bound= [1,1,3,7,11,17,24,33,42,53,64,77,92,107,123,142,162,182] # starts at 0
            if n < len(oeis_min_bound): # maximal snakes known
                return oeis_min_bound[n]
            else: # based on my construction of big snakes
                assert n>=18, "Oeis values up to 17"
                # n = 6k + r
                k = n//6
                r = n - 6*k
                inner_6x6_square_area  = 24 # aligns with 2/3 -2 (because in center)
                if r == 0:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 205-24
                    outer_addition = 88
                    return base_construction_area + (k_diff-1)*outer_addition + (k_diff**2)*inner_6x6_square_area
                elif r == 1:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 107 # I think we could go bigger with base case in n=19
                    outer_addition = 88+8*r
                    return base_construction_area + k_diff*outer_addition + (k_diff**2)*inner_6x6_square_area
                elif r == 2:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 122  # I think we could go bigger with base case in n=20
                    outer_addition = 88+8*r
                    return base_construction_area + k_diff*outer_addition + (k_diff**2)*inner_6x6_square_area
                elif r == 3:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 142
                    outer_addition = 88+8*r
                    return base_construction_area + k_diff*outer_addition + (k_diff**2)*inner_6x6_square_area
                elif r == 4:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 162
                    outer_addition = 88+8*r
                    return base_construction_area + k_diff*outer_addition + (k_diff**2)*inner_6x6_square_area
                elif r == 5:
                    base_construction_k = 2
                    k_diff = k - base_construction_k
                    base_construction_area = 182
                    outer_addition = 88+8*r
                    return base_construction_area + k_diff*outer_addition + (k_diff**2)*inner_6x6_square_area
            assert False, f"n=6k+r, 0 <= r <= 5, but your r is :{r}"
        else:
            assert b == h, "Only implemented for nxn for now"

    
    def should_prune(self, sig_counter_pair: SignatureCounter_pair,col: int, row:int) -> bool:
        sig: Signature = sig_counter_pair.signature # not used
        sig_max_area :int = sig_counter_pair.maxAreaCount.max_area
        column_complete = (row == self.h-1) # kink at bottom of column iff row == h-1

        # calculate area right of signature with conjecture 2/3 filling of size w x h
        conject_23_fill_area = 0

        # Area to the right is a single big rectangle
        if column_complete:
            b_23 = self.b - col
            h_23 = self.h
            conject_23_fill_area = self.conj_23(b_23,h_23)
        
        # Area to the right can be split into two useful rectangles
        elif row>=2 and row<=self.h-4:
            #rectangle 1
            b_23 = self.b - col
            h_23 = row+1
            conject_23_fill_area = self.conj_23(b_23,h_23)
            #rectangle 2
            b_23 = (self.b - col) + 1
            h_23 = self.h - (row+1)
            conject_23_fill_area += self.conj_23(b_23,h_23)

        else: return False # Haven't found a way to prune
        
        return sig_max_area + conject_23_fill_area < self.min_bound


    def conj_23(self, w: int, h: int) -> int:
        conject_23_fill_area = 0
        if w>h:
            w,h = h,w
        if w==0:
            conject_23_fill_area = 0
        # conjecture 2/3
        elif w==1 or (h==2 and w==2):
            conject_23_fill_area = w*h
        elif w==2 and h%2==1 and h>=3 :
            conject_23_fill_area = (3*w*h + 2)//4
        elif w==2 and h%2==0 and h>=4 :
            conject_23_fill_area = 3*w*h//4
        elif w==3 or (h%3==0 and w%3==0):
            conject_23_fill_area = (2*w*h + 6)//3
        elif w>=4 and h%3 == w%3 and w%3 != 0:
            conject_23_fill_area = (2*w*h + 4)//3
        elif w>=4 and w%3==0 and w%3 != 0 :
            conject_23_fill_area = (2*w*h + 3)//3
        else:
            conject_23_fill_area = (2*w*h + 2)//3
        return conject_23_fill_area
        

#############################################################################
# Program run and log
#############################################################################

def safe_run_and_log(n_values):
    os.makedirs("polyEnum_Jensen/python_maxSnakes/data", exist_ok=True)

    for n in n_values:
        filename = f"polyEnum_Jensen/python_maxSnakes/data/maxsnakeEnumData_{n}x{n}.txt"
        with open(filename, "w") as f:
            def log(msg):
                print(msg)         # Keep this if you still want to see the output live
                print(msg, file=f) # Save to file

            program = maxSnake_Enumerator(n, n)
            start = time.time()
            log(f"{datetime.now().isoformat()}")
            log(f"Jensen-style algorithm to find maximal snake in an {n} x {n} square (using conjecture 2/3 + min_bound pruning)")
            
            result = program.run()
            log(str(result))

            runtime = time.time() - start
            log("Here are some column by column stats:")
            log(f"\tNumber of pruned signatures with construction and 2/3 theorem: {program.prune_count}")
            log(f"\tNumber of pruned signatures with vert_symmetries: {program.vertical_symmetry_prune_count}")
            log(f"\tNumber of total sigs per column before vert_symmetry pruning: {program.signatures_per_column}")
            # log(f"Proposed min_bound: {program.min_bound}")
            log(f"Program runtime: {runtime:.2f}s")
            log("")

safe_run_and_log([10])