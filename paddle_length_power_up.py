import pygame
from my_sprite import mySprite

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

