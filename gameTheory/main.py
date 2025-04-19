import pygame
import matplotlib.pyplot as plt
import consts as c
import world
from creature import Creature
import random
import math
import numpy as np
import extraFunctions as ef
from button import Button

#Init pygame
pygame.init()
#Create FPS clock
clock = pygame.time.Clock()
#Create window
WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
#Set caption for window
pygame.display.set_caption("Game Theory")
#Initialise matplotlib in way that doesn't interfere and stop pygame event loop (non-blocking mode)
plt.ion()
fig, ax = plt.subplots()

#Load Images
#Load Button Images
showButtonImage = pygame.transform.scale_by(pygame.image.load("assets/show.png").convert_alpha(), (0.1,0.1))
hideButtonImage = pygame.transform.scale_by(pygame.image.load("assets/hide.png").convert_alpha(), (0.1,0.1))

#Load text font
text_font = pygame.font.SysFont("Consolas", 24, bold = True)

############################
########### Vars ###########
############################
#Arrays for storing population data
doveData = []
hawkData = []
#Initial dove and hawk numbers. Declared here to avoid error with labels drawing before first data point
doves = 0
hawks = 0
#Initialise average percentage variables to avoid throwing errors on first render
doveAveragePercentage = 0
hawkAveragePercentage = 0
#Var for tracking whether visuals are being shown
visuals = True

############################
##### Create Objects #######
############################
#Create creature group
creatureGroup = pygame.sprite.Group()
#Create world to draw grid
world = world.World()

#Create initial creatures
for i in range(c.INITIAL_BEINGS):
    newCreatureFightChance = random.choice([0,100])
    newCreature = Creature(newCreatureFightChance, random.randint(1,500))
    creatureGroup.add(newCreature)
#Get initial percentages of doves and hawks and give a value to graphing data to avoid errors in first render
    if newCreatureFightChance:
        hawks += 1
doves = c.INITIAL_BEINGS - hawks
doveData.append(doves)
hawkData.append(hawks)
hawkAveragePercentage = hawks/c.INITIAL_BEINGS * 100
doveAveragePercentage = 100 - hawkAveragePercentage

#Create Buttons
displayVisualsButton = Button(750, 30, showButtonImage, hideButtonImage)
############################
####### Game Loop ##########
############################
#Set running variables
run = True
#
############################
######## GAME LOOP #########
############################

while run:
    #Tick clock
    clock.tick(c.FPS)
    #Clear screen (to remove dead creatures)
    WIN.fill((0,0,0))
    #Close visuals button
    if displayVisualsButton.draw(WIN, visuals):
        if visuals:
            visuals = False
        else:
            visuals = True
    if visuals:
        #Draw Grid
        world.draw_grid(WIN)
        #Draw creatures
        ef.drawCreatures(creatureGroup, WIN)
    #Draw labels
    ef.draw_labels(WIN, doves, hawks, doveAveragePercentage, hawkAveragePercentage, text_font)
    #Force all creatures to confront another and change score accordingly
    ef.fightAllCreatures(creatureGroup)
    #Remove any with score lower than -100 or ended lifespan. Tick lifespan.
    ef.removeDead(creatureGroup)
    #Replace removed dead
    for k in ef.getNextGeneration(creatureGroup):
        newCreature = Creature(k.fightChance, 50)
        creatureGroup.add(newCreature)
    #Fill next plot of data in data array and set current dove and hawk numbers
    doves, hawks = ef.getNextGraphReading(creatureGroup)
    #Get new average percentages
    doveAveragePercentage = ((len(doveData)*doveAveragePercentage/100*c.INITIAL_BEINGS + doves) / (len(doveData) + 1)) / c.INITIAL_BEINGS * 100
    hawkAveragePercentage = 100 - doveAveragePercentage
    doveData.append(doves)
    hawkData.append(hawks)

    #Matplotlib Plotting
    fig.clear()
    plt.axis([0, len(doveData), 0, c.INITIAL_BEINGS])
    plt.plot(doveData, label="Doves")
    plt.plot(hawkData, label="Hawks")
    plt.xlabel("Generation")
    plt.ylabel("Population Size")
    plt.title("Graph showing Population Size over Generations")
    plt.legend(loc="upper left")
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    #Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Update screen
    pygame.display.update()
#Quit
pygame.quit()