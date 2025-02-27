# CSE-3130-OOP2-Project

## Game Overview and Rules
This program remakes the game Brick Breaker. The goal of this game is score as many points as possible.
To score points, the player needs to control a paddle to bounce the ball into bricks. Each time a brick is
hit, the score increases by one. However, the player also needs to prevent the ball from touching the bottom
of the screen as this would result in the player a life. The player has three lives so if the ball touches
the bottom three times, the game ends.

To complete a level, the player must successfully destroy all the bricks in that level. Once a level is completed, 
new bricks will come down, indicating the start of a new level. This game has no end, meaning the game will
continue as long as the player has lives remaining. 

The paddle can be controlled using the left and right arrow keys, as well as the keys "A" and "D".
Pressing the left arrow key or "A" moves the paddle left while pressing the right arrow key or "D" moves the paddle right.

At the start of the game, and after the player loses a life, the player can "launch" the ball from their 
paddle, which means the ball will move up from wherever the paddle is. To "launch" the ball, press either 
the "W" key or up arrow key. The ball will go towards the left if the left movement key is held otherwise it will
go towards the right, regardless if the right movement is held.

One final note about the paddle: If the ball is coming in from the left side, and it hits exactly the left side
of the paddle, it will bounce back along its path. Similarly, if the ball is coming in from the right side, and
it hits the right side of the paddle, it will bounce along the path it took. Otherwise, the ball will bounce
normally as expected. The reason this occurs is because this makes the game physics more interesting, and it
prevents the ball from getting "stuck" into paddle when it hits the paddle from the side. 

## Extra Features
Here are the main extra features in this game:
1. Bricks have their own individual health. This means that it may take multiple hits from the
ball to destroy certain bricks. As the level increases, the health of the brick increases. On
Level 1, the bricks have a health of up to two. On Level 2, the maximum health of the bricks is
three. On Level 3, the maximum health of the bricks is four. Afterwards, the bricks will continue
to have a maximum health of four, even as the levels increase. 
* White bricks' health is one, yellow bricks' health is two, orange bricks' health is three, and red
bricks' health is four. The bricks will change color when they are hit and the bricks will be
destroyed once they have been hit by the ball enough times.

2. 

## Planning Components

## How To Run The Program
Run the file _main.py_. A pygame window should appear and the player can begin the game.

## Reflection

Include this: On level three, the bricks will have a health up to four. Afterwards, the brick's health will not increase as I think it makes
the game feel too monotonous if it begins taking a long time to destroy bricks.
