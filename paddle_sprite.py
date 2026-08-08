import pygame
from my_sprite import mySprite

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
    
