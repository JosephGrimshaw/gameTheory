import pygame

class Button():
    def __init__(self, x, y, image, altImage, single_click=True):
        self.image = image
        self.altImage = altImage
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface, mode=True):
        action = False
        #Mouse position
        pos = pygame.mouse.get_pos()

        #Mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                #If button is single-click, set clicked to true
                if self.single_click:
                    self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #Draw button
        if mode:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.altImage, self.rect)

        return action