# maximal snake enumerator in an nxn square. (bxh à implémenter plus tard)

This project implements a modified version of Iwan Jensen's algorithm for enumerating maximal snake like polyominoes inscribed in a given rectangle, written in pure Python. The code is modular and built around core object-oriented classes representing polyomino boundary signatures, their generating functions, and dynamic programming transitions.

## Features
- Computes the size of the longest fixed snake-like polyominoes and the quantity of them
- Uses a transfer matrix algorithm with extra constraints on cell degrees
- Supports mirrored signature merging to reduce computation
- Supports pruning of signatures when they are not dense enough by using a minimal bound (obtained through constructions) and the 2/3 conjecture to fill the unoccupied cells. The pruning can probably be ameliorated by playing with the area on which the 2/3 conjecture fill is applied. Will it make a difference?

There are two main modifications to Jensen's tree-like polyomino enumeration:
- The signature include an occupation satus for every cell behind the classical signature column.
- The transition function does not allow adding an occupied cell if it would cause a cell to exceed degree 2.


## Structure
```
python_snakeEnum/
├── generating_function.py
├── signature.py
├── signature_pair.py
├── signature_table.py
├── enumerator.py
├── transitions.py
├── tests/
│   └──test.py
├── README.md
```

## Usage
You might need to comment out the tests I am currently doing at the bottom of the enumerator.py file (or call the following lines directly from there). 
```python
from poly_enum.enumerator import PolyominoEnumerator

n=10
program = maxSnake_Enumerator(n,n)
start = time.time()
print(f"Jensen style algorithm to find maximal snake in an {n} x {n} square (using conjecture 2/3 + min_bound pruning)")
print(program.run(True)) 
runtime = time.time() - start

print("Here are some column by column stats:")
print(f"\tNumber of pruned signatures with construction and 2/3 theorem: {program.prune_count}")
print(f"\tNumber of pruned signatures with vert_symmetries: {program.vertical_symmetry_prune_count}")
print(f"\tNumber of total sigs per column before vert_symmetry pruning: {program.signatures_per_column}")
# print(f"Proposed min_bound: {program.min_bound}")
print(f"program runtime: {runtime}s")
print()
```

## Dependencies
- Python 3.9+

## Author
Maxime Fagnan

## License
MIT License
