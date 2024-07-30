# Sliding
# Cubes or other objects
# Turrets
# Portals
# Wall jump?


import pygame as pyg

pyg.init()
width, height = 1200, 800
screen = pyg.display.set_mode((width, height))
clock = pyg.time.Clock()

# Constants
playerPos = [600,200]
playerVel = [0,0]
playerSize = 15
playerSpeed= 1

gravityConstant = .05
gameMap = []
debugObjs = []

keys = [False,False,False]

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


testWall = Wall(500,300,150,150)
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
    if playerVel[1]<10:
        playerVel[1]+=gravityConstant

    # Handles velocity
    playerPos[0]+=playerVel[0]
    playerPos[1]+=playerVel[1]

    #Handles movement
    if keys[0]:
        playerPos[1]-=playerSpeed*4
    if keys[1]:
        playerPos[0]-=playerSpeed
    if keys[2]:
        playerPos[0]+=playerSpeed

    predictedPos = [playerPos[0]+playerVel[0],playerPos[1]+playerVel[1]]

    for block in gameMap:
        closestPoint = (block.left+max(0,min(playerPos[0]-block.left,block.width)), block.top+max(0,min(playerPos[1]-block.top,block.height)))
        pyg.draw.circle(screen, (255,0,0), closestPoint, 5,width=0)
        if dist(closestPoint,playerPos)<playerSize:
            #playerVel=list(map(lambda x:-x*dampen,playerVel))
            playerVel=[0,0]

            #-+
            if block.left<=closestPoint[0]<=block.center[0] and block.top<=closestPoint[1]<=block.center[1]:
                playerPos=[playerPos[0],block.top-playerSize] if closestPoint[0]-block.left>=closestPoint[1]-block.top else [block.left-playerSize,playerPos[1]]
            #++
            elif block.center[0]<=closestPoint[0]<=block.left+block.width and block.top<=closestPoint[1]<=block.center[1]:
                playerPos=[playerPos[0],block.top-playerSize] if closestPoint[0]-block.center[0]>=block.center[1]-closestPoint[1]
                #if closestPoint[0]-block.center[0]>=block.center[1]-closestPoint[1] else [block.left+block.width+playerSize,playerPos[1]]

    pyg.draw.circle(screen, (255,255,255), playerPos, playerSize,width=1)

def manageKeys(event):
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

while True:
    screen.fill((0,0,0))
    mousePos = pyg.mouse.get_pos()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            exit()
        manageKeys(event)


    drawPlayer()
    drawMap()
    drawDebug()

    clock.tick(120)
    pyg.display.update()