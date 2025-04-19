import consts as c
import random
import math

def drawCreatures(creatureGroup, WIN):
    i = 0
    j = 0
    for creature in creatureGroup:
                #creature.rollMutate()
                if (i+1)*c.SQUARE_SIZE - j <= c.INITIAL_BEINGS:
                    creature.draw(WIN, 16 + j*c.SQUARE_WIDTH, 16+i*c.SQUARE_WIDTH)
                j += 1
                if j >= c.SQUARE_SIZE:
                    j = 0
                    i += 1

def fightAllCreatures(creatureGroup):
    allCreatures = list(creatureGroup.sprites())
    pairs = [tuple(random.sample(allCreatures, 2)) for _ in range(math.floor(c.INITIAL_BEINGS/2))]
    for i, (creature1, creature2) in enumerate(pairs):
        getResults(creature1, creature2)

def getResults(creature1, creature2):
    creature1Fight = creature1.getFight()
    creature2Fight = creature2.getFight()
    if creature1Fight and creature2Fight:
        if random.choice([0,1]):
            creature1.score += c.SCORES['fightWinScore']
            creature2.score += c.SCORES['fightLoseScore']
        else:
            creature1.score += c.SCORES['fightLoseScore']
            creature2.score += c.SCORES['fightWinScore']
    elif creature1Fight:
        creature1.score += c.SCORES['scareWinScore']
    elif creature2Fight:
        creature2.score += c.SCORES['scareWinScore']
    else:
        if random.choice([0,1]):
            creature1.score += c.SCORES['threatWinScore']
            creature2.score -= c.SCORES['threatLoseScore']
        else:
            creature1.score -= c.SCORES['threatLoseScore']
            creature2.score += c.SCORES['threatWinScore']

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
    for creatureX in creatureGroup:
        creatureList.append(creatureX)
        if creatureX.score <= 0:
            weightsList.append(0)
        else:
            weightsList.append(creatureX.score)
    winners = random.choices(creatureList, weights=weightsList, k=c.INITIAL_BEINGS-len(creatureList))
    return winners

def getNextGraphReading(creatureGroup):
    doves = 0
    hawks = 0
    for creature in creatureGroup:
        if creature.fightChance == 100:
            hawks += 1
        elif creature.fightChance == 0:
            doves += 1
    return doves, hawks

def draw_text(WIN, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x,y))

def draw_labels(WIN, doves, hawks, doveAveragePercentage, hawkAveragePercentage, font):
    #Dove labels (numbers, percentage)
    draw_text(WIN, "Doves: " + str(doves), font, (255,255,255), 765, 200)
    draw_text(WIN, f"({round(doves/c.INITIAL_BEINGS*100, 2)}%)", font, (255,255,255), 770, 220)
    draw_text(WIN, "Avrg doves: " + str(round(doveAveragePercentage, 2)) + "%", font, (255,255,255), 765, 240)
    #Hawk numbers (numbers, percentage)
    draw_text(WIN, "Hawks: " + str(hawks), font, (255,255,255), 765, 360)
    draw_text(WIN, f"({round(hawks/c.INITIAL_BEINGS*100, 2)}%)", font, (255,255,255), 770, 380)
    draw_text(WIN, "Avrg hawks: " + str(round(hawkAveragePercentage, 2)) + "%", font, (255,255,255), 765, 400)