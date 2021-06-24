A list of really obnoxious bugs.

#Bug Aleph

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