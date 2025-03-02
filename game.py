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
from tokens import Tokens, YELLOW, RED, EMPTY

# token values




                
        
def main():
    """Game play"""    
    
    try:
        
        player_can_play = True # to decides who plays first
        
        # loops on new game indefinitely
        while True:
            text = ""
            tokens = Tokens(LINE_NB, COL_NB) # new game
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
                best_col, best_score = tokens.computer_play(LEVEL)
                            
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
    
def test_rows():
    tokens = Tokens(LINE_NB, COL_NB)
    
    for row in tokens.get_rows():
        display.play(tokens, "", True, row)

    display.end()

main()
#test()

#test_rows()
