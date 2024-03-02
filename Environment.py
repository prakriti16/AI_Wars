import os
import time
import signal
import player_1
import player_2
import player_3
import multiprocessing
from functools import partial
from typing import List, Tuple
from termcolor import colored


PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_3 = 3

class Environment:
   
    def __init__(self, n : int) -> None:
        '''
            Environemnt class for Conquer the Battlefield!!
        
            N: int -> Number of dots horizontally or vertically
            player_1: List[Tuple] -> ALl edges occupied by Player 1
            player_2: List[Tuple] -> ALl edges occupied by Player 2
            max_steps: int -> Number of moves (valid / invalid) for entire game
            player_1_score: int -> One point per edge and 5 points per sqaure 
            player_2_score: int -> One point per edge and 5 points per sqaure 
        
        '''
        self.N: int = n
        self.player_1: List[Tuple] = []
        self.player_2: List[Tuple] = []
        self.player_3: List[Tuple] = []
        self.max_steps: int = 2*self.N*(self.N - 1)*1000
        self.max_edges: int = 2*self.N*(self.N - 1)
        self.player_1_score: int = 0
        self.player_2_score: int = 0
        self.player_3_score: int = 0
        self.mat = [['+' if i%2==0 else ' ' for i in range(2*self.N-1)] if j%2==0 else [' ' for _ in range(2*self.N-1)] for j in range(2*self.N-1)]
    
    def run_with_timeout(self, func, args, timeout_seconds) -> Tuple:
        '''
            A function that runs a given function until timeout is reached
            It may raise an exception or return a tuple
        '''
        result = func(*args)
        if not result:
            raise TimeoutError("Move time exceeded 1 second")
        
        return self.adjust_edge_name(result)
    
    def end_game(self, tick: int):
        '''
            Returns True if game ends
                - Max number of moves are done
                - All edges are filled
        '''
        return tick >= self.max_steps or len(self.player_1) + len(self.player_2) + len(self.player_3) >= self.max_edges
    
    def start(self) -> None:
        '''
            Main function that communicates with player functions and updates
            the moves.
        '''
        tick = 0
        while not self.end_game(tick):
            
            # First player
            while not self.end_game(tick):
                squared = False
                try:
                    player_1_runner = player_1.make_move
                    args = (self.N, self.player_1+self.player_2+self.player_3)
                    result = self.run_with_timeout(player_1_runner, args, 1)
                    assert self.is_valid(result)
                    self.player_1.append(result)
                    squared = self.update_score(result, PLAYER_1)
                except TimeoutError:
                    print("One second exceeded by Player 1")
                except Exception as e:
                    print("Invalid move Player 1")
                
                tick += 1
                if not squared: break
                
            
            # Second player
            while not self.end_game(tick):
                squared = False
                try:
                    player_2_runner = player_2.make_move
                    args = (self.N, self.player_1+self.player_2+self.player_3)
                    result = self.run_with_timeout(player_2_runner, args, 1)
                    assert self.is_valid(result)
                    self.player_2.append(result)
                    squared = self.update_score(result, PLAYER_2)
                except TimeoutError:
                    print("One second exceeded by Player 2")
                except Exception as e:
                    print("Invalid move Player 2")

                tick += 1
                if not squared:
                    break
            
            # Third player
            while not self.end_game(tick):
                squared = False
                try:
                    player_3_runner = player_3.make_move
                    args = (self.N, self.player_1+self.player_2+self.player_3)
                    result = self.run_with_timeout(player_3_runner, args, 1)
                    assert self.is_valid(result)
                    self.player_3.append(result)
                    squared = self.update_score(result, PLAYER_3)
                except TimeoutError:
                    print("One second exceeded by Player 3")
                except Exception as e:
                    print("Invalid move Player 3")

                tick += 1
                if not squared:
                    break
            
            self.display_driver()
            time.sleep(0.5)
            # os.system("cls || clear")
        self.announce_winner()
    
    def is_valid(self,move: Tuple[int, int, int, int])-> bool:
        '''
            Check whether a given move is valid ot invalid.
            Return True if valid, else Return False
        '''
        x1, y1, x2, y2 = move
        # Check if coordinates are within the valid range of the board
        if x1 < 0 or x1 >= self.N or y1 < 0 or y1 >= self.N:
            return False
        if x2 < 0 or x2 >= self.N or y2 < 0 or y2 >= self.N:
            return False
        # Check if edge already exists
        if move in [*self.player_1, *self.player_2, *self.player_3]:
            return False
        # Calculate the distance between (x1, y1) and (x2, y2)
        distance = abs(x2 - x1) + abs(y2 - y1)
        # Check if the distance is equal to 1
        if distance == 1:
            return True
        else:
            return False
    
    
    def announce_winner(self) -> None:
        # TODO:
        '''
            A function that does the finishing up of the game, 
            announce winners, display winner score, etc.
        '''
        print("Scores:")
        print("Player 1: ", self.player_1_score)
        print("Player 2: ", self.player_2_score)
        print("Player 3: ", self.player_3_score)
        if self.player_1_score > self.player_2_score and self.player_1_score > self.player_3_score:
            print("Player 1 is the winner!")
        elif self.player_2_score > self.player_1_score and self.player_2_score > self.player_3_score:
            print("Player 2 is the winner!")
        elif self.player_3_score > self.player_2_score and self.player_3_score > self.player_1_score:
            print("Player 3 is the winner!")
        elif self.player_1_score == self.player_2_score and self.player_1_score > self.player_3_score:
            print("Match Drawn Between Player 1 and Player 2!")
        elif self.player_1_score == self.player_3_score and self.player_1_score > self.player_2_score:
            print("Match Drawn Between Player 1 and Player 3!")
        elif self.player_3_score == self.player_2_score and self.player_3_score > self.player_1_score:
            print("Match Drawn Between Player 2 and Player 3!")
        else:
            print("Match Drawn between Player 1, Player 2 and Player 3!")

    
    def display_driver(self) -> None:
        # TODO:
        '''
            Shows / Updates the GUI of the environment
        '''
        print()
        print()
        for row in self.mat:
            print(*row)
        print(4*self.N*'-')

    def adjust_edge_name(self, move: Tuple) -> Tuple:
        """
        Returns the edge's representation in the fixed convention.
        """
        x1, y1, x2, y2 = move

        if x1==x2:
            # vertical line

            if y1 > y2:
                temp = x1
                x1 = x2
                x2 = temp

                temp = y1
                y1 = y2
                y2 = temp
            
        elif y1==y2:
            # horizintal line
        
            if x1 > x2:
                temp = x1
                x1 = x2
                x2 = temp

                temp = y1
                y1 = y2
                y2 = temp
        
        return (x1, y1, x2, y2)
    
    def update_score(self, move: Tuple, player: int) -> None:
        '''
            Upadte Player 1 or Player 2 or Player 3 score
            along with putting the new move on the diplay mat
        '''
        made_square = False
        all_edges = [*self.player_1, *self.player_2, *self.player_3]
        x1, y1, x2, y2 = self.adjust_edge_name(move)

        # placing coloured edge on mat
        if player == PLAYER_1: color_chosen = "red"
        elif player == PLAYER_2: color_chosen = "blue"
        elif player == PLAYER_3: color_chosen = "green"
        if x1==x2: self.mat[y1*2+1][x1*2]=colored('|', color_chosen)
        else: self.mat[y1*2][x1*2+1]=colored('-', color_chosen)

        # finding the possible boxes that can be attained
        sq1 = []
        sq2 = []
        if x1==x2:
            # vertical line
            if x1!=self.N-1:
                # right box
                sq1.append((x1, y1, x1+1, y1))
                sq1.append((x1+1, y1, x2+1, y2))
                sq1.append((x2, y2, x2+1, y2))
            if x1!=0:
                # left box
                sq2.append((x1-1, y1, x1, y1))
                sq2.append((x1-1, y1, x2-1, y2))
                sq2.append((x2-1, y2, x2, y2))
        elif y1==y2:
            # horizintal line
            if y1!=self.N-1:
                # bottom box
                sq1.append((x1, y1, x1, y1+1))
                sq1.append((x1, y1+1, x2, y2+1))
                sq1.append((x2, y2, x2, y2+1))
            if y1!=0:
                # top box
                sq2.append((x1, y1-1, x1, y1))
                sq2.append((x1, y1-1, x2, y2-1))
                sq2.append((x2, y2-1, x2, y2))
        
        # Updating score and mat
        # 1 score per edge  &  5 score per box
        score_to_add = 1
        if len(sq1)>0 and all(x in all_edges for x in sq1):
            # update score to be awarded
            score_to_add += 5
            # update the mat with assignment of box to player
            self.mat[y1*2+1][x1*2+1] = str(player)
            made_square = True
        
        if len(sq2)>0 and all(x in all_edges for x in sq2):
            # update score to be awarded
            score_to_add += 5
            # update the mat with assignment of box to player
            if x1==x2: self.mat[y1*2+1][x1*2-1] = str(player)
            elif y1==y2: self.mat[y1*2-1][x1*2+1] = str(player)
            made_square = True
            
        
        if player == PLAYER_1:
            self.player_1_score += score_to_add
        elif player == PLAYER_2:
            self.player_2_score += score_to_add
        elif player == PLAYER_3:
            self.player_3_score += score_to_add

        return made_square

# To prevent multiprocess error
print("Starting Environment...")
time.sleep(2)  

env = Environment(10)
env.start()
