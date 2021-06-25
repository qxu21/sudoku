A list of really obnoxious bugs.

# Bug Aleph

At first commit 12c6d9c, the tests `test_create_board` and `test_board` ran succeessfully on their own, but crashed if run together.

Further investigation reveals that the column creation function is somehow keeping state between instantiations.
Debugging was complicated by my use of {c.val for c in cells} stripping out the duplicates I was looking for.

Solved by close investigation of this segment:

```python
class Board():

    grid: list = []

    # for future extension beyond 9x9
    # this is the number of cells wide each box is,
    # plus the number of boxes wide the board is
    d: int = 3

    # this is the number of cells in a row, col, or box
    d2: int = d**2
```
Somehow `d` kept state because of the poor scoping decisions, and `d2` got bigger and bigger in different circumstances. I moved all this into `__init__` and suddenly the unit tests started working.

When I first implemented moving the selected cell by keyboard, I got some hilariously weird results, such as moving diagonally. Turns out I had swapped the row and column arguments to `getViewCell`.

# Bug Bet

When the solve algorithm first worked, and I plugged 1-8 in on the first row, the entire board filled with 9s. Look at the difference between the buggy chunk

```python
class Group():

    cells: set = set()
    have: set = set()
    want: set = set(range(1,10))

    def __init__(self,cells:set):
        if len(cells) != 9:
            raise Exception
        self.cells = cells
```
and the edit that fixed it
```python
class Group():
    
    def __init__(self,cells:set):
        self.cells: set = set()
        self.have: set = set()
        self.want: set = set(range(1,10))
        if len(cells) != 9:
            raise Exception
        self.cells = cells
```

Turns out the first one has universally shared class attributes, so when I updated the `have` and `want` sets on any one `Group`, the change was visible to all `Group`s! Lesson learned: only use per-instance attributes in the init function.

That stopped the entire grid from filling up with numbers, but the correct cell wasn't filling. Turns out I made the same error of swapping my row and column in my `Board.getCell()` function, which caused the wrong cell to be associated to each `ViewCell`. Write your tests, kids.