import pygame

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
