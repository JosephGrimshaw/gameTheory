import consts as c
import math
import pygame

class World():
    def __init__(self):
        pass

    def draw_grid(self, WIN):
        for i in range(c.SQUARE_SIZE + 1):
            pygame.draw.line(WIN, (255,255,255), (15 + i*c.SQUARE_WIDTH, 15), (15+i*c.SQUARE_WIDTH, 735), 1)
            pygame.draw.line(WIN, (255,255,255), (15, 15 + i*c.SQUARE_WIDTH), (735, 15 + i*c.SQUARE_WIDTH), 1)