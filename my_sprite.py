import pygame

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