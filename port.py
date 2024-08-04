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
playerAir = True

gravityConstant = .1
gameMap = []
debugObjs = []

debugMode = False

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


testWall = Wall(350,300,300,150)
gameMap.append(testWall)

# Secondary functions
def drawMap():
    for block in gameMap:
        block.draw()

def drawDebug():
    for deco in debugObjs:
        deco.draw()

def drawPlayer():
    global playerPos,playerVel,playerSize,playerAir

    # Handles gravity
    if playerVel[1]<10:
        playerVel[1]+=gravityConstant

    # Handles velocity
    playerPos[0]+=playerVel[0]
    playerPos[1]+=playerVel[1]

    #Handles movement
    if keys[0] and not playerAir:
        playerVel[1]=-3.5
        playerAir=True
        playerPos[1]-=playerSpeed
    if keys[1]:
        playerPos[0]-=playerSpeed
    if keys[2]:
        playerPos[0]+=playerSpeed



    predictedPos = [playerPos[0]+playerVel[0],playerPos[1]+playerVel[1]]

    #Block collisions
    for block in gameMap:
        closestPoint = (block.left+max(0,min(predictedPos[0]-block.left,block.width)), block.top+max(0,min(predictedPos[1]-block.top,block.height)))
        if dist(closestPoint,predictedPos)<=playerSize:
            gridPos = [(predictedPos[0]-block.center[0])/(block.width/2),(predictedPos[1]-block.center[1])/(block.height/2)]
            playerVel=[0,0]
            #+-
            if gridPos[0]>=0 and gridPos[1]<=0:
                playerPos = [playerPos[0],block.top-playerSize] if gridPos[0]<=abs(gridPos[1]) else [block.left+block.width+playerSize,playerPos[1]]
                playerAir = False
            #--
            if gridPos[0]<=0 and gridPos[1]<=0:
                playerPos = [playerPos[0],block.top-playerSize] if abs(gridPos[0])<=abs(gridPos[1]) else [block.left-playerSize,playerPos[1]]
                playerAir = False
            
            #-+
            if gridPos[0]<=0 and gridPos[1]>=0:
                playerPos = [playerPos[0],block.top+block.height+playerSize] if abs(gridPos[0])<=gridPos[1] else [block.left-playerSize,playerPos[1]]
                playerAir = True if abs(gridPos[0])<=gridPos[1] else False
            #++
            if gridPos[0]>=0 and gridPos[1]>=0:
                playerPos = [playerPos[0],block.top+block.height+playerSize] if gridPos[0]<=gridPos[1] else [block.left+block.width+playerSize,playerPos[1]]
                playerAir = True if gridPos[0]<=gridPos[1] else False

    # Render the player
    pyg.draw.circle(screen, (255,255,255), playerPos, playerSize,width=1)

def manageKeys(event):
    global playerPos,playerAir
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

    drawPlayer()
    drawMap()
    drawDebug()

    clock.tick(120)
    pyg.display.update()