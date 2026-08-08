import pygame
from my_sprite import mySprite

class Brick(mySprite):
    def __init__(self, HEALTH, Width=1, Height=1, X=0, Y=0, Type="Regular"):
        # Abstraction is utilized here where the Brick class only has attributes needed for this program
        # Important attributes of the brick include its health, width, legnth, x and y position,
        mySprite.__init__(self, Width, Height, x=X, y=Y)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)
        self.__Health = HEALTH
        self.__Type = Type
    
    # --- Methods ---
    def LoseHealth(self):
        self.__Health -= 1

    # --- Accessors ---
    def GetHealth(self):
        return self.__Health
    
    def GetType(self):
        return self.__Type
