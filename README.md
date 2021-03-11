# dobbelBot
Discord drinking game bot, own creation

This bot is fully in Dutch, so if you dont't understand it, I'm sorry. The game is pretty simple, and only has a few rules:

## Starting the game ##
All participants can join the game using the '$join' command. 
When all players are ready, someone can start the game using the '$start' command.

## Game flow ##

When the game is started, a random first player is selected. The order of the players will remain the same during the game. 
This first player can now throw 3 dices using the '$gooi'command. The game will now ask if he wants to throw again (confirm with 'j' / 'n'). 
If he finds this score sufficient (= hard to beat), and doesn't throw again, the other players now need to improve his score to win this round (in maximum the same amount of tries). You can use a maximum amount of 3 tries to set a score!!


## The end of a round ##
The player with the highest score at the end of the round wins this round, and can start in the next round! The one with the lowest score needs to drink up as well!
If there is a tie game, the players with the equal highscore need to throw just one dice. The game will determine which player can start (can be random), and the player with the highest throw wins the entire round. The 100 and 60 score are not involved here, just the regular numbers that is displayed on the dice counts.


## Scores ##
The scores are determinded pretty easily:
---------------
|Dice | Score |
|-------------|
|  1  |  100  |
|  2  |   2   |
|  3  |   3   |
|  4  |   4   |
|  5  |   5   |
|  6  |  60   |
---------------

Score ranking:
Zand van 1   (1,1,1)
Soixant-neuf (4,5,6)
Zand van 2   (2,2,2)
Zand van 3   (3,3,3)
Zand van 4   (4,4,4)
Zand van 5   (5,5,5)
Zand van 6   (6,6,6)
260          (1,1,6)
220          (1,6,6)
...
7            (2,2,3) Bottoms up, this is the lowest score you can throw! You can not throw again.


## Stopping the game ##
You can stop the game at any time, since it will continue to run automatically. The game is stopped by entering the '$stop' command. The game will stop after completing the round.
