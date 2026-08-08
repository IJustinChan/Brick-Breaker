import pygame
from my_sprite import mySprite

class UpperBlock(mySprite): # Create the upper boundary of the game
    def __init__(self, Width, Height):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)
