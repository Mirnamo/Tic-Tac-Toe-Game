import copy
import sys
import pygame
import random
import numpy as n

from game_constants import *

# PYGAME SETUP

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(Background_color)

# CLASSES

class Board:

    def __init__(self):
        self.squares = n.zeros((ROWS, COL))
        self.marked_sqrs = 0

    def final_state(self, show=False):

        # Vertical wins
        for col in range(COL):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = LINES_COLOR if self.squares[0][col] == 2 else LINES_COLOR
                    start_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    end_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, start_pos, end_pos, WIDTH_LINE)
                return self.squares[0][col]

        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = LINES_COLOR if self.squares[row][0] == 2 else LINES_COLOR
                    start_pos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    end_pos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, start_pos, end_pos, WIDTH_LINE)
                return self.squares[row][0]

        # Descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = LINES_COLOR if self.squares[1][1] == 2 else LINES_COLOR
                start_pos = (20, 20)
                end_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, start_pos, end_pos, CROSS_WIDTH)
            return self.squares[1][1]

        # Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = LINES_COLOR if self.squares[1][1] == 2 else LINES_COLOR
                start_pos = (20, HEIGHT - 20)
                end_pos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, start_pos, end_pos, CROSS_WIDTH)
            return self.squares[1][1]

        # No win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COL):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def choice_random(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(len(empty_sqrs))
        return empty_sqrs[idx] 

    def minimax(self, board, maximizing):
        # Terminal case
        terminalCase = board.final_state()

        # Player 1 wins
        if terminalCase == 1:
            return 1, None

        # Player 2 wins
        if terminalCase == 2:
            return -1, None

        # Draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.choice_random(main_board)
        else:

            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in position {move} with an evaluation of: {eval}')

        return move

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # 1-cross  # 2-circles
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        # Background
        screen.fill(Background_color)

        # Vertical lines
        pygame.draw.line(screen, LINES_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), WIDTH_LINE)
        pygame.draw.line(screen, LINES_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), WIDTH_LINE)

        # Horizontal lines
        pygame.draw.line(screen, LINES_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), WIDTH_LINE)
        pygame.draw.line(screen, LINES_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), WIDTH_LINE)

    def draw_fig(self, row, col):
        if self.player == 1:
            # Draw cross
            # Descending line
            start_desc = (col *SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, LINES_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # Ascending line
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, LINES_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # Draw circle
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, LINES_COLOR, center, RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # Objects
    game = Game()
    board = game.board
    ai = game.ai

    # Main loop
    while True:
        
        # Pygame events
        for event in pygame.event.get():

            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keydown event
            if event.type == pygame.KEYDOWN:

                # G - Gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # R - Restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0 - Random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 - Random AI
                if event.key == pygame.K_1:
                    ai.level = 1

            # Click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                
                # Human mark square
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # Update the screen
            pygame.display.update()

            # AI evaluation
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

if __name__ == "__main__":
    main()
