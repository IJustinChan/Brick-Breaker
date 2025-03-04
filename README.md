# CSE-3130-OOP2-Project

## Game Overview and Rules
This program remakes the game Brick Breaker. The goal of this game is score as many points as possible.
To score points, the player needs to control a paddle to bounce the ball into bricks. Each time a brick is
hit, the score increases by one. However, the player also needs to prevent the ball from touching the bottom
of the screen as this would result in the player a life. The player has three lives so if the ball touches
the bottom three times, the game ends.

To complete a level, the player must successfully destroy all the bricks in that level. Once a level is completed, 
new bricks will come down, indicating the start of a new level. This game has no end, meaning the game will
continue as long as the player has lives remaining. However, the ball will speed up after each level has been
completed.

The paddle can be controlled using the left and right arrow keys, as well as the keys "A" and "D".
Pressing the left arrow key or "A" moves the paddle left while pressing the right arrow key or "D" moves the paddle right.

At the start of the game, and after the player loses a life, the player can "launch" the ball from their 
paddle, which means the ball will move up from wherever the paddle is. To "launch" the ball, press either 
the "W" key or up arrow key. The ball will go towards the left if the left movement key is held. Otherwise, it will
go towards the right, regardless if the right movement is held or not.

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
    * White bricks' health is one, yellow bricks' health is two, orange bricks' health is three, and red bricks' health is four. 
    The bricks will change color when they are hit and the bricks will be destroyed once they have been hit by the ball enough times.
    * Some bricks have a color of cyan, which has a health of one. These bricks are power up bricks,
    which means that power ups will drop down from the brick after it has been destroyed.

2. Power ups (and power downs). After destroying cyan bricks, power ups will drop down from where
the cyan bricks were destroyed. These power ups will either increase the length of the paddle or they
will decrease the length of the paddle (hence, power downs). There is a 25% chance to get a power up
that increases the paddle's length and a 75% chance to get a power down that decreases the paddle's
length. Once the paddle's length changes, it will remain at that length until the player collects a
power up or a power down.
    * A green sprite falling down from where the cyan brick was destroyed is a power up, meaning if
    the paddle collides with the green sprite, the paddle's length will increase. However, there is a
    maximum length the paddle can reach, which means that collecting more green sprites will
    eventually not change the length of the paddle. Instead, the player will get five points.
    * A purple sprite falling down from the cyan brick is a power down. If the paddle touches this
    purple sprite, the paddle's length will decrease. Similar to green sprites (power ups), there is a 
    minimum length the paddle can reach, so the player will lose 10 points after they keep 
    colliding with the purple sprites.
    * Note: The paddle's length can only be changed by collecting these power ups and power downs. 
    This means that it is possible for the paddle to shift between long and short as the player collect these 
    power ups and power downs. However, power downs will result in a shorter paddle, which makes it harder for 
    the player to bounce the ball back up. Thus, it is in the player's best interest to avoid collecting power 
    downs and to instead collect power ups so it is easier to bounce the ball back up. Also, the 
    power downs are larger than power ups, so they will need to be avoided more carefully.

3. The player has three lives. If the player loses a life, they will have the option to "launch"
the ball from their paddle. Once the player loses all three of their lives, the game will end. The
ball will also speed up as the level increases.


## Planning Components
UML Tables:

![UML Tables](Images/Brick%20Breaker%20UML%20Tables.drawio.png)

Flowchart:

![Flowchart](Images/Brick%20Breaker%20Flowchart.drawio.png)

## How To Run The Program
Ensure that pygame is installed. Then, run the file _main.py_. A pygame window should appear and the player 
can press the space bar to begin playing the game.

## Reflection

One of the biggest challenges I encountered was handling the collision between the ball and the paddle.
Initially, the collision I made for the ball and paddle worked fine until the ball hits the left and
right edge of the paddle. This resulted in numerous bugs such as the ball getting stuck inside
the paddle, preventing the ball from bouncing away. I first tried to fix this issue by using a while-loop 
to make the ball move away from the paddle before the game continues, but this resulted in the ball temporarily 
speeding up, making the collision look weird and unnatural. To solve this problem, I had to make the ball 
directly bounce along the path it came from. This led to the new game physics where if the paddle hits the ball 
using its left or right sides, the ball bounces away following the path it came from. Creating this new
collision physics solved the problem of the ball getting stuck into the paddle when it hits the sides.
At the same time, it makes the game more dynamic as the player will have more control of where the ball
bounces, so I was able to indirectly improve the game in two ways using this solution.

One of my extra feature was making the bricks have different health, requiring the ball to hit some bricks
multiple times to destroy them. I decided to make the bricks have a health of up to four, which occurs
on Level 3. After Level 3, the bricks' health will stop increasing as I realize that the game will begin feeling
monotonous if it takes a long to destroy the bricks. Thus, I decided a maximum brick health of four is reasonable. 
Additionally, I also made it so the bricks will have a certain color depending on their health. This allows the 
user to know how many times they have to hit a certain brick to destroy it. I also chose intuitive colors for the 
bricks such as red, orange, yellow and white so the user can quickly figure out which bricks have more health.
This decision taught me the importance of taking the perspective of the user when designing my program
as I want my game to be as intuitive to understand as possible.

A small feature I have in my program is allowing the user to wait five seconds to restart the game after
they lose all three of their lives. I originally had difficulties making this feature as I would have to
reset several variables and objects. However, I found a solution involving recursion, where I placed all of my code
inside a function called Main(). The while-loop inside Main() is stopped after the user finishes waiting five
seconds, and this function then calls itself, which resets everything. While this solution works, I probably
should have created a class called "Game" that controls everything. This would make it easier to reset the game 
and it makes all the other classes and objects easier to control. It also makes the code more organized.
In the future, I will try planning more aspects of my code out at the beginning to prevent my code from
being more complicated later on.





