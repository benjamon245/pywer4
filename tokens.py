#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:01:35 2025

@author: glg
"""
YELLOW = "Y"
RED = "R"
EMPTY = "0"

class Tokens:
    """Represents the state of the game"""
    
    def __init__ (self, linenb, colnb):
        self.linenb = linenb
        self.colnb = colnb
        self.array = [] # array with tokens'values
        for _ in range(self.linenb):
            self.array.append([EMPTY] * self.colnb)
        
    def copy(self):
        """deep copies the instance """
        new = Tokens(self.linenb, self.colnb)
        for col in range(0, self.colnb):
            for line in range(0, self.linenb):
                new.array[line][col] = self.array[line][col]
        return new
        
    def isfull(self):
        """cheks if the grid is full"""
        for line in range(1, self.linenb + 1):
            for col in range(1, self.colnb +1):
                if self.get(line, col) == EMPTY:
                    return False
        return True
        
    def get (self, line, col):
        """gets a token's value """
        return self.array[self.linenb - line][col - 1]
        
    def set_token(self, line, col, color):
        """sets a token's value for a given line and column"""
        self.array[self.linenb - line][col - 1] = color
        
            
    def set_col(self, col, color):
        """sets a token's value for a given column (figures the line itself)"""
        # check if valid column
        if self.get(self.linenb, col) != EMPTY:
            return False
        
        # set the right  token
        for line in range(1, self.linenb + 1):
            if self.get(line, col) == EMPTY:
                self.set_token(line, col, color)
                break
        
        return True
    
    
    def get_line(self, col):
        """figures the next free line for a given column"""
        for line in range(1, self.linenb + 1):
            if self.get(line, col) == EMPTY:
                return line
        
        return None
        
    def check(self, line, col):
        """checks if a token can be set at given line and column"""
        return ((line >=1) and (line <=self.linenb) and (col >=1) and (col <= self.colnb) 
                and ((line == 1) or (self.get(line - 1, col) != EMPTY )) and (self.get(line, col) == EMPTY))
    
    def get_rows(self):
        """returns the list of all rows of the grid
        A row is a list of aligned squares in the grid with minimum size 4"""
        # TODO: doesn't need to be a method of Tokens
        # TODO: doesn't need to run again and again: it always gives the same answer
        
        rows = []
        # column rows
        for col in range(1, self.colnb + 1):
            row = []
            for line in range(1, self.linenb + 1):
                row.append((line, col))
            rows.append(row)
        # line rows
        for line in range(1, self.linenb + 1):
            row = []
            for col in range(1, self.colnb + 1):
                row.append((line, col))
            rows.append(row)
        # diagonal rows (bottom left to top right)
        for line in range(-self.colnb+4, self.linenb-2):
            row = []
            for col in range(1, self.colnb + 1):
                observed_line = line + col - 1
                if (observed_line >= 1) and (observed_line <= self.linenb) and (col >= 1) and (col <= self.colnb):
                    row.append((observed_line, col))
            if len(row) >= 4 : 
                rows.append(row)
        # diagonal rows (from top left to bottom right)
        for line in range(-self.colnb+5, self.linenb-2):
            row = []
            for col in range(1, self.colnb + 1):
                observed_line = line - col + self.colnb 
                if (observed_line >= 1) and (observed_line <= self.linenb) and (col >= 1) and (col <= self.colnb):
                    row.append((observed_line, col))
            if len(row) >= 4 : 
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
        for col in range(1, self.colnb + 1):
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
    
    def computer_play(self, level=1):           
        ### bot plays
        best_col = None
        best_score = None
        # check what is the best move with emulation
        for col in range(1, self.colnb + 1):
            emulation = self.copy()
            if emulation.set_col(col, RED):
                score = emulation.simulate(depth=level, color=YELLOW)
                if (best_score is None) or (score > best_score):
                    best_col = col
                    best_score = score
        return best_col, best_score
    
    
    def __str__(self):
        s = ""
        for line in self.array:
            s += f"{line}\n"
        return s