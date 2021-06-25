import classes
import pygame
import pygame.locals as plocals
from enum import Enum

#board = classes.Board(list(range(1,10))*9)
board = classes.Board()
selected_cell = None

class Phase(Enum):
    SETUP = 0
    SOLVING = 1
    COMPLETE = 2

def round_down(num, divisor):
    return num - (num%divisor)

keymap = {
    # i know this is a sin,
    # but i see no way forward but a hardcode
    plocals.K_0: None,
    plocals.K_BACKSPACE: None,
    plocals.K_DELETE: None,
    plocals.K_1: 1,
    plocals.K_2: 2,
    plocals.K_3: 3,
    plocals.K_4: 4,
    plocals.K_5: 5,
    plocals.K_6: 6,
    plocals.K_7: 7,
    plocals.K_8: 8,
    plocals.K_9: 9,
}

width = 600
height = 600
margin = 50

# set these to sane values! best practice is to make both odd
boxwidth = 5
cellwidth = 3

assert (boxwidth % 2, cellwidth % 2) == (1,1)

boxsize = round_down((height - 2*margin)/3,3)
cellsize = boxsize / 3 - boxwidth / 3

# PHASES:
# 0: setup, allow input
# 1: solving, no input
# 2: complete
phase = Phase.SETUP

pygame.init()
surf = pygame.display.set_mode(size=(width,height))

font = pygame.font.Font(None,48)

bg = (0,0,0)

viewcells = []

class ViewCell():
    bgcolor = (0,0,0)

    def __init__(self,row,col,cellrect,rect,cell):
        self.row = row
        self.col = col
        self.rect = rect
        self.cell = cell
        self.cellrect = cellrect

    def render(self):
        if self is selected_cell and phase == Phase.SETUP:
            self.bgcolor = (180,120,0)
        else:
            self.bgcolor = (0,0,0)
        if self.bgcolor is not None:
            pygame.draw.rect(
                surf, self.bgcolor,
                self.rect)
        if type(self.cell.val) == int:
            n = font.render(str(self.cell.val),True,(255,255,255),self.bgcolor)
            rect = n.get_rect()
            rect.center = self.rect.center
            surf.blit(n, rect)

def drawBoard():
    for i in range(0,3):
        for j in range(0,3):
            # draw boxes
            pygame.draw.rect(
                surf,200,
                pygame.Rect(
                    # left, top, width, height
                    margin+i*boxsize,
                    margin+j*boxsize,
                    boxsize,boxsize
                    ),
                width=boxwidth)

    for i in range(0,9):
        for j in range(0,9):
            # draw cells\
            left = (
                    margin
                    +i*cellsize #offset cell
                    +boxwidth//2 #offset by outer boundary
                    +(i//3)*boxwidth) #offset individual lines
            top = (
                    margin
                    +j*cellsize 
                    +boxwidth//2 
                    +(j//3)*boxwidth) 
            cellrect = pygame.Rect(
                    left,
                    top,
                    cellsize,cellsize)
            pygame.draw.rect(
                surf, 100,
                cellrect,
                width=cellwidth)

            cell = ViewCell(
                row = i,
                col = j,
                cellrect = cellrect,
                rect = pygame.Rect(
                left+cellwidth/2,
                top+cellwidth/2,
                cellsize-cellwidth-1,
                cellsize-cellwidth-1),
                cell=board.getCell(i,j))

            cell.render()
            viewcells.append(cell)


drawBoard()
#selected_cell = viewcells[0]

running = True
updated = []

def select(c):
    global selected_cell
    if selected_cell is not None:
        updated.append(selected_cell)
    selected_cell = c
    if c is not None:
        updated.append(c)

def getViewCell(r,c):
    return viewcells[c+r*board.d2]

def offsetWrap(v,off,bound=board.d2):
    assert off in (-1,0,1)
    if v == 0 and off == -1:
        v = bound-1
    elif v == bound-1 and off == 1:
        v = 0
    else:
        v += off
    return v

def moveSelect(xoff,yoff):
    # xoff and yoff in [-1,1]
    assert xoff in (-1,0,1) and yoff in (-1,0,1)
    r = offsetWrap(selected_cell.row,yoff)
    c = offsetWrap(selected_cell.col,xoff)
    select(getViewCell(r,c))

while running:
    
    for event in pygame.event.get():
        # be wary of this order!
        if event.type == plocals.QUIT or (event.type == plocals.KEYDOWN and event.key==plocals.K_q):
            running = False
        elif phase == Phase.SETUP:
            if (event.type == plocals.KEYDOWN
            and event.key == plocals.K_RETURN):
                updated.append(selected_cell)
                selected_cell = None
                phase = Phase.SOLVING
                board.prepSolve()
            elif event.type == plocals.MOUSEBUTTONDOWN:
                for c in viewcells:
                    if c.cellrect.collidepoint(event.pos[0],event.pos[1]):
                        select(c)
                        break
            elif selected_cell and event.type == plocals.KEYDOWN:
                if event.key in keymap:
                    selected_cell.cell.val = keymap[event.key]
                elif event.key in (plocals.K_UP,plocals.K_w):
                    moveSelect(-1,0)
                elif event.key in (plocals.K_DOWN,plocals.K_s):
                    moveSelect(1,0)
                elif event.key in (plocals.K_LEFT,plocals.K_a):
                    moveSelect(0,-1)
                elif event.key in (plocals.K_RIGHT,plocals.K_d):
                    moveSelect(0,1)
                updated.append(selected_cell)
        




    # superstructure will be its own module after beta
    if phase == phase.SOLVING:
        board.evalOp()

    #if board.updated:
    #    print("board ids to update:",board.updated)
    #    for x in board.updated:
    #        print(board.grid[x].val)
    #        print(viewcells[x].cell.val)
    #        print("end board update info")

    updated = updated + [viewcells[i] for i in board.updated]
    board.updated = []

    for u in updated:
        u.render()
    updated = []


    pygame.display.flip()

    

