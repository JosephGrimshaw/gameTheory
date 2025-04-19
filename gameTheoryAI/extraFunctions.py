import consts as c
import random
import math

def fightAllCreatures(creatureGroup, scoreWeights):
    pairs = [tuple(random.sample(creatureGroup, 2)) for _ in range(math.floor(c.INITIAL_BEINGS/2))]
    for i, (creature1, creature2) in enumerate(pairs):
        getResults(creature1, creature2, scoreWeights)

def getResults(creature1, creature2, scores):
    creature1Fight = creature1.fightChoice
    creature2Fight = creature2.fightChoice
    if creature1Fight and creature2Fight:
        if random.choice([0,1]):
            creature1.score += scores["fightWinScore"]
            creature2.score += scores["fightLoseScore"]
        else:
            creature1.score += scores["fightLoseScore"]
            creature2.score += scores["fightWinScore"]
    elif creature1Fight:
        creature1.score += scores["scareWinScore"]
    elif creature2Fight:
        creature2.score += scores["scareWinScore"]
    else:
        if random.choice([0,1]):
            creature1.score += scores["threatWinScore"]
            creature2.score += scores["threatLoseScore"]
        else:
            creature1.score += scores["threatLoseScore"]
            creature2.score += scores["threatWinScore"]

def removeDead(creatureGroup):
     for creature in creatureGroup:
        if creature.score <= -100:
            creatureGroup.remove(creature)
        if creature.rollLifespan():
            creatureGroup.remove(creature)

def getNextGeneration(creatureGroup):
    spacesToFill = c.INITIAL_BEINGS-len(creatureGroup)
    weightsList = []
    creatureList = []
    livingCreature = False
    for creatureX in creatureGroup:
        creatureList.append(creatureX)
        if creatureX.score <= 0:
            weightsList.append(0)
        else:
            weightsList.append(creatureX.score)
            livingCreature = True
    if livingCreature:
        winners = random.choices(creatureList, weights=weightsList, k=c.INITIAL_BEINGS-len(creatureList))
    winners = random.choices(creatureList, k=c.INITIAL_BEINGS-len(creatureList))
    return winners

def getNextGraphReading(creatureGroup):
    doves = 0
    hawks = 0
    for creature in creatureGroup:
        if creature.fightChoice == True:
            hawks += 1
        else:
            doves += 1
    return doves, hawks