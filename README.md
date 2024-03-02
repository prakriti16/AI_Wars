The aim was to develop a heuristic for a bot that can play the game capture the boxes. 
Details on how to run the game are given in the .pdf file.
The heuristic function we developed takes the parameters number of vertices (N) and list of captured edges(edges).
Then it creates a 2 dimensional array and marks all the played edges.
We use the double cross strategy to decide which edge to play.
In the double cross strategy we capture all but 2 boxes.
This forces the opponent to open the next set of boxes for us to capture.
