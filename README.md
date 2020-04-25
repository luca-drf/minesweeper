# Minesweeper Python
Basic Minesweeper game implementation in Python.

**Note:** The only user interface for the moment is textual (command line)

## Requirements
- Python 3.8
- pytest (dev)

## Usage

There are four modes available: 9x9, 16x16, 25x25, 32x32.
Simply run the main executable and follow the instructions.

```
$ python minesweeper.py
== Minesweeper ==
Enter Grid dimension
[S]mall, [M]edium, [L]arge, E[X]tra Large: s

   1  2  3  4  5  6  7  8  9
 A -  -  -  -  -  -  -  -  -
 B -  -  -  -  -  -  -  -  -
 C -  -  -  -  -  -  -  -  -
 D -  -  -  -  -  -  -  -  -
 E -  -  -  -  -  -  -  -  -
 F -  -  -  -  -  -  -  -  -
 G -  -  -  -  -  -  -  -  -
 H -  -  -  -  -  -  -  -  -
 I -  -  -  -  -  -  -  -  -

Enter action: [F]lag/[U]nflag or [R]eveal followed by cell coordinates (e.g. R A:9)
Action: R I:9
```
