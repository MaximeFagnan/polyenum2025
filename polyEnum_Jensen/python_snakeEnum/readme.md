# Polyomino Enumerator

This project implements a modified version of Iwan Jensen's algorithm for enumerating snake like polyominoes, written in pure Python. The code is modular and built around core object-oriented classes representing polyomino boundary signatures, their generating functions, and dynamic programming transitions.

## Features
- Computes the number of fixed snake-like polyominoes of each size up to `n`
- Uses dynamic programming with signatures
- Encapsulates generating functions for efficient addition and multiplication
- Supports mirrored signature merging to reduce computation

There are two main modifications to Jensen's tree-like polyomino enumeration:
- The signature include an occupation satus for every cell behind the classical signature column.
- The transition function does not allow adding an occupied cell if it would cause a cell to exceed degree 2.

## Structure
```
python_implementation/
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
```python
from poly_enum.enumerator import PolyominoEnumerator

enumerator = PolyominoEnumerator(n=10)
gf = enumerator.run()
print(gf)
```

## Dependencies
- Python 3.9+

## Development
Tests are located in the `tests/` folder and can be run with `pytest`.

## Author
Maxime Fagnan

## License
MIT License

