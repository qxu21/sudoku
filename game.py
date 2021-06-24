import classes
import pygame
from pygame.locals import *
from enum import Enum

board = classes.Board(list(range(1,10))*9)

class Phase(Enum):
    SETUP = 0
    SOLVING = 1
    COMPLETE = 2

def round_down(num, divisor):
    return num - (num%divisor)

width = 800
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

selected_cell = (5,5)

pygame.init()
surf = pygame.display.set_mode(size=(width,height))

font = pygame.font.Font(None,48)

bg = (0,0,0)

viewcells = []

class ViewCell():
    bgcolor = None

    def __init__(self,innerrect,cell):
        self.rect = innerrect
        self.cell = cell

    def render(self):
        if self.bgcolor is not None:
            pygame.draw.rect(
                surf, self.bgcolor,
                self.rect)
        if type(self.cell.val) == int:
            n = font.render(str(self.cell.val),True,(255,255,255),self.bgcolor)
            rect = n.get_rect()
            rect.center = self.rect.center
            surf.blit(n, rect)




def findBg(x,y):
    if phase == Phase.SETUP and (x,y) == selected_cell:
        return (180,120,0)
    else:
        return None
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
                innerrect = pygame.Rect(
                left+cellwidth/2,
                top+cellwidth/2,
                cellsize-cellwidth-1,
                cellsize-cellwidth-1),
                cell=board.getCell(i,j))

            bgcolor = findBg(i,j)
            if bgcolor is not None:
                cell.bgcolor = bgcolor

            cell.render()

            viewcells.append(cell)
                

            


#surf.blit()

drawBoard()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            break

    pygame.display.flip()

    

