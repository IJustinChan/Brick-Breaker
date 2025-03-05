"""
name: Brick Breaker
author: Justin Chan
date: 2025-02-06
"""

import pygame
import random
import time

pygame.init()

# --- WINDOW CLASS ---
class WINDOW:
    def __init__(self, TITLE, WIDTH, HEIGHT, FPS):
        # Encapsulation is utilized here to protect the WINDOW class's attributes
        # This prevents the other classes from directly accessing WINDOW's attributes
        self.__Title = TITLE
        self.__FPS = FPS
        self.__Width = WIDTH
        self.__Height = HEIGHT
        self.__ScreenDimensions = (self.__Width, self.__Height) # Create the dimensions of the screen
        self.__Clock = pygame.time.Clock() # Create pygame clock object
        self.__Surface = pygame.display.set_mode(self.__ScreenDimensions) # Create the screen
        self.__Surface.fill((128, 128, 128)) # Make the background color gray
        pygame.display.set_caption(self.__Title) # Create the game's title

    # --- Methods ---
    def ClearScreen(self):
        self.__Surface.fill((128, 128, 128))

    def UpdateFrame(self):
        self.__Clock.tick(self.__FPS) # Make the game run at the specified FPS
        pygame.display.flip() # Update the game's window

    # --- Accessors ---
    def GetSurface(self):
        return self.__Surface

    def GetWidth(self):
        return self.__Width

    def GetHeight(self):
        return self.__Height

class mySprite:
    def __init__(self, Width=1, Height=1, x=0, y=0, Speed=5, Color=(255, 255, 255)):
        # Encapsulation is used here for most of these attributes to protect them
        # This makes it so they can only be accessed using setter and getter methods
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

    # --- Methods ---
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

    def SetColor(self, COLOR): # Allows the sprites' colors to be changed
        self._Color = COLOR
        self._Surface.fill(self._Color)

    def LeftRightMove(self, PRESSED_KEYS):
        """
        Moves a sprite left or right
        :param PRESSED_KEYS: dict
        :return: None
        """
        if PRESSED_KEYS[pygame.K_d] == 1 or PRESSED_KEYS[pygame.K_RIGHT] == 1: # Move right using right arrow key or "D"
            self.__x += self.__Speed
        if PRESSED_KEYS[pygame.K_a] == 1 or PRESSED_KEYS[pygame.K_LEFT] == 1: # Move left using left arrrow key or "A"
            self.__x -= self.__Speed
        self.SetPosition(self.__x, self.__y) # Update the position

    def CheckBoundaries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        """
        Check to make sure the sprite does not go out of the window screen
        :param MAX_X: int
        :param MAX_Y: int
        :param MIN_X: int
        :param MIN_Y: int
        :return: None
        """
        if self.__x > MAX_X - self.GetWidth(): # Right edge
            self.__x = MAX_X - self.GetWidth()
        if self.__x < MIN_X: # Left edge
            self.__x = MIN_X
        if self.__y > MAX_Y - self.GetHeight(): # Bottom edge
            self.__y = MAX_Y - self.GetHeight()
        if self.__y < MIN_Y: # Top edge
            self.__y = MIN_Y
        self.__Position = (self.__x, self.__y)

    def isCollision(self, Width, Height, Position):
        """
        Use the width, height and position of an external sprite to test if it is colliding with the given sprite
        :param WIDTH: int
        :param HEIGHT: int
        :param POS: tuple
        :return: bool
        """
        if Position[0] + Width >= self.__x and Position[0] <= self.__x + self.GetWidth():
            if Position[1] + Height >= self.__y and Position[1] <= self.__y + self.GetHeight():
                return True
        return False

    def ChangeDirX(self, NEW_VAL): # Update x-direction variable
        self.__DirX = NEW_VAL

    def ChangeDirY(self, NEW_VAL): # Update y-direction variable
        self.__DirY = NEW_VAL
    
    def MoveDown(self, POSITION, SPEED): # Move a sprite down the screen
        PositionX = POSITION[0]
        PositionY = POSITION[1] + SPEED # Move it down using the sprite's speed
        self.SetPosition(PositionX, PositionY)

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

class BallSprite(mySprite): # Inheritance is used here as the ball sprite is inheriting the properties from parent class mySprite
    def __init__(self, Width=1, Height=1, Speed=5):
        mySprite.__init__(self, Width=Width, Height=Height, Speed=Speed) # Initialize the parent class
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

    def Move(self, POSITION):
        """
        Make the ball move in a diagonal path
        :param POSITION: tuple
        :return: None
        """
        PositionX = POSITION[0] + (self.GetSpeed()*self.GetDirX())
        PositionY = POSITION[1] + (self.GetSpeed()*self.GetDirY())
        self.SetPosition(PositionX, PositionY)

    # Polymorphism is used here as the child's class method shares the same name as parent's method
    # However, it checks boundaries in a different way due to how the ball differs from other sprites
    def CheckBoundaries(self, MAX_X, MAX_Y, MIN_X=0, MIN_Y=0):
        """
        Check to make sure the ball is inside the window's boundaries. A separate function checks the bottom edge.
        :param MAX_X: int
        :param MAX_Y: int
        :param MIN_X: int
        :param MIN_Y: int
        :return: None
        """
        POSITION = self.GetPosition() # Get the ball's current position
        if POSITION[0] + self.GetWidth() > MAX_X: # Hit the right edge
            self.ChangeDirX(-1) # Change the x-direction
        elif POSITION[0] < MIN_X: # Hit the left edge
            self.ChangeDirX(1)
        elif POSITION[1] < MIN_Y: # Hit the top edge
            self.ChangeDirY(1) # Change the y-direction

    def HitBottomEdge(self, MAX_Y): # Check to see if the ball has hit the bottom edge
        Position = self.GetPosition()
        if Position[1] > MAX_Y: # Ball has hit the bottom edge
            return True
        return False # Ball did not hit the bottom edge
    
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
        if mySprite.isCollision(self, Width, Height, Position) is True: # Collision has occurred between the ball and a brick
            BallPosition = self.GetPosition()
            BallX = BallPosition[0]
            BallY = BallPosition[1]

            # Put the ball's vertices in a list to make it easier to take each vertex into account
            BallVertices = [
                (BallX, BallY), # Top-left vertex
                (BallX + self.GetWidth(), BallY), # Top-right vertex
                (BallX, BallY + self.GetHeight()), # Bottom-left vertex
                (BallX + self.GetWidth(), BallY + self.GetHeight()) # Bottom-right vertex
                ]

            BrickX = Position[0]
            BrickY = Position[1]

            # Get the position of the brick's edges
            BrickLeftSide = BrickX
            BrickRightSide = BrickX + Width
            BrickTopSide = BrickY
            BrickBottomSide = BrickY + Height

            # These variables make it so the x and y direction of the ball can only be changed once
            XDirChanged = False
            YDirChanged = False

            for VertexX, VertexY in BallVertices: # Loop through each vertex and get their x and y positions
                # Check to make sure the vertex collides with the ball
                if (VertexX >= BrickLeftSide and VertexX <= BrickRightSide) and (VertexY >= BrickTopSide and VertexY <= BrickBottomSide):
                    # Find the distance VertexX is to right and left side, and find the distance VertexY is to top and bottom side.
                    LeftSideDistance = abs(VertexX - BrickLeftSide) # Use absolute value to get the positive distance so they are easier to compare
                    RightSideDistance = abs(VertexX - BrickRightSide)
                    TopSideDistance = abs(VertexY - BrickTopSide)
                    BottomSideDistance = abs(VertexY - BrickBottomSide)

                    # Minimum distance the vertex is to one side tells us which side of the brick the ball collided with
                    MinDistance = min(LeftSideDistance, RightSideDistance, TopSideDistance, BottomSideDistance)

                    # Check the minimum distance value to determine which direction needs to be reversed
                    if MinDistance == LeftSideDistance or MinDistance == RightSideDistance: # The ball hit the left or right edge so x-direction needs to be reversed
                        if XDirChanged is False:
                            self.ChangeDirX(self.GetDirX()*-1)
                            XDirChanged = True # Set it to be True to prevent the x-direction from being changed again

                    if MinDistance == TopSideDistance or MinDistance == BottomSideDistance: # The ball hit the top or bottom side so reverse the y-direction
                        if YDirChanged is False:
                            self.ChangeDirY(self.GetDirY()*-1)
                            YDirChanged = True

            return True # Indicate a collision has occurred after checking each vertices
        return False # No collision between the ball and brick

    def SetBallAtPaddle(self, PADDLE_POS, WIDTH):
        # Get the paddle's x and y position
        PaddleX = PADDLE_POS[0]
        PaddleY = PADDLE_POS[1]

        # Placed the ball around where the center of the paddle is
        self.SetPosition(PaddleX + (WIDTH/2) - self.GetWidth()/2, PaddleY - self.GetHeight() - 5) # Subtract by 5 to create space between ball and paddle so no collision occurs

class PaddleSprite(mySprite):
    def __init__(self, Width=1, Height=1):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

        # Variable to track of the paddle's current state (longer/shorter) after taking power ups
        # Zero means normal width, -1 means shorten one time, -2 means shorten twice, 1 means width increased once, and 2 means width increased twice
        # Player will lose points if this variable is -2 and the player will get points if this variable is 2
        self.__WidthState = 0

    # --- Methods ---
    def LaunchBall(self, PRESSED_KEYS, BALL):
        """
        Allows the player to shoot the ball from the paddle at the start of the game or when they just lost a life
        :param PRESSED_KEYS: dict
        :param BALL: obj
        :return: None
        """
        if PRESSED_KEYS[pygame.K_d] == 1 or PRESSED_KEYS[pygame.K_RIGHT] == 1: # Paddle is moving right so shoot the ball right
            BALL.ChangeDirX(1)
        elif PRESSED_KEYS[pygame.K_a] == 1 or PRESSED_KEYS[pygame.K_LEFT] == 1: # Paddle is moving left so shoot the ball left
            BALL.ChangeDirX(-1)
        else: # Paddle is not moving so shoot the ball right by default
            BALL.ChangeDirX(1)
    
    def ChangePaddleWidth(self, NEW_WIDTH):
        self._Surface = pygame.transform.scale(self._Surface, (NEW_WIDTH, self.GetHeight())) # Resize the paddle's width after hitting a power up or power down

    def UpdateWidthState(self, NEW_VAL):
        self.__WidthState = NEW_VAL
    
    # --- Accessors ---
    def GetWidthState(self):
        return self.__WidthState

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

class UpperBlock(mySprite): # Create the upper boundary of the game
    def __init__(self, Width, Height):
        mySprite.__init__(self, Width, Height)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)

class PaddleLengthPowerUp(mySprite): # Power up / power down sprite class
    def __init__(self, Type, Width, Height, Speed):
        mySprite.__init__(self, Width=Width, Height=Height, Speed=Speed)
        self._Surface = pygame.Surface(self._Dimensions, pygame.SRCALPHA, 32)
        self._Surface.fill(self._Color)
        # Abstraction is used here as the type of power up is the only additional information this program needs
        self.__PowerUpType = Type # Store what the power up does
    
    # --- Methods ---
    def UpdateColor(self, PowerUpType): # Change the power up color depending on what it does to player's paddle
        if PowerUpType == "Longer Paddle": # Makes the paddle longer
            self.SetColor((40, 212, 86))
        else: # Makes the paddle shorter
            self.SetColor((109, 33, 181))
    
    def SetPowerUpAtBrick(self, BRICK_POSITION, WIDTH, HEIGHT):
        """
        Create the power up or power down at where the poewr up brick was destroyed
        :param BRICK_POSITION: tuple
        :param WIDTH: int
        :param HEIGHT: int
        :return: None
        """
        BrickX = BRICK_POSITION[0]
        BrickY = BRICK_POSITION[1]

        # Create the power-up at the center of the brick
        CenterX = BrickX + (WIDTH/2) - self.GetWidth()/2
        CenterY = BrickY + (HEIGHT/2) - self.GetHeight()/2
        self.SetPosition(CenterX, CenterY)
    
    def CheckBoundaries(self, MAX_Y): # Check to see if the power up or power down reached the bottom of the screen
        Position = self.GetPosition()
        PowerUpY = Position[1]
        if PowerUpY > MAX_Y: # It has reached the bottom of the screen
            return True
        else:
            return False
    
    # --- Accessors ---
    def GetPowerUpType(self):
        return self.__PowerUpType
    

# --- INPUTS ---
# Users give their input through pygame and not the console so there are no inputs

# --- PROCESSING ---
def CreateBricks(NUM_ROWS, NUM_COLUMNS, LEVEL, WIDTH, HEIGHT, COLORS, INSIDE_SCREEN=True):
    """
    Create all the bricks in the game at a certain position. It also makes each brick have unique health and determines if they are power ups or not.
    :param NUM_ROWS: int
    :param NUM_COLUMNS: int
    :param LEVEL: int
    :param WIDTH: int
    :param HEIGHT: int
    :param COLORS: dict
    :param INSIDE_SCREEN: bool
    """
    BricksArr = [] # Store all the bricks created in this list. It utilizes aggregation.

    # Specify the padding between the bricks when they are created
    PaddingX = 10
    PaddingY = 10

    # Maximum health of the bricks is four, so ensure higher levels do not change the health
    if LEVEL > 3:
        MaxHealth = 4
    else:
        MaxHealth = LEVEL + 1

    # Specify the lowest y position the bricks will be created at. 
    # This will help us create the bricks off screen so they can move down once a new level starts
    MaxY = (NUM_ROWS - 1)*(PaddingY + HEIGHT)

    for i in range(NUM_ROWS):
        for j in range(NUM_COLUMNS):
            Health = random.randint(1, MaxHealth) # Generate random health of the brick

            BrickType = "Regular" # Assume the brick does not give power ups
            if Health == 1: # Only bricks with a health of one can give power ups
                if CalculatePowerUpChance() is True: # Determine if the brick with one health can be a power up brick
                    BrickType = "PowerUp"

            XPOS = (PaddingX + WIDTH)*j + 60 # Determine the x-position using its column number, x-padding, and width. Translate it 60 pixels to the right

            # This checks if we are creating the bricks inside the screen or outside the screen
            # When the user starts playing the game, the bricks will initially be created inside the screen.
            # After a level ends, bricks will be created outside the screen so they can move down.
            if INSIDE_SCREEN is True:
                YPOS = (PaddingY + HEIGHT)*i + 80 # Translate 80 pixels down as well to ensure bricks are not created in the top boundary
            else:
                YPOS = (PaddingY + HEIGHT)*i - MaxY # Subtract by MaxY to make the bricks above the screen

            # Aggregation is implemented here as the brick objects are being placed into the same list
            BricksArr.append(Brick(Health, WIDTH, HEIGHT, XPOS, YPOS, BrickType))

            if BrickType == "Regular": # Change the color of the brick depending on its health if it is a regular brick
                BricksArr[-1].SetColor(COLORS[Health])
            else: # Give power up bricks a special color
                BricksArr[-1].SetColor((63, 181, 191))

    return BricksArr

def CalculatePowerUpChance():
    """
    Decide if a brick with a health of one is a power up brick or not
    :return: bool
    """
    Chance = random.randint(1, 5) # Choose a random number between 1 and 5, inclusive
    if Chance <= 3: # 60% chance that brick is a power up brick
        return True
    else:
        return False

def DecidePowerUpType():
    """
    Decide if a power up or power down will be created after a power up brick is destroyed
    :return: str
    """
    LongerPaddleChance = random.randint(1, 4) # Both ends are inclusive
    if LongerPaddleChance == 1: # 25% chance it is a power up that makes the paddle longer
        return "Longer Paddle"
    else:
        return "Shorter Paddle"

# --- OUTPUTS ---
# No output functions since pygame will display the output in the window

# --- Main program code ---
def Main():
    Window = WINDOW("Brick Breaker", 475, 630, 60)

    # --- Colors ---
    BrickColors = {
        1: (255, 255, 255), # White
        2: (255, 255, 102), # Yellow
        3: (255, 153, 51), # Orange
        4: (204, 0, 0) # Red
    }

    # Possible Paddle widths depending on how much times they hit a power up
    # --- Paddle widths ---
    PaddleWidths = {
        0: 100, # When no power up is applied, its original width is 100
        -1: 60, # Hit a power up that decreases its width for the first time
        -2: 25, # Hit a power up that decreases its width for the second time
        1 : 125, # Power up increases its width first time
        2: 150 # Power up increases its width for the second time
    }

    # --- Variables ---
    Score = 0
    Level = 1
    Lives = 3
    GameOngoing = True # Variable to keep track if the player still has lives left

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

    GameOverText = TextSprite("Game Over!", "Comic sans", 40)
    GameOverText.SetPosition(-100, -100) # Set this sprite off screen
    GameOverText.SetColor((0, 0, 0))
    GameOverText.UpdateText("Game Over!") # This function applies the text color to the text

    ScoreMessageText = TextSprite("Your final score is " + str(Score), "Comic sans", 25)
    ScoreMessageText.SetPosition(-150, -150) # Set this sprite off screen
    ScoreMessageText.SetColor((0, 0, 0))
    ScoreMessageText.UpdateText("Your final score is " + str(Score))

    RestartText = TextSprite("Click pygame's exit button to quit. Or, wait 5 seconds the restart", "Comic sans", 15)
    RestartText.SetPosition(-40, -40) # Make this sprite go off screen
    RestartText.SetColor((0, 0, 0))
    RestartText.UpdateText("Click pygame's exit button to quit. Or, wait 5 seconds the restart")

    # --- Other Sprites ---
    TopBoundary = UpperBlock(Window.GetWidth(), 50)
    TopBoundary.SetColor((0, 0, 0))

    Paddle = PaddleSprite(100, 10)
    # Place the paddle at the center of the screen
    Paddle.SetPosition(Window.GetWidth()/2 - Paddle.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 30)

    Ball = BallSprite(20, 20, 4.5)
    PaddleStartPos = Paddle.GetPosition()
    Ball.SetBallAtPaddle(PaddleStartPos, Paddle.GetWidth()) # Place the ball at the center of the paddle

    # --- Brick variables ---
    NumRows = 6
    NumColumns = 6
    BrickWidth = 50
    BrickHeight = 35
    MoveBricksDown = False # Brick does not need to be moved down at the start of the game
    Counter = (NumRows - 1)*(10 + BrickHeight) + 80 # Value to store how much pixels the bricks need to be moved down

    # Aggregation is utilized here where we create a list that stores individual objects
    BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, True)

    # List to store all the power up objects, which also uses aggregation
    PowerUpList = []

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
        if StartGame is False: # Wait until the player pressed the space bar to start the game
            if PRESSED_KEYS[pygame.K_SPACE]:
                StartGame = True
        else: # Game has started
            Paddle.LeftRightMove(PRESSED_KEYS) # Allow the paddle to move left and right
            Paddle.CheckBoundaries(Window.GetWidth(), Window.GetHeight())

            if CanShootBall is True: # Check if the ball needs to be launched at the paddle
                Ball.SetBallAtPaddle(Paddle.GetPosition(), Paddle.GetWidth())
                if PRESSED_KEYS[pygame.K_UP] == 1 or PRESSED_KEYS[pygame.K_w] == 1: # Ball will be launched when up arrow key or "W" is pressed
                    Paddle.LaunchBall(PRESSED_KEYS, Ball)
                    CanShootBall = False # Set it to False so player can no longer shoot the ball after it is launched
            else: # Move the ball after it has been launched
                Ball.Move(Ball.GetPosition())

            Ball.CheckBoundaries(Window.GetWidth(), Window.GetHeight(), 0, TopBoundary.GetHeight())

            if MoveBricksDown is True: # Check if the brick needs to be move down if it has not reached final position
                for brick in BricksList: # Move each brick down
                    brick.MoveDown(brick.GetPosition(), 4)
                Counter -= 4 # Decrease Counter so we know how much the bricks still needs to move down by
                if Counter <= 0: # Brick has reached their final positions
                    MoveBricksDown = False

            for brick in BricksList:
                if Ball.isCollision(brick.GetWidth(), brick.GetHeight(), brick.GetPosition()) is True:
                    brick.LoseHealth() # Make the brick lose health after the ball hits it
                    Score += 1
                    if brick.GetHealth() <= 0: # Brick has been destroyed
                        if brick.GetType() == "PowerUp": # Check if the brick gives power ups
                            
                            # Decide what type of power up to give
                            if DecidePowerUpType() == "Longer Paddle":
                                PowerUp = PaddleLengthPowerUp("Longer Paddle", 20, 20, 4) # The power up increases paddle's length
                                PowerUp.UpdateColor("Longer Paddle") # Change color to green
                            else:
                                PowerUp = PaddleLengthPowerUp("Shorter Paddle", 110, 20, 4)
                                PowerUp.UpdateColor("Shorter Paddle") # Change color to purple
                            
                            PowerUp.SetPowerUpAtBrick(brick.GetPosition(), brick.GetWidth(), brick.GetHeight()) # Create power up at where the brick was destroyed
                            PowerUpList.append(PowerUp)

                        BricksList.remove(brick) # Remove the brick from the list to indicate it is gone from the game
                    else:
                        brick.SetColor(BrickColors[brick.GetHealth()]) # Change brick's color if it has still has health left
            
            if len(PowerUpList) > 0:
                for powerup in PowerUpList: # Move each power ups down
                    powerup.MoveDown(powerup.GetPosition(), powerup.GetSpeed())
                    if powerup.CheckBoundaries(Window.GetHeight()) is True: # Remove the power up from the game after it hits the bottom of the screen
                        PowerUpList.remove(powerup)
            
            if len(BricksList) == 0: # All the bricks in the level has been destroyed
                Level += 1
                Ball.SetSpeed(Ball.GetSpeed() + 0.2) # Speed up the ball
                BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, False) # Create new bricks outside the screen
                MoveBricksDown = True
                Counter = (NumRows - 1)*(10 + BrickHeight) + 80 # Calculate how much the bricks need to move down by

            if Paddle.isCollision(Ball.GetWidth(), Ball.GetHeight(), Ball.GetPosition()): # Check if paddle and ball collided
                BallPosition = Ball.GetPosition()
                BallX = BallPosition[0]
                
                PaddlePosition = Paddle.GetPosition()
                PaddleX = PaddlePosition[0]

                if BallX >= PaddleX and BallX + Ball.GetWidth() <= PaddleX + Paddle.GetWidth(): # Both the ball's bottom vertices hit the paddle's top surface
                    Ball.ChangeDirY(Ball.GetDirY()*-1)
                else:
                    # The ball was going down diagonally-right and hit the right side of the top surface
                    if BallX >= PaddleX and BallX + Ball.GetWidth() > PaddleX + Paddle.GetWidth() and Ball.GetDirX() == 1:
                        Ball.ChangeDirY(Ball.GetDirY() * -1)

                    # The ball was going down diagonally left and hit the left side of the top surface
                    elif BallX + Ball.GetWidth() <= PaddleX + Paddle.GetWidth() and BallX < PaddleX and Ball.GetDirX() == -1:
                        Ball.ChangeDirY(Ball.GetDirY() * -1)

                    # This means that the ball hit the left or right side of the paddle, and not the top surface, so make the ball bounce back from where it came from
                    else:
                        Ball.ChangeDirY(Ball.GetDirY()*-1)
                        Ball.ChangeDirX(Ball.GetDirX()*-1)

                # Move the ball until it no longer collides with the paddle
                while Paddle.isCollision(Ball.GetWidth(), Ball.GetHeight(), Ball.GetPosition()):
                    Ball.Move(Ball.GetPosition())
            
            for powerup in PowerUpList:
                if Paddle.isCollision(powerup.GetWidth(), powerup.GetHeight(), powerup.GetPosition()): # Paddle hit a power up
                    PaddleWidthState = Paddle.GetWidthState()

                    if powerup.GetPowerUpType() == "Longer Paddle":
                        if PaddleWidthState + 1 <= 2: # Only make the paddle longer if it hasn't reached its maximum length yet

                            PaddleWidthState += 1
                            Paddle.UpdateWidthState(PaddleWidthState)
                            NewPaddleWidth = PaddleWidths[PaddleWidthState] # Get the new longer width the paddle should change into
                            Paddle.ChangePaddleWidth(NewPaddleWidth) # Increase paddle's width
                        else: # Paddle reached maximum length
                            Score += 5
                        PowerUpList.remove(powerup)
                    else: # Make the paddle shorter
                        if PaddleWidthState - 1 >= -2: # Paddle can still be shortened
                            PaddleWidthState -= 1
                            Paddle.UpdateWidthState(PaddleWidthState)
                            NewPaddleWidth = PaddleWidths[PaddleWidthState] # Get the new shorter width the paddle should change to
                            Paddle.ChangePaddleWidth(NewPaddleWidth) # Make the paddle shorter
                        else: # Paddle reached minimum length
                            Score -= 20

                        PowerUpList.remove(powerup) # Remove power up or power down from the game

            if Ball.HitBottomEdge(Window.GetHeight()) is True: # Check if the ball has hit the bottom edge
                Lives -= 1
                if Lives <= 0: # The game is over
                    GameOngoing = False
                else: # Allow the player to reshoot the ball
                    Ball.SetBallAtPaddle(Paddle.GetPosition(), Paddle.GetWidth())
                    CanShootBall = True

            # --- Update text sprites here ---
            ScoreText.UpdateText("Score: " + str(Score))

            LevelText.UpdateText("Level: " + str(Level))
            LevelText.SetPosition(Window.GetWidth() - LevelText.GetWidth() - 10, 0)

            LivesText.UpdateText("Lives: " + str(Lives))
            LivesText.SetPosition(Window.GetWidth() - LivesText.GetWidth() - 10, LevelText.GetHeight())

            ScoreMessageText.UpdateText("Your final score is " + str(Score)) # Update this text so it is ready to be displayed when the game ends

        # --- OUTPUTS ---
        Window.ClearScreen()

        if StartGame is False: # Game has not started yet
            Window.GetSurface().blit(StartText.GetSurface(), StartText.GetPosition()) # Display message for user to press space bar

        if len(PowerUpList) > 0: # Check if there are any power ups created
            for powerup in PowerUpList: # Display each power up
                Window.GetSurface().blit(powerup.GetSurface(), powerup.GetPosition())

        for brick in BricksList: # Display all the bricks
            Window.GetSurface().blit(brick.GetSurface(), brick.GetPosition())

        Window.GetSurface().blit(Paddle.GetSurface(), Paddle.GetPosition())
        Window.GetSurface().blit(Ball.GetSurface(), Ball.GetPosition())

        Window.GetSurface().blit(TopBoundary.GetSurface(), TopBoundary.GetPosition())

        # Display the text sprites
        Window.GetSurface().blit(TitleText.GetSurface(), TitleText.GetPosition())
        Window.GetSurface().blit(ScoreText.GetSurface(), ScoreText.GetPosition())
        Window.GetSurface().blit(LevelText.GetSurface(), LevelText.GetPosition())
        Window.GetSurface().blit(LivesText.GetSurface(), LivesText.GetPosition())

        # Make this if-statement at the end so the game-over texts can be placed on top of everything
        if GameOngoing is False: # The player has ran out of lives

            # Display the game over text sprites
            GameOverText.SetPosition(Window.GetWidth()/2 - GameOverText.GetWidth()/2, Window.GetHeight()/2 - GameOverText.GetHeight()/2 - 50)
            ScoreMessageText.SetPosition(Window.GetWidth()/2 - ScoreMessageText.GetWidth()/2, Window.GetHeight()/2 - ScoreMessageText.GetHeight()/2)
            RestartText.SetPosition(Window.GetWidth()/2 - RestartText.GetWidth()/2, Window.GetHeight()/2 - RestartText.GetHeight()/2 + 50)

            Window.GetSurface().blit(GameOverText.GetSurface(), GameOverText.GetPosition())
            Window.GetSurface().blit(ScoreMessageText.GetSurface(), ScoreMessageText.GetPosition())
            Window.GetSurface().blit(RestartText.GetSurface(), RestartText.GetPosition())

            Window.UpdateFrame() # Show the messages above

            # This allows the user to close the pygame window during the five second wait time
            StartTime = time.time()
            while time.time() - StartTime < 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

            break # This ends the main loop

        Window.UpdateFrame()
    
    Main() # Use recursion to call the Main() function which restarts the whole game

if __name__ == "__main__":
    Main() # Run the function where the main program code is held in

