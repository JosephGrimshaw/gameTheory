import pygame
import consts as c
import random

class Creature(pygame.sprite.Sprite):
    def __init__(self, fightChance, lifespan):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.lifespan = 50
        self.fightChance = fightChance
        self.colour = fightChance*2.55

    def draw(self, WIN, x, y):
        pygame.draw.rect(WIN, (self.colour, 0, 255), pygame.Rect(x, y, c.SQUARE_WIDTH-1, c.SQUARE_WIDTH-1))
    
    def getFight(self):
        if random.randint(0,100) <= self.fightChance:
            return True
        return False
    
    def rollMutate(self):
        if random.randint(0,1000) == 21:
            self.fightChance = random.randint(0,100)
            self.colour = self.fightChance*2.55

    def rollLifespan(self):
        '''
        if random.choice([0,1]):
            self.lifespan -= 1
        if self.lifespan:
            return False
        return True
        '''
        return False