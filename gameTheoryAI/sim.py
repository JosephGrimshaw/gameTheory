import consts as c
from creature import Creature
import random
import extraFunctions as ef

def runSim(generations, scoreWeights):
    ############################
    ########### Vars ###########
    ############################
    #Initial dove and hawk numbers. Declared here to avoid error with labels drawing before first data point
    doves = 0
    hawks = 0

    ############################
    ##### Create Objects #######
    ############################
    #Create creature group
    creatureGroup = []

    #Create initial creatures
    for i in range(int(c.INITIAL_BEINGS/2)):
        newCreature = Creature(False, random.randint(1,500))
        creatureGroup.append(newCreature)
        doves += 1
    for i in range(int(c.INITIAL_BEINGS/2)):
        newCreature = Creature(True, random.randint(1,500))
        creatureGroup.append(newCreature)
        hawks += 1
    #Get initial percentages of doves and hawks and give a value to graphing data to avoid errors in first render
    hawkFraction = hawks/c.INITIAL_BEINGS

    ############################
    ######## GAME LOOP #########
    ############################

    for generation in range(generations):
        #Force all creatures to confront another and change score accordingly
        ef.fightAllCreatures(creatureGroup, scoreWeights)
        #Remove any with score lower than -100 or ended lifespan. Tick lifespan.
        ef.removeDead(creatureGroup)
        #Replace removed dead
        for k in ef.getNextGeneration(creatureGroup):
            newCreature = Creature(k.fightChoice, 50)
            creatureGroup.append(newCreature)
        #Fill next plot of data in data array and set current dove and hawk numbers
        doves, hawks = ef.getNextGraphReading(creatureGroup)
        #Get new average percentages
        hawkFraction = (hawks / c.INITIAL_BEINGS)
    print(hawkFraction)
    return hawkFraction


runSim(500, {
                "fightWinScore": 50,
                "fightLoseScore": -50,
                "scareWinScore": 50,
                "threatWinScore": 40,
                "threatLoseScore": -10
            })
