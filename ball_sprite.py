import pygame
from my_sprite import mySprite

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


