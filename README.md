lmk if u find bugs

Ait lemme explain this shit

The objective of the game is to destroy your opponent's bot first<br>
Bots will get destroyed if:

- a projectile hits them
- rammed by another bot (driven into)

The map is a grid defined by a continuous array of cells<br>
Your task is to make an 'AI'<br>
You do this by inheriting the Bot class and overriding the 'next_action' method (i recc you make it a diff file and import this for ease of use)

You receive as arguments:

- the grid state
- the bots directions ( dict[ botname, direction ] )
  The method should return the next action your bot will perform
  TIP:
  You are free to override **init**, remember to initialize super class aswell (https://www.w3schools.com/python/python_inheritance.asp#:~:text=Use%20the%20super()%20Function)

check the example bots for an idea
