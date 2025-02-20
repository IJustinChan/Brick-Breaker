# CSE-3130-OOP2-Project

## Game Overview and Rules
This program remakes the game Brick Breaker. The goal of this game is score as many points as possible.
To score points, the player needs to control a paddle to bounce the ball into bricks. Each time a brick is
hit, the score increases by one. However, the player also needs to prevent the ball from touching the bottom
of the screen as this would result in the player losing since the ball "fell down". 

To complete a level, the player must successfully destroy all the bricks in that level. Once a level is completed, 
new bricks will come down, indicating the start of a new level. This game has no end, meaning the game will
continue as long as the ball has not touched the bottom of the screen. This also means that the player only
has one life, so the game is over as soon as the player fails to bounce the ball up with the paddle.

The paddle can be controlled using the left and right arrow keys, as well as the keys "A" and "D".
Pressing the left arrow key or "A" moves the paddle left while pressing the right arrow key or "D" moves the paddle right.

One final note about the paddle: If the ball is coming in from the left side, and it hits exactly the left side
of the paddle, it will bounce back along its path. Similarly, if the ball is coming in from the right side, and
it hits the right side of the paddle, it will bounce along the path it took. Otherwise, the ball will bounce
normally as expected. The reason this occurs is because this makes the game physics more interesting. and it
prevents the ball from getting "stuck" into paddle when it hits the paddle from the side. 

## Extra Features
Here are the main extra features in this game:
1. The bricks get harder to destroy as each level increases. This means that each brick has a health associated
with them. Thus, it may take multiple hits from the ball to destroy one brick. As the level increases, bricks with more health
will spawn. On level one, bricks either have a health of one or two. On level two, the bricks will have a health up to three.
On level three, the bricks will have a health up to four. Afterwards, the brick's health will not increase as I think it makes
the game feel too monotonous if it begins taking a long time to destroy bricks.

2. 

## Planning Components

## How To Run The Program
Run the file _main.py_. A pygame window should appear and the player can begin the game.

## Reflection

