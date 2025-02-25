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

    def WASDmove(self, PRESSED_KEYS):
        if PRESSED_KEYS[pygame.K_d] == 1:
            self.__x += self.__Speed
        if PRESSED_KEYS[pygame.K_a] == 1:
            self.__x -= self.__Speed
        if PRESSED_KEYS[pygame.K_w] == 1:
            self.__y -= self.__Speed
        if PRESSED_KEYS[pygame.K_s] == 1:
            self.__y += self.__Speed
        self.SetPosition(self.__x, self.__y)

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

    # Another example of polymorphism here as the child's class method shares the same name as parent's method
    # However, it checks boundaries in a different way due to how the ball differs from other sprites
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

    def HitBottomEdge(self, MAX_Y):
        POSITION = self.GetPosition()
        if POSITION[1] + self.GetHeight() > MAX_Y:
            return True
        return False
    
    def isCollision(self, Width, Height, Position):
        """
        Test if the ball has collided with another sprite (mainly the brick)
        Use the width, height and position of an external sprite to if Ball object is in collision
        The ball x and y directions are modified accordingly depending on which vertex is hitting the external sprite
        :param WIDTH: int
        :param HEIGHT: int
        :param POS: tuple
        :return:
        """
        # Polymorphism is utilized here as the child class modifies the parent's class method
        if mySprite.isCollision(self, Width, Height, Position) is True:
            BallPosition = Ball.GetPosition()
            BallX = BallPosition[0]
            BallY = BallPosition[1]

            BallVertices = [
                (BallX, BallY), # Top-left vertex
                (BallX + self.GetWidth(), BallY), # Top-right vertex
                (BallX, BallY + self.GetHeight()), # Bottom-left vertex
                (BallX + self.GetWidth(), BallY + self.GetHeight()) # Bottom-right vertex
                ]

            BrickX = Position[0]
            BrickY = Position[1]

            BrickLeftSide = BrickX
            BrickRightSide = BrickX + Width
            BrickTopSide = BrickY
            BrickBottomSide = BrickY + Height

            XDirChanged = False
            YDirChanged = False

            for VertexX, VertexY in BallVertices:
                # Check to make sure the vertex collides with the ball
                if (VertexX >= BrickLeftSide and VertexX <= BrickRightSide) and (VertexY >= BrickTopSide and VertexY <= BrickBottomSide):
                    # Find the distance VertexX is to right and left side, and find the distance VertexY is to top and bottom side.
                    LeftSideDistance = abs(VertexX - BrickLeftSide)
                    RightSideDistance = abs(VertexX - BrickRightSide)
                    TopSideDistance = abs(VertexY - BrickTopSide)
                    BottomSideDistance = abs(VertexY - BrickBottomSide)

                    # Minimum distance the vertex is to one side tells us which side of the brick the ball collided with
                    MinDistance = min(LeftSideDistance, RightSideDistance, TopSideDistance, BottomSideDistance)

                    # Check the minimum distance value to determine which direction needs to be reversed
                    if MinDistance == LeftSideDistance or MinDistance == RightSideDistance: # The ball hit the left or right edge so x-direction needs to be reversed
                        if XDirChanged is False:
                            Ball.ChangeDirX(Ball.GetDirX()*-1)
                            XDirChanged = True
                    # Use another if-statement just in case the Ball's vertex collided with the Brick's vertex
                    if MinDistance == TopSideDistance or MinDistance == BottomSideDistance: # The ball hit the top or bottom side so reverse the y-direction
                        if YDirChanged is False:
                            Ball.ChangeDirY(Ball.GetDirY()*-1)
                            YDirChanged = True

            return True
        return False # No collision between the ball and brick

    def SetBallAtPaddle(self, PADDLE_POS, WIDTH, HEIGHT):
        PaddleX = PADDLE_POS[0]
        PaddleY = PADDLE_POS[1]

        Ball.SetPosition(PaddleX + (WIDTH/2) - Ball.GetWidth()/2, PaddleY - Ball.GetHeight() - 5)

class PaddleSprite(mySprite):
    def __init__(self, Width=1, Height=1):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

    def LaunchBall(self, PRESSED_KEYS, BALL):
        if PRESSED_KEYS[pygame.K_d] == 1 or PRESSED_KEYS[pygame.K_RIGHT] == 1:
            BALL.ChangeDirX(1)
        elif PRESSED_KEYS[pygame.K_a] == 1 or PRESSED_KEYS[pygame.K_LEFT] == 1:
            BALL.ChangeDirX(-1)
        else:
            BALL.ChangeDirX(1)

class Brick(mySprite):
    def __init__(self, HEALTH, Width=1, Height=1, X=0, Y=0):
        mySprite.__init__(self, Width, Height, x=X, y=Y)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)
        self.__Health = HEALTH

    # def __str__(self):
    #     return self.GetPosition()
    
    # def __repr__(self):
    #     return f"{self.__str__()}"
    
    # --- Methods ---

    def LoseHealth(self):
        self.__Health -= 1
    
    def MoveDown(self, POSITION, SPEED):
        PositionX = POSITION[0]
        PositionY = POSITION[1] + SPEED
        self.SetPosition(PositionX, PositionY)

    # --- Accessors ---
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
def CreateBricks(NUM_ROWS, NUM_COLUMNS, LEVEL, WIDTH, HEIGHT, COLORS, INSIDE_SCREEN=True):
    BricksArr = []
    PaddingX = 10
    PaddingY = 10
    if LEVEL > 3:
        MaxHealth = 4
    else:
        MaxHealth = LEVEL + 1
    MaxY = (NUM_ROWS - 1)*(PaddingY + HEIGHT) # Makes it 80 pixels above the screen
    for i in range(NUM_ROWS):
        for j in range(NUM_COLUMNS):
            Health = random.randint(1, MaxHealth)
            XPOS = (PaddingX + WIDTH)*j + 60
            if INSIDE_SCREEN is True:
                YPOS = (PaddingY + HEIGHT)*i + 80
            else:
                YPOS = (PaddingY + HEIGHT)*i - MaxY #+ 100  #- 250 # + 80
            BricksArr.append(Brick(Health, WIDTH, HEIGHT, XPOS, YPOS))
            BricksArr[-1].SetColor(COLORS[Health])

    return BricksArr


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
    Lives = 3

    # --- Text Sprites ---
    TitleText = TextSprite("BRICK BREAKER!", "Comic sans", 25)
    TitleText.SetPosition(Window.GetWidth()/2 - TitleText.GetWidth()/2, 0)

    ScoreText = TextSprite("Score: " + str(Score), "Comic sans", 25)
    ScoreText.SetPosition(0, 0)

    LevelText = TextSprite("Level: " + str(Level), "Comic sans", 18)
    LevelText.SetPosition(Window.GetWidth() - LevelText.GetWidth() - 10, 0)

    StartText = TextSprite("Press SPACE to start!", "Comic sans", 30)
    StartText.SetPosition(Window.GetWidth()/2 - StartText.GetWidth()/2, Window.GetHeight()/2 + 80)

    LivesText = TextSprite("Lives: " + str(Lives), "Comic sans", 18)
    LivesText.SetPosition(Window.GetWidth() - LivesText.GetWidth() - 10, LevelText.GetHeight())

    # --- Other Sprites ---
    TopBoundary = UpperBlock(Window.GetWidth(), 50)
    TopBoundary.SetColor((0, 0, 0))

    Paddle = PaddleSprite(100, 10)
    Paddle.SetPosition(Window.GetWidth()/2 - Paddle.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 30)

    # BallYInitialPath = [1, -1]
    Ball = BallSprite(20, 20, 4.5)
    PaddleStartPos = Paddle.GetPosition()
    Ball.SetBallAtPaddle(PaddleStartPos, Paddle.GetWidth(), Paddle.GetHeight())

    # Ball.SetPosition(Window.GetWidth()/2 - Ball.GetWidth()/2, Window.GetHeight()/2 - Ball.GetHeight()/2 - 130) # Main
    # Ball.SetPosition(Window.GetWidth()/2 - Ball.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 80)
    # Ball.ChangeDirX(random.choice(BallYInitialPath))

    SingleBrick = Brick(1, 65, 35, 250, 400)

    # --- Brick variables ---
    NumRows = 6
    NumColumns = 6
    BrickWidth = 50
    BrickHeight = 35
    MoveBricksDown = False
    Counter = (NumRows - 1)*(10 + BrickHeight) + 80

    BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, True)

    StartGame = False # Game only starts once the player presses the space bar
    CanShootBall = True # Set it to True so player can shoot the ball at the beginning of the game

    while True:
        # --- INPUTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        PRESSED_KEYS = pygame.key.get_pressed()

        # --- PROCESSING ---
        if StartGame is False:
            if PRESSED_KEYS[pygame.K_SPACE]:
                StartGame = True
        else:
            Paddle.LeftRightMove(PRESSED_KEYS)
            Paddle.CheckBoundaries(Window.GetWidth(), Window.GetHeight())

            if CanShootBall is True:
                Ball.SetBallAtPaddle(Paddle.GetPosition(), Paddle.GetWidth(), Paddle.GetHeight())
                if PRESSED_KEYS[pygame.K_b] == 1:
                    Paddle.LaunchBall(PRESSED_KEYS, Ball)
                    CanShootBall = False
            else:
                Ball.Move(Ball.GetPosition())
            # Ball.WASDmove(PRESSED_KEYS)
            Ball.CheckBoundaries(Window.GetWidth(), Window.GetHeight(), 0, TopBoundary.GetHeight())

            # if Ball.HitBottomEdge(Window.GetHeight()) is True:
            #     Lives -= 1
            #     if Lives <= 0:
            #         pass # End the game
            #     else:
            #         pass

            # Ball.isCollision(SingleBrick.GetWidth(), SingleBrick.GetHeight(), SdingleBrick.GetPosition(), None)

            if MoveBricksDown is True:
                for brick in BricksList:
                    brick.MoveDown(brick.GetPosition(), 4)
                Counter -= 4
                if Counter <= 0:
                    MoveBricksDown = False

            for brick in BricksList:
                if Ball.isCollision(brick.GetWidth(), brick.GetHeight(), brick.GetPosition()) is True:
                    brick.LoseHealth()
                    Score += 1
                    if brick.GetHealth() <= 0:
                        BricksList.remove(brick)
                    else:
                        brick.SetColor(BrickColors[brick.GetHealth()])
            
            if len(BricksList) == 0:
                Level += 1
                BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, False)
                MoveBricksDown = True
                Counter = (NumRows - 1)*(10 + BrickHeight) + 80

            if Paddle.isCollision(Ball.GetWidth(), Ball.GetHeight(), Ball.GetPosition()):
                # Ball.ChangeDirY(Ball.GetDirY()*-1)
                BallPosition = Ball.GetPosition()
                BallX = BallPosition[0]
                BallY = BallPosition[1]
                
                PaddlePosition = Paddle.GetPosition()
                PaddleX = PaddlePosition[0]
                PaddleY = PaddlePosition[1]

                # --- Maybe put this inside a function ---

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

        if StartGame is False:
            Window.GetSurface().blit(StartText.GetSurface(), StartText.GetPosition())

        for brick in BricksList:
            Window.GetSurface().blit(brick.GetSurface(), brick.GetPosition())

        Window.GetSurface().blit(Paddle.GetSurface(), Paddle.GetPosition())
        Window.GetSurface().blit(Ball.GetSurface(), Ball.GetPosition())

        # Window.GetSurface().blit(SingleBrick.GetSurface(), SingleBrick.GetPosition())

        Window.GetSurface().blit(TopBoundary.GetSurface(), TopBoundary.GetPosition())

        Window.GetSurface().blit(TitleText.GetSurface(), TitleText.GetPosition())
        Window.GetSurface().blit(ScoreText.GetSurface(), ScoreText.GetPosition())
        Window.GetSurface().blit(LevelText.GetSurface(), LevelText.GetPosition())
        Window.GetSurface().blit(LivesText.GetSurface(), LivesText.GetPosition())
        Window.UpdateFrame()



