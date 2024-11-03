#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display of the game

Created on Sat Oct 19 10:53:33 2024

@author: benjamon245
"""

import pygame
import sys
# config of the game
from conf import BLOCK_SIZE, LINE_NB, COL_NB


pygame.init()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 204, 204)

# set-up of the windoz
WINDOW_WIDTH = BLOCK_SIZE*(COL_NB + 2)
WINDOW_HEIGHT = BLOCK_SIZE*(LINE_NB + 5)
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# creation of the grid Surface
grid_rect = pygame.Rect(BLOCK_SIZE, BLOCK_SIZE*2, BLOCK_SIZE*COL_NB, BLOCK_SIZE*LINE_NB)
grid = pygame.Surface((grid_rect.width, grid_rect.height))
grid.set_colorkey(BLACK)
pygame.draw.rect(grid, BLUE, grid.get_rect())
pygame.draw.rect(grid, WHITE, grid.get_rect(), 2)
for line in range(1, LINE_NB + 1):
    for col in range(1, COL_NB + 1):
        pygame.draw.circle(grid, BLACK, (BLOCK_SIZE*(col - 0.5), BLOCK_SIZE*(line - 0.5)), BLOCK_SIZE*0.4)
      
# init of the font        
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', BLOCK_SIZE)


def play(tokens, text="", highlight=False, highlighted_squares=[]):
    """Displays the grid and detects a click"""
    
    # text Surface set-up
    text_surface = my_font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = grid_rect.centerx
    text_rect.y = grid_rect.bottom + BLOCK_SIZE
    
    # displays the grid until there is a click
    while True:
            
        screen.fill(BLACK)
        
        # capturing events
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left button
                    (x, y) = event.pos # coordonates of the click in pixels
                    #print(f"Click in x: {x} et y: {y}")
                    # converting coordinates
                    col = int((x - grid_rect.left)/BLOCK_SIZE) + 1
                    line = int((grid_rect.bottom - y)/BLOCK_SIZE) + 1
                    return (line, col)
                    
        # drawing the tokens
        for line in range(1, LINE_NB + 1):
            for col in range(1, COL_NB + 1):
                if tokens.get(line, col) == "Y":
                    x_token = int(grid_rect.left + BLOCK_SIZE*(col - 0.5))
                    y_token = int(grid_rect.bottom - BLOCK_SIZE*(line - 0.5))
                    pygame.draw.circle(screen, YELLOW, (x_token, y_token), int(BLOCK_SIZE*0.5))
                    
                if tokens.get(line, col) == "R":
                    x_token = int(grid_rect.left + BLOCK_SIZE*(col - 0.5))
                    y_token = int(grid_rect.bottom - BLOCK_SIZE*(line - 0.5))
                    pygame.draw.circle(screen, RED, (x_token, y_token), int(BLOCK_SIZE*0.5))
                
        
        # display the grid (on top of the tokens)
        screen.blit(grid, grid_rect)
        
        # highlighting some squares
        for (line, col) in highlighted_squares:
            highlight_rect = pygame.Rect(grid_rect.left + BLOCK_SIZE*(col-1), grid_rect.bottom - BLOCK_SIZE*(line), BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GREEN, highlight_rect, 3)
        
        # Highlighting the text
        if highlight :
            highlight_rect = text_rect.scale_by(1.5)
            highlight_rect.centerx = text_rect.centerx
            highlight_rect.centery = text_rect.centery
            pygame.draw.rect(screen, GREEN, highlight_rect, 0, int(BLOCK_SIZE/4) )
            pygame.draw.rect(screen, WHITE, highlight_rect, 2, int(BLOCK_SIZE/4) )
        
        # writting text
        screen.blit(text_surface, text_rect)
        
        # display on window
        pygame.display.update()
        
        # Ensure program maintains a rate
        clock.tick(30)
    
    
def wait(tokens, text=""):
    """displays the grid for a short time"""
    
    text_surface = my_font.render(text, False, WHITE)
    
    # displays 10 frames
    for _ in range(10) :
            
        # re-initialiser l' écran
        screen.fill(BLACK)
        
        # event capture
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                    
                 
        # drawing the tokens
        for line in range(1, LINE_NB + 1):
            for col in range(1, COL_NB + 1):
                if tokens.get(line, col) == "Y":
                    x_token = int(grid_rect.left + BLOCK_SIZE*(col - 0.5))
                    y_token = int(grid_rect.bottom - BLOCK_SIZE*(line - 0.5))
                    pygame.draw.circle(screen, YELLOW, (x_token, y_token), int(BLOCK_SIZE*0.5))
                    
                if tokens.get(line, col) == "R":
                    x_token = int(grid_rect.left + BLOCK_SIZE*(col - 0.5))
                    y_token = int(grid_rect.bottom - BLOCK_SIZE*(line - 0.5))
                    pygame.draw.circle(screen, RED, (x_token, y_token), int(BLOCK_SIZE*0.5))
                
        
        # display the grid
        screen.blit(grid, grid_rect)
        # display the text
        screen.blit(text_surface, (BLOCK_SIZE,BLOCK_SIZE*9))
        
        # display on the window
        pygame.display.update()
        
        # Ensure program maintains a rate
        clock.tick(30)    


def end():
    """ closing the window """
    pygame.quit()
    
    
if __name__ == "__main__":
    pygame.quit()
    
    