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
    def __init__(self, Width=1, Height=1, x=0, y=0, Speed=5, Color=(255, 255, 255)):
        self.__Width = Width
        self.__Height = Height
        self._Dimensions = (self.__Width, self.__Height)
        self.__x = x
        self.__y = y
        self.__Position = (self.__x, self.__y)
        self._Color = Color
        self.__Speed = Speed
        self._Surface = pygame.Surface
        self.__DirX = 1
        self.__DirY = 1
    
    def SetX(self, x):
        self.__x = x
        self.__Position = (self.__x, self.__y)
    
    def SetY(self, y):
        self.__y = y
        self.__Position = (self.__x, self.__y)
    
    def SetPosition(self, x, y):
        self.SetX(x)
        self.SetY(y)
    
    def SetSpeed(self, SPEED):
        self.__Speed = SPEED
    
    def SetColor(self, COLOR):
        self._Color = COLOR
        self._Surface.fill(self._Color)
    
    def LeftRightMove(self, PRESSED_KEYS):
        if PRESSED_KEYS[pygame.K_d] == 1:
            self.__x += self.__Speed
        if PRESSED_KEYS[pygame.K_a] == 1:
            self.__x -= self.__Speed
        self.SetPosition(self.__x, self.__y)

    # def WASDmove(self, PRESSED_KEYS):
    #     if PRESSED_KEYS[pygame.K_d] == 1:
    #         self.__x += self.__Speed
    #     if PRESSED_KEYS[pygame.K_a] == 1:
    #         self.__x -= self.__Speed
    #     if PRESSED_KEYS[pygame.K_w] == 1:
    #         self.__y -= self.__Speed
    #     if PRESSED_KEYS[pygame.K_s] == 1:
    #         self.__y += self.__Speed
    #     self.SetPosition(self.__x, self.__y)
    
    def CheckBoundaries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        if self.__x > MAX_X - self.GetWidth():
            self.__x = MAX_X - self.GetWidth()
        if self.__x < MIN_X:
            self.__x = MIN_X
        if self.__y > MAX_Y - self.GetHeight():
            self.__y = MAX_Y - self.GetHeight()
        if self.__y < MIN_Y:
            self.__y = MIN_Y
        self.__Position = (self.__x, self.__y)

    # --- Accessor Methods ---
    def GetPosition(self):
        return self.__Position
    
    def GetSurface(self):
        return self._Surface

    def GetWidth(self):
        return self._Surface.get_width()
    
    def GetHeight(self):
        return self._Surface.get_height()

class Ball(mySprite):
    pass

class PaddleSprite(mySprite):
    def __init__(self, Width=1, Height=1):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

class Brick(mySprite):
    pass

class Text(mySprite):
    pass

class UpperBlock(mySprite):
    def __init__(self, Width, Height):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

if __name__ == "__main__":
    Window = WINDOW("Brick Breaker", 500, 600, 60)

    TopBoundary = UpperBlock(Window.GetWidth(), 50)
    TopBoundary.SetColor((0, 0, 0))

    Paddle = PaddleSprite(100, 20)
    Paddle.SetPosition(Window.GetWidth()/2 - Paddle.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 30)

    while True:
        # --- INPUTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        PRESSED_KEYS = pygame.key.get_pressed()
        # --- PROCESSING ---
        Paddle.LeftRightMove(PRESSED_KEYS)
        Paddle.CheckBoundaries(Window.GetWidth(), Window.GetHeight())

        Window.ClearScreen()
        Window.GetSurface().blit(Paddle.GetSurface(), Paddle.GetPosition())

        Window.GetSurface().blit(TopBoundary.GetSurface(), TopBoundary.GetPosition())
        Window.UpdateFrame()






