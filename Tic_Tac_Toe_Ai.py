import random
import sys
import pygame
import numpy as n
import copy
# * means import all
from game_constants import *

# PYGAME SETUP
#these lines are always the same
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Game")
screen.fill(Background_color)

#self is like this keyword in JAVA

#board class
class Board():
    def __init__(self):
        #The zeros() function in Python is used to create a new array of a given shape and type, filled with zeros. 
        #It's commonly used to initialize arrays before filling them with actual data
        #Initialize the matrix
        self.squares = n.zeros((ROWS, COL))
        
    
    def mark_squares(self, row, col, player):
        self.squares[row][col] = player
    
    #check if rows and columns are empty
    def empty_squares(self, row, col):
        return self.squares[row][col] == 0



#lines that differantiate X and O
#create game class
class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1
        self.lines()

    def lines(self):
        #vertical lines
        pygame.draw.line(screen,LINES_COLOR,(SQUARE_SIZE,0),(SQUARE_SIZE,HEIGHT), WIDTH_LINE)
        pygame.draw.line(screen,LINES_COLOR,(WIDTH - SQUARE_SIZE,0),(WIDTH - SQUARE_SIZE,HEIGHT), WIDTH_LINE)

        #horizontal lines
        pygame.draw.line(screen,LINES_COLOR,(0, SQUARE_SIZE),(WIDTH,SQUARE_SIZE), WIDTH_LINE)
        pygame.draw.line(screen,LINES_COLOR,(0, HEIGHT - SQUARE_SIZE),(WIDTH, HEIGHT - SQUARE_SIZE), WIDTH_LINE)

    def player_turn(self):

        #if player is one then remiander is 1 and +1 is 2
        self.player = self.player % 2 + 1
    
    def draw_figure(self, row, col):
        if self.player == 1:
            #draw X
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, (0,0,0), start_desc, end_desc, CROSS_WIDTH)
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, (0,0,0), start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw O
            x_axis = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y_axis = row * SQUARE_SIZE + SQUARE_SIZE // 2
            center = (x_axis, y_axis)
            pygame.draw.circle(screen, (0,0,0), center, RADIUS, CIRC_WIDTH)
        
#main function
def main():

    #creating game object
    game = Game()
    board = game.board
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exist()
            #add an event
            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                #check if rows and columns are empty or not
                if board.empty_squares(row, col):
                    board.mark_squares(row,col,game.player)
                    game.draw_figure(row, col)
                    game.player_turn()

        #apply the update of the background
        pygame.display.update()

if __name__ == "__main__":
    main()