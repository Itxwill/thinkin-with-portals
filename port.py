import pygame as pyg

pyg.init()
width, height = 1200, 800
screen = pyg.display.set_mode((width, height))
clock = pyg.time.Clock()

playerpos = [600,400]
playervel = [0,0]
playersize = 15
objects = []



def drawplayer():
    playervel[1]+=.1

    playerpos[0]+=playervel[0]
    playerpos[1]+=playervel[1]
    pyg.draw.circle(screen,(255,255,255), playerpos, playersize,1)
    

while True:
    screen.fill((0,0,0))
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            exit()
    clock.tick(120)
    drawplayer()
    pyg.display.update()