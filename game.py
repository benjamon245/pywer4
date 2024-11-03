#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Power 4 game logic

Created on Thu Oct 24 20:37:03 2024

@author: benjamon245
"""

# config of the game
from conf import LEVEL, LINE_NB, COL_NB
import display


# token values
YELLOW = "Y"
RED = "R"
EMPTY = "0"


class Tokens:
    """Represents the state of the game"""
    
    def __init__ (self):
        self.array = [] # array with tokens'values
        for _ in range(LINE_NB):
            self.array.append([EMPTY] * COL_NB)
        
    def copy(self):
        """deep copies the instance """
        new = Tokens()
        for col in range(0, COL_NB):
            for line in range(0, LINE_NB):
                new.array[line][col] = self.array[line][col]
        return new
        
    def isfull(self):
        """cheks if the grid is full"""
        for line in range(1, LINE_NB + 1):
            for col in range(1, COL_NB +1):
                if self.get(line, col) == EMPTY:
                    return False
        return True
        
    def get (self, line, col):
        """gets a token's value """
        return self.array[6 - line][col - 1]
        
    def set_token(self, line, col, color):
        """sets a token's value for a given line and column"""
        self.array[6 - line][col - 1] = color
        
            
    def set_col(self, col, color):
        """sets a token's value for a given column (figures the line itself)"""
        # check if valid column
        if self.get(6, col) != EMPTY:
            return False
        
        # set the right  token
        for line in range(1, LINE_NB + 1):
            if self.get(line, col) == EMPTY:
                self.set_token(line, col, color)
                break
        
        return True
        
    def check(self, line, col):
        """checks if a token can be set at given line and column"""
        return ((line >=1) and (line <=LINE_NB) and (col >=1) and (col <= COL_NB) 
                and ((line == 1) or (self.get(line - 1, col) != EMPTY )) and (self.get(line, col) == EMPTY))
    
    def get_rows(self):
        """returns the list of all rows of the grid
        A row is a list of aligned squares in the grid with minimum size 4"""
        # TODO: doesn't need to be a method of Tokens
        # TODO: doesn't need to run again and again: it always gives the same answer
        
        rows = []
        # column rows
        for col in range(1, COL_NB + 1):
            row = []
            for line in range(1, LINE_NB + 1):
                row.append((line, col))
            rows.append(row)
        # line rows
        for line in range(1, LINE_NB + 1):
            row = []
            for col in range(1, COL_NB + 1):
                row.append((line, col))
            rows.append(row)
        # diagonal rows (bottom left to top right)
        for line in range(-2, 4):
            row = []
            for col in range(1, COL_NB + 1):
                observed_line = line + col - 1
                if (observed_line >= 1) and (observed_line <= 6):
                    row.append((observed_line, col))
            rows.append(row)
        # diagonal rows (from top left to bottom right)
        for line in range(-2, 4):
            row = []
            for col in range(1, COL_NB + 1):
                observed_line = line - col + 7
                if (observed_line >= 1) and (observed_line <= 6):
                    row.append((observed_line, col))
            rows.append(row)
        
        return rows
    
    def win(self, color = YELLOW):
        """detects if the input colors has won"""
        for row in self.get_rows():
            win_squares = []
            in_a_row = 0
            for tup in row:
                (line, col) = tup
                result = self.get(line, col)
                if result == color:
                    in_a_row += 1
                    win_squares.append(tup)
                else:
                    in_a_row = 0
                    win_squares = []
                if in_a_row == 4:
                    return True, win_squares 
        return False, []

    def get_in_a_rows(self, color = YELLOW):
        """returns al list of all numbers of tokens aligned in a row for the input color
        only considers cases where there is space to go up to 4 in a row"""
        in_a_row_list = []
        # loops on possible rows
        for row in self.get_rows():
            in_a_row = 0 # tokens of the color in a row
            in_a_row_potential = 0 # tokens of the color or empty in a row
            for (line, col) in row:
                result = self.get(line, col)
                if result == color:
                    in_a_row += 1
                if (result == EMPTY) or (result == color):
                    in_a_row_potential +=1
                else:
                    if (in_a_row_potential >= 4) and (in_a_row > 0):
                        in_a_row_list.append(in_a_row)
                    in_a_row_potential = 0
                    in_a_row = 0
            if (in_a_row_potential >= 4) and (in_a_row > 0):
                in_a_row_list.append(in_a_row)
                
        return in_a_row_list
                

    def score_bot(self):
        """Evaluates how good is the position of the Reds in the game.
        The higher the score the better the position of the red.
        Score above 0 means better position compared to Yellows
        The score is based on numbers of tokens in a row"""
        
        score = 0
        # Is there a winner?
        if self.win(RED)[0]:
            return 1000000
        if self.win(YELLOW)[0]:
            return -1000000
        
        # assigning values for every number of in-a-row tokens
        in_a_row_red = self.get_in_a_rows(RED)
        in_a_row_yellow = self.get_in_a_rows(YELLOW)
        for iar in in_a_row_red:
            if iar == 1: score += 10    # 1 red tokens in a row
            if iar == 2: score += 100   # 2 red tokens in a row
            if iar >= 3: score += 1000  # 3 red tokens in a row
        for iar in in_a_row_yellow:
            if iar == 1: score += -10   # 1 yellow tokens in a row
            if iar == 2: score += -100  # 2 yellow tokens in a row
            if iar >= 3: score += -1000 # 3 yellow tokens in a row
        
        return score
    
    
    def simulate(self, depth, color=RED):
        """Recursively simulate N moves in advance 
        to return the bets possible score for input color.
        For the last level of simulation we use score_bot method.
        Min-Max algorithm: each player plays optimal move
        """
        
        # in case there is a winner return high value 
        if color == RED:
            opposite_color = YELLOW
            sign = 1
        else:
            opposite_color = RED
            sign = -1 
        if self.win(color)[0]:
            # value returned must be higher if we are not deep in the simulation
            # to favor losing in 4 moves compared to lose in 2 moves for example
            return sign * 1000000*(1 + depth)
        
        # For the last level of simulation we use score_bot method.
        if depth == 0:
            return self.score_bot()
        
        # Min-Max algorithm
        best_score = None
        for col in range(1, COL_NB + 1):
            emulation = self.copy()
            if emulation.set_col(col, color):
                score = emulation.simulate(depth-1, opposite_color)
                if color == RED:
                    if (best_score is None) or (score > best_score):
                        best_score = score
                if color == YELLOW:
                    if (best_score is None) or (score < best_score):
                        best_score = score
        return best_score
                
        
    def __str__(self):
        s = ""
        for line in self.array:
            s += f"{line}\n"
        return s
                
        
def main():
    """Game play"""    
    
    try:
        
        player_can_play = True # to decides who plays first
        
        # loops on new game indefinitely
        while True:
            text = ""
            tokens = Tokens() # new game
            # loops on one player move and one bot move
            while True:
                
                ### player plays
                if player_can_play :
                    check = False
                    # check if the move is valid
                    while check == False:
                        # get move from click on the grid
                        (line, col) = display.play(tokens, "à toi de jouer")
                        print((line, col))
                        check = tokens.check(line, col)
                        
                    # sets the token
                    tokens.set_token(line, col, YELLOW)
                                    
                    # checks whether yellow wins
                    winner, squares = tokens.win(color = YELLOW)
                    if winner:
                        print("yellow wins")
                        text = "Bravo !"
                        player_can_play = False
                        break
    
                    # checks if the board is full (Tie)
                    if tokens.isfull():
                        print("Tie")
                        text = "Egalité !"
                        break

                    
                else: 
                    player_can_play = True
                
                # waits a bit before playing
                display.wait(tokens)
                ### bot plays
                best_col = None
                best_score = None
                # check what is the best move with emulation
                for col in range(1, COL_NB + 1):
                    emulation = tokens.copy()
                    if emulation.set_col(col, RED):
                        score = emulation.simulate(depth=LEVEL, color=YELLOW)
                        if (best_score is None) or (score > best_score):
                            best_col = col
                            best_score = score
                            
                # sets the token
                tokens.set_col(best_col, RED)
                    
                # checks whether red wins                
                winner, squares = tokens.win(color = RED)
                if winner:
                    print("Red wins")
                    text = "Looser"

                    break
                # checks if the board is full (Tie)
                if tokens.isfull():
                    print("Tie")
                    text = "Egalité !"
                    squares = []
                    break

            # highlighting the winning tokens'squares
            display.play(tokens, text, True, squares)
        
    
    except:
        display.end()
        raise
        
        


def test():
    
    tokens = Tokens()
    
    tokens.set_token(2, 4, RED)
    #tokens.set_token(3, 2, YELLOW)
    #tokens.set_token(4, 3, YELLOW)
    #tokens.set_token(5, 4, YELLOW)
    tokens.set_token(2, 2, RED)
    
    tokens.set_token(6, 4, RED)
    #tokens.set_token(5, 5, YELLOW)
    #tokens.set_token(4, 6, YELLOW)
    #tokens.set_token(3, 7, YELLOW)
    tokens.set_token(6, 3, RED)
    tokens.set_token(3, 7, RED)
    tokens.set_token(2, 7, RED)
    tokens.set_token(1, 7, RED)
    tokens.set_token(1, 4, RED)
    #tokens.set_token(4, 7, YELLOW)
    #tokens.set_token(6, 5, YELLOW)
    
    print(tokens)
    print(tokens.get_in_a_rows(YELLOW))
    print(tokens.get_in_a_rows(RED))
    print(tokens.score_bot())
    
    display.end()
    

main()
#test()