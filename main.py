"""
name: Brick Breaker
author: Justin Chan
date: 2025-02-06
"""

import pygame
pygame.init()

# --- WINDOW CLASS ---
class WINDOW:
    def __init__(self, TITLE, WIDTH, HEIGHT, FPS):
        self.__Title = TITLE
        self.__FPS = FPS
        self.__Width = WIDTH
        self.__Height = HEIGHT
        self.__ScreenDimensions = (self.__Width, self.__Height)
        self.__Clock = pygame.time.Clock()
        self.__Surface = pygame.display.set_mode(self.__ScreenDimensions)
        self.__Surface.fill((128, 128, 128))
        pygame.display.set_caption(self.__Title)

    def ClearScreen(self):
        self.__Surface.fill((128, 128, 128))

    def UpdateFrame(self):
        self.__Clock.tick(self.__FPS)
        pygame.display.flip()

    def GetSurface(self):
        return self.__Surface

    def GetWidth(self):
        return self.__Width

    def GetHeight(self):
        return self.__Height

class mySprite:
    pass

class Ball(mySprite):
    pass

class Paddle(mySprite):
    pass

class Brick(mySprite):
    pass

class Text:
    pass

if __name__ == "__main__":
    Window = WINDOW("Brick Breaker", 500, 500, 60)
    while True:
        # --- INPUTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Window.ClearScreen()
        Window.UpdateFrame()






