# sudoku

It should, at some point, solve sudoku.

## Terminology

* GROUP: A box, row, or column on the sudoku board.
* LINE: A row or column
* SUPERPOSITION: *n* cells (the vast majority of useful superpositions are two cells) that share a group and the same set of *n* possible values. All groups shared by the cells in the superposition can be considered to already have that value for purposes of evaluating other cells.

## Development goals

**ALPHA**: Data structures, board display and read-in.

**BETA**: Complete all algorithm subfunctions and create the primitive beta superstructure: evaluate every unfilled cell on the board, then run negative evaluation on each group until solved or stalled. Beta may not be able to completely solve some or all boards because it doesn't implement superpositions.

**GAMMA**: Implement superpositions.

**DELTA**: To be determined, but a system/heuristics for determining in what order to apply the operations.

## Types
* `CellVal` is the union of `int` for a definite value, `set[int]` for possible values, or `None` for an unevaluated cell.

## Data Structures

### Group
A box, row, or column.

### Cell
A cell on the board.

`ValueSet`

## The Algorithm

All functions act on the board and have no output.

A superstructure that efficiently chooses which sub-operation to apply where will be developed later, but the first superstructure will be a brute-force system that repeatedly applies operations in a hardcoded manner as long as possible.

## Suboperations

### Evaluation
Input: cell
Purpose: evaluates an unevaluated cell, setting the cell to either a set of possibilities or a single value.

* Compile a list of all values in the cell's groups
* "Invert" this list of values, by subtracting it from `range(1,10)`
* If the inverted list has one value, **set** the cell

### Set/Eliminate
Input: cell, number
Purpose: sets a cell's value and recursively propagates changes to all affected cells.

* Set the cell to the given value.
* If not already (due to superpositions), add the given value to the set of values held by each of its groups.
* For all groups of the cell which do not have the number, and for all cells in said groups which have the number as a posssibility, remove the cell from the possibilities.
* If the cell only has one possibility, **recursively set** the cell with its new value, triggering further elimination

### Negative Evaluation
Input: group
Purpose: identify whether any cells in a group are the only possible place to put a given unfilled number, as well as identifying superpositions.

* For all unfilled cells in the group, count the number of occurences of each possiblity (up to 2). Additionally count the number of repetitions of each possibilities set.
* If the possibility-count is 1 for any given possibility value, find the cell which has that value and **set** it to the value, since the group requires this value and this cell is the only one that can have it.
* If a given size *n* possibilities set shows up exactly *n* times, set each cell to a superposition. Add the superpositioned values to the list of values held by the group.