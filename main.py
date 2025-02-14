"""
name: Brick Breaker
author: Justin Chan
date: 2025-02-06
"""

import pygame
import random

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
        if PRESSED_KEYS[pygame.K_d] == 1 or PRESSED_KEYS[pygame.K_RIGHT] == 1:
            self.__x += self.__Speed
        if PRESSED_KEYS[pygame.K_a] == 1 or PRESSED_KEYS[pygame.K_LEFT] == 1:
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

    def isCollision(self, Width, Height, Position):
        if Position[0] + Width >= self.__x and Position[0] <= self.__x + self.GetWidth():
            if Position[1] + Height >= self.__y and Position[1] <= self.__y + self.GetHeight():
                return True
        return False

    def ChangeDirX(self, NEW_VAL):
        self.__DirX = NEW_VAL

    def ChangeDirY(self, NEW_VAL):
        self.__DirY = NEW_VAL

    # --- Accessor Methods ---
    def GetPosition(self):
        return self.__Position

    def GetSurface(self):
        return self._Surface

    def GetWidth(self):
        return self._Surface.get_width()

    def GetHeight(self):
        return self._Surface.get_height()

    def GetDirX(self):
        return self.__DirX

    def GetDirY(self):
        return self.__DirY

    def GetSpeed(self):
        return self.__Speed

class BallSprite(mySprite):
    def __init__(self, Width=1, Height=1, Speed=5):
        mySprite.__init__(self, Width=Width, Height=Height, Speed=Speed)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

    def Move(self, POSITION):
        PositionX = POSITION[0] + (self.GetSpeed()*self.GetDirX())
        PositionY = POSITION[1] + (self.GetSpeed()*self.GetDirY())
        self.SetPosition(PositionX, PositionY)

    def CheckBoundaries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0): # Incomplete
        # mySprite.CheckBoundaries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0)
        POSITION = self.GetPosition()
        if POSITION[0] + self.GetWidth() > MAX_X:
            self.ChangeDirX(-1)
        elif POSITION[0] < MIN_X:
            self.ChangeDirX(1)
        elif POSITION[1] < MIN_Y:
            self.ChangeDirY(1)
        elif POSITION[1] + self.GetHeight() > MAX_Y: # Player lose so change this
            self.ChangeDirY(-1)

class PaddleSprite(mySprite):
    def __init__(self, Width=1, Height=1):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

class Brick(mySprite):
    def __init__(self, HEALTH, Width=1, Height=1, X=0, Y=0):
        mySprite.__init__(self, Width, Height, x=X, y=Y)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)
        self.__Health = HEALTH

    def isCollision(self, Width, Height, Position):
        if mySprite.isCollision(Width, Height, Position) is True: # MAYBE USE POLYMORPHISM HERE
            pass

    def LoseHealth(self):
        self.__Health -= 1

    def GetHealth(self):
        return self.__Health

class TextSprite(mySprite):
    def __init__(self, TEXT, F_FAMILY="Arial", F_SIZE=36, X=0, Y=0):
        mySprite.__init__(self, x=X, y=Y)
        self.__Text = TEXT
        self.__FontFamily = F_FAMILY
        self.__FontSize = F_SIZE
        self.__Font = pygame.font.SysFont(self.__FontFamily, self.__FontSize)
        self._Surface = self.__Font.render(self.__Text, True, self._Color)

    def UpdateText(self, NEW_TEXT):
        self.__Text = NEW_TEXT
        self._Surface = self.__Font.render(self.__Text, True, self._Color)

class UpperBlock(mySprite):
    def __init__(self, Width, Height):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

# --- INPUTS ---

# --- PROCESSING ---
def CreateBricks(NUM_BRICKS, LEVEL, WIDTH, HEIGHT): # INCOMPELTE AT THE MOMENT
    BricksArr = []
    StartX = 0
    StartY = 0
    if LEVEL > 4:
        MaxHealth = 4
    else:
        MaxHealth = LEVEL
    for i in range(NUM_BRICKS):
        Health = random.randint(1, MaxHealth)
        XPOS = (StartX + WIDTH + 10)*(i % 6)
        YPOS = (StartY + HEIGHT + 10) # FIX THIS
        BricksArr.append(Brick(Health, WIDTH, HEIGHT))


# --- OUTPUTS ---


if __name__ == "__main__":
    Window = WINDOW("Brick Breaker", 475, 630, 60)

    # --- Colors ---
    BrickColors = {
        1: (255, 255, 255),
        2: (255, 255, 102),
        3: (255, 153, 51),
        4: (204, 0, 0)
    }

    # --- Variables ---
    Score = 0
    Level = 1

    # --- Text Sprites ---
    TitleText = TextSprite("BRICK BREAKER!", "Comic sans", 25)
    TitleText.SetPosition(Window.GetWidth()/2 - TitleText.GetWidth()/2, 0)

    ScoreText = TextSprite("Score: " + str(Score), "Comic sans", 25)
    ScoreText.SetPosition(0, 0)

    LevelText = TextSprite("Level: " + str(Level), "Comic sans", 25)
    LevelText.SetPosition(Window.GetWidth() - LevelText.GetWidth() - 10, 0)

    TopBoundary = UpperBlock(Window.GetWidth(), 50)
    TopBoundary.SetColor((0, 0, 0))

    Paddle = PaddleSprite(100, 10)
    Paddle.SetPosition(Window.GetWidth()/2 - Paddle.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 30)

    Ball = BallSprite(20, 20, 4.5)
    Ball.SetPosition(Window.GetWidth()/2 - Ball.GetWidth()/2, Window.GetHeight()/2 - Ball.GetHeight()/2)

    SingleBrick = Brick(1, 65, 35, 100, 100)

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

        Ball.Move(Ball.GetPosition())
        Ball.CheckBoundaries(Window.GetWidth(), Window.GetHeight(), 0, TopBoundary.GetHeight())

        if Paddle.isCollision(Ball.GetWidth(), Ball.GetHeight(), Ball.GetPosition()):
            # Ball.ChangeDirY(Ball.GetDirY()*-1)
            BallPosition = Ball.GetPosition()
            BallX = BallPosition[0]
            BallY = BallPosition[1]
            
            PaddlePosition = Paddle.GetPosition()
            PaddleX = PaddlePosition[0]
            PaddleY = PaddlePosition[1]

            # --- Maybe put this inside a function ---
            Ball_BottomRight = (BallX + Ball.GetWidth(), BallY + Ball.GetHeight())
            Ball_BottomLeft = (BallX, BallY + Ball.GetHeight())

            if BallX >= PaddleX and BallX + Ball.GetWidth() <= PaddleX + Paddle.GetWidth():
                Ball.ChangeDirY(Ball.GetDirY()*-1)
            else:
                if BallX >= PaddleX and BallX + Ball.GetWidth() > PaddleX + Paddle.GetWidth() and Ball.GetDirX() == 1:
                    Ball.ChangeDirY(Ball.GetDirY() * -1)
                elif BallX + Ball.GetWidth() <= PaddleX + Paddle.GetWidth() and BallX < PaddleX and Ball.GetDirX() == -1:
                    Ball.ChangeDirY(Ball.GetDirY() * -1)
                else:
                    Ball.ChangeDirY(Ball.GetDirY()*-1)
                    Ball.ChangeDirX(Ball.GetDirX()*-1)

            while Paddle.isCollision(Ball.GetWidth(), Ball.GetHeight(), Ball.GetPosition()):
                Ball.Move(Ball.GetPosition())

            # Ball.SetPosition(Ball.GetPosition()[0], Paddle.GetPosition()[1])
            # Ball.ChangeDirX(Ball.GetDirX()*-1)


        ScoreText.UpdateText("Score: " + str(Score)) # Maybe an if-statement for this when the score actually changes

        LevelText.UpdateText("Level: " + str(Level)) # Put this after a level has been cleared
        LevelText.SetPosition(Window.GetWidth() - LevelText.GetWidth() - 10, 0)

        # --- OUTPUTS ---
        Window.ClearScreen()
        Window.GetSurface().blit(Paddle.GetSurface(), Paddle.GetPosition())
        Window.GetSurface().blit(Ball.GetSurface(), Ball.GetPosition())

        Window.GetSurface().blit(SingleBrick.GetSurface(), SingleBrick.GetPosition())

        Window.GetSurface().blit(TopBoundary.GetSurface(), TopBoundary.GetPosition())

        Window.GetSurface().blit(TitleText.GetSurface(), TitleText.GetPosition())
        Window.GetSurface().blit(ScoreText.GetSurface(), ScoreText.GetPosition())
        Window.GetSurface().blit(LevelText.GetSurface(), LevelText.GetPosition())
        Window.UpdateFrame()



