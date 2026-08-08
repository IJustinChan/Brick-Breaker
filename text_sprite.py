import pygame
from my_sprite import mySprite

class TextSprite(mySprite):
    def __init__(self, TEXT, F_FAMILY="Arial", F_SIZE=36, X=0, Y=0):
        mySprite.__init__(self, x=X, y=Y)
        self.__Text = TEXT
        self.__FontFamily = F_FAMILY
        self.__FontSize = F_SIZE
        self.__Font = pygame.font.SysFont(self.__FontFamily, self.__FontSize)
        self._Surface = self.__Font.render(self.__Text, True, self._Color)

    def UpdateText(self, NEW_TEXT): # Change the words the text is showing
        self.__Text = NEW_TEXT
        self._Surface = self.__Font.render(self.__Text, True, self._Color)
