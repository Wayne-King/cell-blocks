# Cell Blocks

Finds a solution to a Cell Blocks puzzle.

Given a grid in which some cells of the grid contain a number, find a solution such that each number is enclosed in a single, rectangular "cell block", where the cell block encloses that number of cells; no cell blocks overlap; and every cell of the grid is enclosed within a cell block.

The entry-point file is warden.py. Currently, it is hard-coded to solve just one particular instance of the puzzle. See the `assign_all_occupants()` function in that file, which composes the starting grid of numbers. 


## How to Use

It was written against Python v3.8.2.

    python.exe
    
    >>> import warden
