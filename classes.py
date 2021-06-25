from enum import Enum
#
#class LineType(Enum):
#    ROW = 0
#    COLUMN = 1

import typing

# possible contents of a cell:
# Number
# Superposition (later)
# Possibilities
# None

# alas, i'm not willing to install 3.9, so the set[int] will have to go

# URGENT: AS IS, SETS WILL OCCUR AFTER EVALS. MAKE PRIORITY OPQUEUES IMMEDIATELY

CellVal = typing.Union[int,set,None]

class Ops(Enum):
    EVAL = 0
    SET = 1
    NEGEVAL = 2

def invertVals(v):
    s = set(range(1,10))
    s.difference_update(v)
    return s

class Cell():

    #had to remove the board type annotation because it isn't a valid name yet
    def __init__(self,i:int,row:int,col:int,box:int,val:CellVal,board):
        self.row: int = row
        self.col: int = col
        self.box: int = box
        self.i: int = i
        self.val: CellVal = val
        self.board: Board = board

    def __repr__(self):
        return f"Cell(row {self.row}, col {self.col}, box {self.box}, val {self.val})\n"

    def getRow(self):
        return self.board.getRow(self.row)

    def getCol(self):
        return self.board.getCol(self.col)

    def getBox(self):
        return self.board.getBox(self.box)

    def getNeighbors(self):
        return set.union(self.getRow().cells,self.getCol().cells,self.getBox().cells)

    def getNeighborsWithout(self,i):
        # realized this was useless after I wrote it
        s = set()
        for o in (self.getRow(),self.getCol(),self.getBox()):
            if i not in o.have:
                s.update(o)
        return s


    def update(self):
        self.board.updated.append(self.i)

    def set(self,v:int):
        self.update()
        self.val = v
        for g in (self.getRow(),self.getCol(),self.getBox()):
            g.possess(v)
        for c in self.getNeighbors():
            if isinstance(c.val,set) and v in c.val:
                c.val.remove(v)
                if len(c.val) == 1:
                    # recursion!
                    nv = c.val.pop()
                    self.board.queue(c.set,nv,priority=True)

    def eval(self):
        """initial evaluation of a cell"""
        if self.val:
            return
        eliminated = self.getRow().have | self.getCol().have | self.getBox().have
        poss = invertVals(eliminated)
        if len(poss) == 1:
            v = poss.pop()
            self.board.queue(self.set,v,priority=True)
        else:
            self.val = poss


class Group():

    # design choice: we're going to use sets of cells internally
    # instead of lists of cells. we shouldn't ever need to pinpoint
    # a cell within a group by its list coordinate, especially since
    # this type is used for boxes and lines.
    

    def __init__(self,cells:set):
        self.have: set = set()
        self.want: set = set(range(1,10))
        if len(cells) != 9:
            raise Exception
        self.cells = cells
        

    def values(self):
        return {c.val for c in self.cells}

    def possess(self,n:int):
        # this group now possesses n: shift the sets accordingly
        self.want.discard(n)
        self.have.add(n)

    def negEval(self):
        pass

    def refresh(self):
        for c in self.cells:
            if type(c.val) is int:
                self.possess(c.val)



class Board():

    def __init__(self,g=81*[None]):

        self.grid: list = []

        # for future extension beyond 9x9
        # this is the number of cells wide each box is,
        # plus the number of boxes wide the board is
        self.d: int = 3

        # this is the number of cells in a row, col, or box
        # this line, formerly in the top class level instead
        # of the constructor, was the cause of bug aleph
        self.d2: int = self.d**2

        # a tip: len(self.grid) == d**4

        self.rows = []
        self.cols = []
        self.boxes = []

        # list[int] of cells to update
        self.updated = []
        self.opqueue = []
        self.pqueue = []

        # g will be a list of int
        for i, v in enumerate(g):
            # jesus this is a lot of powers
            boxrow = i // self.d**3
            boxcol = (i % self.d2) // self.d
            boxn = boxrow*self.d + boxcol
            cell = Cell(
                i = i,
                row = i // self.d2,
                col = i % self.d2,
                box = boxn,
                val = v,
                board = self
                )
            self.grid.append(cell)
            self.queue(cell.eval)

        for j in range(0,self.d2):
            self.rows.append(self.makeRow(j))
            self.cols.append(self.makeCol(j))
            self.boxes.append(self.makeBox(j))

    def queue(self,func,arg=None,priority=False):
        if priority:
            self.pqueue.append((func,arg))
        else:
            self.opqueue.append((func,arg))



    def slice(self,start:int,end:int,step:int = 1) -> set:
        s = self.grid[start:end:step]
        se = set(s)
        return se

    def makeRow(self,i: int) -> Group:
        start = i*self.d2
        end = (i+1)*self.d2
        g = Group(self.slice(start,end))
        return g

    def makeCol(self,i: int) -> Group:
        start = i
        end = -self.d2+i+1 #hope that works, maybe off by one
        if end >= 0:
            end = len(self.grid)
        step = self.d2 # grab every ncols'th cell
        s = self.slice(start,end,step)
        g = Group(s)
        return g

    def sliceUnion(self,ends:tuple) -> set:
        # return the union of several slices given by the endpoints,
        # in the format ((start1,end1),(start2,end2),...)
        s = set()
        for i in ends:
            s = s | self.slice(i[0],i[1])
        return s

    def makeBox(self,i: int) -> Group:
        # i'm gonna hardcode this
        # actually, not today satan, i will not hardcode this
        # watch:

        # start is the number on the grid list
        # of the upper left corner of the box
        start = (
            # find which row (on the box grid)
            # the box is on,
            # and then multiply the row by d^3,
            # which will skip d rows of boxes
            (i // self.d) * self.d**3
            # then find the column of the box
            # on the box grid, and shift over
            # an appropriate number of columns
            + (i % self.d) * self.d)

        endpoints = (
            # first row: start to d
            (start,start+self.d),
            # second row: shift up one row, so d^2
            (start+self.d2,start+self.d2+self.d),
            # same idea, shift by 2d^2
            (start+2*self.d2,start+2*self.d2+self.d))
        g = Group(self.sliceUnion(endpoints))
        return g

    def getRow(self,i:int) -> Group:
        return self.rows[i]

    def getCol(self,i:int) -> Group:
        return self.cols[i]

    def getBox(self,i:int) -> Group:
        return self.boxes[i]

    def getCell(self,r,c):
        return self.grid[c+r*self.d2]

    def evalOp(self):
        if self.pqueue != []:
            op = self.pqueue.pop(0)
        elif self.opqueue == []:
            return
        else:
            op = self.opqueue.pop(0)
        if op[1] is not None:
            # packing is mysterious
            op[0](op[1])
        else:
            op[0]()

    def prepSolve(self):
        # current purpose is to set all the groups
        for g in self.rows + self.cols + self.boxes:
            g.refresh()


     
#b = Board(list(range(0,81)))
