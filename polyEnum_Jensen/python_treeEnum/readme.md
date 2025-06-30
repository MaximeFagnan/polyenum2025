# Polyomino Enumerator

This project implements Iwan Jensen's algorithm for enumerating tree-like polyominoes, written in pure Python. The code is modular and built around core object-oriented classes representing polyomino boundary signatures, their generating functions, and dynamic programming transitions.

## Features
- Computes the number of fixed polyominoes of each size up to `n`
- Uses dynamic programming with signatures
- Encapsulates generating functions for efficient addition and multiplication
- Supports mirrored signature merging to reduce computation

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

