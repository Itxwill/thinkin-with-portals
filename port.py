from typing import Any
import pygame as pyg

pyg.init()
width, height = 1200, 800
screen = pyg.display.set_mode((width, height))
clock = pyg.time.Clock()

# Constants
playerPos = [600,400]
playerVel = [0,0]
playerSize = 15

gravityConstant = .1
gameMap = []
debugObjs = []

# Handler functions
def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1/2)


# Classes
class Line():
    def __init__(self,p1,p2,width=1,color=(255,255,255)):
        self.p1=p1
        self.p2=p2
        self.color=color
        self.width=width
    def draw(self):
        pyg.draw.line(screen,self.color,self.p1,self.p2,self.width)

class Wall():
    def __init__(self,left,top,width,height,lineWidth=5,color=(255,255,255)):
        self.color=color
        self.left = left
        self.top=top
        self.width=width
        self.height=height
        self.lineWidth=lineWidth

        self.center = (left+width/2,top+height/2)

    def draw(self):
        pyg.draw.rect(screen,self.color,pyg.Rect(self.left,self.top,self.width,self.height),width=self.lineWidth)


testWall = Wall(0,750,1200,50)
gameMap.append(testWall)

# Secondary functions
def drawMap():
    for block in gameMap:
        block.draw()

def drawDebug():
    for deco in debugObjs:
        deco.draw()

def drawPlayer():
    global playerPos,playerVel,playerSize

    # Handles gravity
    playerVel[1]+=gravityConstant

    # Handles velocity
    playerPos[0]+=playerVel[0]
    playerPos[1]+=playerVel[1]

    for block in gameMap:
        closestPoint = (max(0,min(playerPos[0]-block.left,block.width)), block.top-playerPos[1])
        pyg.draw.circle(screen, (255,0,0), closestPoint, 5,width=0)
        #if dist(closestPoint,playerPos)<playerSize:
            

    pyg.draw.circle(screen, (255,255,255), playerPos, playerSize,width=1)
    

while True:
    screen.fill((0,0,0))
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            exit()

    drawPlayer()
    drawMap()
    drawDebug()

    clock.tick(120)
    pyg.display.update()