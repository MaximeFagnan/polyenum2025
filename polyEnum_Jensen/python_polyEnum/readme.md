# Polyomino Enumerator

This project implements Iwan Jensen's algorithm for enumerating polyominoes, written in pure Python. The code is modular and built around core object-oriented classes representing polyomino boundary signatures, their generating functions, and dynamic programming transitions.

## Features
- Computes the number of fixed polyominoes of each size up to `n`
- Uses dynamic programming with signatures
- Encapsulates generating functions for efficient addition and multiplication
- Supports mirrored signature merging to reduce computation

## Structure
```
python_polyEnum/
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

n=10
enumerator = PolyominoEnumerator(n)
gf = enumerator.run()
print(gf)
```

## Dependencies
- Python 3.9+

## OEIS
Tests are located in the `tests/` folder. The OEIS comparator let's you quickly compare the calculated values with the values from OEIS and include a runtime calculator for the program.

## Author
Maxime Fagnan

## License
MIT License

