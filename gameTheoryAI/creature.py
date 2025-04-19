import consts as c
import random

class Creature():
    def __init__(self, fightChoice, lifespan):
        self.score = 0
        self.lifespan = 50
        self.fightChoice = fightChoice
    
    def rollMutate(self):
        if random.randint(0,1000) == 21:
            self.fightChoice = random.choice([True, False])

    def rollLifespan(self):
        '''
        if random.choice([0,1]):
            self.lifespan -= 1
        if self.lifespan:
            return False
        return True
        '''
        return False