# Sliding
# Cubes or other objects
# Turrets
# Portals
# Wall jump?

import math
import pygame as pyg

pyg.init()
width, height = 1200, 800
screen = pyg.display.set_mode((width, height))
clock = pyg.time.Clock()

# Constants
gravityConstant = .1
gameMap = []
players = []
debugObjs = []

debugMode = False

keys = [False,False,False]
mouseState = [False,False,False]
mousePos = [0,0]

# Handler functions
def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1/2)

def manageCollisions(predictedPos,obj):
    #The object should have a size, and a position
    objSize = obj.size
    objPos = obj.pos
    for block in gameMap:
        closestPoint = (block.left+max(0,min(predictedPos[0]-block.left,block.width)), block.top+max(0,min(predictedPos[1]-block.top,block.height)))
        if dist(closestPoint,predictedPos)<=objSize:
            gridPos = [(predictedPos[0]-block.center[0])/(block.width/2),(predictedPos[1]-block.center[1])/(block.height/2)]
            if hasattr(obj,'vel'):
                obj.vel=[0,0]
            #+-
            if gridPos[0]>=0 and gridPos[1]<=0:
                objPos = [objPos[0],block.top-objSize] if gridPos[0]<=abs(gridPos[1]) else [block.left+block.width+objSize,objPos[1]]

                if hasattr(obj,'playerAir'):
                    obj.playerAir = False if gridPos[0]<=abs(gridPos[1]) else True
            #--
            if gridPos[0]<=0 and gridPos[1]<=0:
                objPos = [objPos[0],block.top-objSize] if abs(gridPos[0])<=abs(gridPos[1]) else [block.left-objSize,objPos[1]]
                if hasattr(obj,'playerAir'):
                    obj.playerAir = False if abs(gridPos[0])<=abs(gridPos[1]) else True
            
            #-+
            if gridPos[0]<=0 and gridPos[1]>=0:
                objPos = [objPos[0],block.top+block.height+objSize] if abs(gridPos[0])<=gridPos[1] else [block.left-objSize,objPos[1]]
                if hasattr(obj,'playerAir'):
                    obj.playerAir = True

            #++
            if gridPos[0]>=0 and gridPos[1]>=0:
                objPos = [objPos[0],block.top+block.height+objSize] if gridPos[0]<=gridPos[1] else [block.left+block.width+objSize,objPos[1]]
                if hasattr(obj,'playerAir'):
                    obj.playerAir = True


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

class Player():
    def __init__(self, playerPos = [600,200], playerVel = [0,0] ,playerSize = 15,playerSpeed = 1, playerAir = True, playerRot = 0, playerMode=True,gunPos=0,predictedPos=[600,200]):
        self.pos = playerPos
        self.vel = playerVel
        self.size = playerSize
        self.speed = playerSpeed
        self.rot = playerRot

        # Unique
        self.playerMode = playerMode # Blue or Orange
        self.playerAir = playerAir
        self.gunPos = gunPos
        self.predictedPos = predictedPos

    def gravity(self):
        if self.vel[1]<10:
            self.vel[1]+=gravityConstant

    def velocity(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]

    def movement(self):
        if keys[0] and not self.playerAir:
            self.vel[1]=-3.5
            self.playerAir=True
            self.pos[1]-=self.speed
        if keys[1]:
            self.pos[0]-=self.speed
        if keys[2]:
            self.pos[0]+=self.speed

    def calculate(self):
        self.rot = math.atan2(mousePos[1]-self.pos[1],mousePos[0]-self.pos[0])
        self.gunPos = [math.cos(self.rot)*25+self.pos[0],math.sin(self.rot)*25+self.pos[1]]
        self.predictedPos = [self.pos[0]+self.vel[0],self.pos[1]+self.vel[1]]

    def render(self):
        pyg.draw.circle(screen, (255,255,255), self.pos, self.size,width=1)
        Line(self.pos,self.gunPos,width=5,color=[125,125,255]).draw() if self.playerMode else Line(self.pos,self.gunPos,width=5,color=[255,125,0]).draw


testWall = Wall(350,300,300,150)
gameMap.append(testWall)

# Secondary functions
def drawMap():
    for block in gameMap:
        block.draw()

def drawDebug():
    for deco in debugObjs:
        deco.draw()

def manageKeys(event):
    global mouseState
    if event.type==pyg.KEYDOWN:
        if event.key == pyg.K_w:
            keys[0]=True
        if event.key == pyg.K_a:
            keys[1]=True
        if event.key == pyg.K_d:
            keys[2]=True
        
    if event.type==pyg.KEYUP:
        if event.key == pyg.K_w:
            keys[0]=False
        if event.key == pyg.K_a:
            keys[1]=False
        if event.key == pyg.K_d:
            keys[2]=False

    if mouseState[0]:
        for player in players:
            player.playerMode = not player.playerMode

players.append(Player())

while True:
    screen.fill((0,0,0))
    mousePos = pyg.mouse.get_pos()
    mouseState = pyg.mouse.get_pressed()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            exit()

        if event.type==pyg.KEYDOWN:
            if event.key==pyg.K_f:
                place = mousePos

            if event.key==pyg.K_g:
                newWall = Wall(place[0],place[1],mousePos[0]-place[0],mousePos[1]-place[1])
                gameMap.append(newWall)

        manageKeys(event)

    for player in players:
        player.gravity()
        player.velocity()
        player.movement()
        player.calculate()
        player.render()
        manageCollisions(player.predictedPos,player)

    drawMap()
    drawDebug()

    clock.tick(120)
    pyg.display.update()