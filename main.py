"""
name: Brick Breaker
author: Justin Chan
date: 2025-02-06
"""

import pygame
import random
import time

from ball_sprite import BallSprite
from paddle_sprite import PaddleSprite
from brick import Brick
from text_sprite import TextSprite
from upper_block import UpperBlock
from paddle_length_power_up import PaddleLengthPowerUp
from window import WINDOW

pygame.init()


# --- HELPER FUNCTIONS ---
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
    BricksArr = []

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
            Health = random.randint(1, MaxHealth)

            BrickType = "Regular"
            if Health == 1: # Only bricks with a health of one can give power ups or multiball bricks
                MultiballChance = random.randint(1, 5)
                if MultiballChance == 1:
                    BrickType = "MultiBall"
                elif CalculatePowerUpChance() is True:
                    BrickType = "PowerUp"

            XPOS = (PaddingX + WIDTH)*j + 60

            # This checks if we are creating the bricks inside the screen or outside the screen
            # When the user starts playing the game, the bricks will initially be created inside the screen.
            # After a level ends, bricks will be created outside the screen so they can move down.
            if INSIDE_SCREEN is True:
                YPOS = (PaddingY + HEIGHT)*i + 80
            else:
                YPOS = (PaddingY + HEIGHT)*i - MaxY

            # Aggregation is implemented here as the brick objects are being placed into the same list
            BricksArr.append(Brick(Health, WIDTH, HEIGHT, XPOS, YPOS, BrickType))

            if BrickType == "Regular": # Change the color of the brick depending on its health if it is a regular brick
                BricksArr[-1].SetColor(COLORS[Health])
            elif BrickType == "PowerUp": # Power up bricks are cyan
                BricksArr[-1].SetColor((63, 181, 191))
            else: # Multi-ball bricks are brown
                BricksArr[-1].SetColor((150, 75, 0))

    return BricksArr

def SpawnNewBall(BALL):
    """
    Create a new ball when a brown multiball brick is destroyed.
    The new ball is created at the same position as the current ball and travels in the opposite x direction.
    :param BALL: obj
    :return: obj
    """
    NewBall = BallSprite(BALL.GetWidth(), BALL.GetHeight(), BALL.GetSpeed())
    NewBall.SetPosition(*BALL.GetPosition())
    NewBall.ChangeDirX(-BALL.GetDirX())
    NewBall.ChangeDirY(BALL.GetDirY())
    return NewBall

def CalculatePowerUpChance():
    """
    Decide if a brick with a health of one is a power up brick or not
    :return: bool
    """
    Chance = random.randint(1, 5)
    if Chance <= 3: # 60% chance that brick is a power up brick
        return True
    else:
        return False

def DecidePowerUpType():
    """
    Decide if a power up or power down will be created after a power up brick is destroyed
    :return: str
    """
    LongerPaddleChance = random.randint(1, 4)
    if LongerPaddleChance == 1: # 25% chance it is a power up that makes the paddle longer
        return "Longer Paddle"
    else:
        return "Shorter Paddle"


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
        -2: 25,
        1 : 125, # Power up increases its width first time
        2: 150
    }

    # --- Variables ---
    Score = 0
    Level = 1
    Lives = 3
    GameOngoing = True

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
    GameOverText.UpdateText("Game Over!")

    ScoreMessageText = TextSprite("Your final score is " + str(Score), "Comic sans", 25)
    ScoreMessageText.SetPosition(-150, -150)
    ScoreMessageText.SetColor((0, 0, 0))
    ScoreMessageText.UpdateText("Your final score is " + str(Score))

    RestartText = TextSprite("Click pygame's exit button to quit. Or, wait 5 seconds to restart", "Comic sans", 15)
    RestartText.SetPosition(-40, -40) # Make this sprite go off screen
    RestartText.SetColor((0, 0, 0))
    RestartText.UpdateText("Click pygame's exit button to quit. Or, wait 5 seconds to restart")

    # --- Other Sprites ---
    TopBoundary = UpperBlock(Window.GetWidth(), 50)
    TopBoundary.SetColor((0, 0, 0))

    Paddle = PaddleSprite(100, 10)
    Paddle.SetPosition(Window.GetWidth()/2 - Paddle.GetWidth()/2, Window.GetHeight() - Paddle.GetHeight() - 30)

    Ball = BallSprite(20, 20, 4.5)
    PaddleStartPos = Paddle.GetPosition()
    Ball.SetBallAtPaddle(PaddleStartPos, Paddle.GetWidth()) # Place the ball at the center of the paddle
    BallsList = [Ball] # Track all active balls

    # --- Brick variables ---
    NumRows = 6
    NumColumns = 6
    BrickWidth = 50
    BrickHeight = 35
    MoveBricksDown = False # Brick does not need to be moved down at the start of the game
    Counter = (NumRows - 1)*(10 + BrickHeight) + 80 # Value to store how much pixels the bricks need to be moved down

    # Aggregation is utilized here where we create a list that stores individual objects
    BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, True)

    PowerUpList = []

    StartGame = False # Game only starts once the player presses the space bar
    CanShootBall = True

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
            Paddle.LeftRightMove(PRESSED_KEYS)
            Paddle.CheckBoundaries(Window.GetWidth(), Window.GetHeight())

            if CanShootBall is True:
                BallsList[0].SetBallAtPaddle(Paddle.GetPosition(), Paddle.GetWidth())
                if PRESSED_KEYS[pygame.K_UP] == 1 or PRESSED_KEYS[pygame.K_w] == 1:
                    Paddle.LaunchBall(PRESSED_KEYS, BallsList[0])
                    CanShootBall = False # Set it to False so player can no longer shoot the ball after it is launched
            else:
                for ball in BallsList:
                    ball.Move(ball.GetPosition())

            for ball in BallsList:
                ball.CheckBoundaries(Window.GetWidth(), Window.GetHeight(), 0, TopBoundary.GetHeight())

            if MoveBricksDown is True: # Check if the brick needs to be move down if it has not reached final position
                for brick in BricksList:
                    brick.MoveDown(brick.GetPosition(), 4)
                Counter -= 4 # Decrease Counter so we know how much the bricks still needs to move down by
                if Counter <= 0:
                    MoveBricksDown = False

            for ball in list(BallsList):
                for brick in list(BricksList):
                    if ball.isCollision(brick.GetWidth(), brick.GetHeight(), brick.GetPosition()) is True:
                        brick.LoseHealth()
                        Score += 1
                        if brick.GetHealth() <= 0:
                            if brick.GetType() == "PowerUp":
                                # Decide what type of power up to give
                                if DecidePowerUpType() == "Longer Paddle":
                                    PowerUp = PaddleLengthPowerUp("Longer Paddle", 20, 20, 4) # The power up increases paddle's length
                                    PowerUp.UpdateColor("Longer Paddle")
                                else:
                                    PowerUp = PaddleLengthPowerUp("Shorter Paddle", 110, 20, 4)
                                    PowerUp.UpdateColor("Shorter Paddle")
                                PowerUp.SetPowerUpAtBrick(brick.GetPosition(), brick.GetWidth(), brick.GetHeight()) # Create power up at where the brick was destroyed
                                PowerUpList.append(PowerUp)
                            elif brick.GetType() == "MultiBall":
                                BallsList.append(SpawnNewBall(ball)) # Create another ball when brown brick is destroyed

                            BricksList.remove(brick) # Remove the brick from the list to indicate it is gone from the game
                            break
                        else:
                            brick.SetColor(BrickColors[brick.GetHealth()]) # Change brick's color if it has still has health left
            
            if len(PowerUpList) > 0:
                for powerup in PowerUpList:
                    powerup.MoveDown(powerup.GetPosition(), powerup.GetSpeed())
                    if powerup.CheckBoundaries(Window.GetHeight()) is True:
                        PowerUpList.remove(powerup)
            
            if len(BricksList) == 0: # All the bricks in the level has been destroyed
                Level += 1
                for ball in BallsList:
                    ball.SetSpeed(ball.GetSpeed() + 0.2) # Speed up every active ball
                BricksList = CreateBricks(NumRows, NumColumns, Level, BrickWidth, BrickHeight, BrickColors, False) # Create new bricks outside the screen
                MoveBricksDown = True
                Counter = (NumRows - 1)*(10 + BrickHeight) + 80 # Calculate how much the bricks need to move down by

            for ball in list(BallsList):
                if Paddle.isCollision(ball.GetWidth(), ball.GetHeight(), ball.GetPosition()):
                    BallPosition = ball.GetPosition()
                    BallX = BallPosition[0]
                    
                    PaddlePosition = Paddle.GetPosition()
                    PaddleX = PaddlePosition[0]

                    if BallX >= PaddleX and BallX + ball.GetWidth() <= PaddleX + Paddle.GetWidth(): # Both the ball's bottom vertices hit the paddle's top surface
                        ball.ChangeDirY(ball.GetDirY()*-1)
                    else:
                        # The ball was going down diagonally-right and hit the right side of the top surface
                        if BallX >= PaddleX and BallX + ball.GetWidth() > PaddleX + Paddle.GetWidth() and ball.GetDirX() == 1:
                            ball.ChangeDirY(ball.GetDirY() * -1)

                        # The ball was going down diagonally left and hit the left side of the top surface
                        elif BallX + ball.GetWidth() <= PaddleX + Paddle.GetWidth() and BallX < PaddleX and ball.GetDirX() == -1:
                            ball.ChangeDirY(ball.GetDirY() * -1)

                        # This means that the ball hit the left or right side of the paddle, and not the top surface, so make the ball bounce back from where it came from
                        else:
                            ball.ChangeDirY(ball.GetDirY()*-1)
                            ball.ChangeDirX(ball.GetDirX()*-1)

                    # Move the ball until it no longer collides with the paddle
                    while Paddle.isCollision(ball.GetWidth(), ball.GetHeight(), ball.GetPosition()):
                        ball.Move(ball.GetPosition())
            
            for powerup in PowerUpList:
                if Paddle.isCollision(powerup.GetWidth(), powerup.GetHeight(), powerup.GetPosition()):
                    PaddleWidthState = Paddle.GetWidthState()

                    if powerup.GetPowerUpType() == "Longer Paddle":
                        if PaddleWidthState + 1 <= 2: # Only make the paddle longer if it hasn't reached its maximum length yet

                            PaddleWidthState += 1
                            Paddle.UpdateWidthState(PaddleWidthState)
                            NewPaddleWidth = PaddleWidths[PaddleWidthState]
                            Paddle.ChangePaddleWidth(NewPaddleWidth)
                        else: # Paddle reached maximum length
                            Score += 5
                        PowerUpList.remove(powerup)
                    else:
                        if PaddleWidthState - 1 >= -2: # Paddle can still be shortened
                            PaddleWidthState -= 1
                            Paddle.UpdateWidthState(PaddleWidthState)
                            NewPaddleWidth = PaddleWidths[PaddleWidthState]
                            Paddle.ChangePaddleWidth(NewPaddleWidth)
                        else: # Paddle reached minimum length
                            Score -= 20

                        PowerUpList.remove(powerup)

            for ball in list(BallsList):
                if ball.HitBottomEdge(Window.GetHeight()) is True: # Check if the ball has hit the bottom edge
                    BallsList.remove(ball)

            if len(BallsList) == 0:
                Lives -= 1
                if Lives <= 0: # The game is over
                    GameOngoing = False
                else: # Allow the player to reshoot the ball
                    Ball = BallSprite(20, 20, 4.5)
                    Ball.SetBallAtPaddle(Paddle.GetPosition(), Paddle.GetWidth())
                    BallsList = [Ball]
                    CanShootBall = True

            # --- Update text sprites here ---
            ScoreText.UpdateText("Score: " + str(Score))

            LevelText.UpdateText("Level: " + str(Level))
            LevelText.SetPosition(Window.GetWidth() - LevelText.GetWidth() - 10, 0)

            LivesText.UpdateText("Lives: " + str(Lives))
            LivesText.SetPosition(Window.GetWidth() - LivesText.GetWidth() - 10, LevelText.GetHeight())

            ScoreMessageText.UpdateText("Your final score is " + str(Score))

        # --- OUTPUTS ---
        Window.ClearScreen()

        if StartGame is False: # Game has not started yet
            Window.GetSurface().blit(StartText.GetSurface(), StartText.GetPosition()) # Display message for user to press space bar

        if len(PowerUpList) > 0: # Check if there are any power ups created
            for powerup in PowerUpList:
                Window.GetSurface().blit(powerup.GetSurface(), powerup.GetPosition())

        for brick in BricksList:
            Window.GetSurface().blit(brick.GetSurface(), brick.GetPosition())

        Window.GetSurface().blit(Paddle.GetSurface(), Paddle.GetPosition())
        for ball in BallsList:
            Window.GetSurface().blit(ball.GetSurface(), ball.GetPosition())

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

            Window.UpdateFrame()

            # This allows the user to close the pygame window during the five second wait time
            StartTime = time.time()
            while time.time() - StartTime < 5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

            break

        Window.UpdateFrame()
    
    Main() # Use recursion to call the Main() function which restarts the whole game

if __name__ == "__main__":
    Main()

