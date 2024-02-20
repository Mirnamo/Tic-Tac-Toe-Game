# Define the board
# Check the winner
#Does the player always begins first?
import random

def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '-':
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '-':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != '-':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != '-':
        return board[0][2]

    return None

board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

# Define the players
players = ['X', 'O']

# Define the current player
current_player = random.choice(players)

# Start the game loop
while True:

    # Display the board
    print(board)

    # Get the player's move
    row = int(input("Enter the row number: "))
    column = int(input("Enter the column number: "))

    # Check if the move is valid
    if not (0 <= row <= 2) and (0 <= column <= 2):
        print('Invalid move.')
        continue

    # Check if the space is already occupied
    if board[row][column] != '-':
        print('Space already occupied.')
        continue

    # Make the move
    board[row][column] = current_player

    # Check if the game is over
    if check_winner(board):
        break

    # Switch players
    current_player = players[players.index(current_player) ^ 1]

# Display the winner
winner = check_winner(board)
if winner is not None:
    print(winner + ' wins!')
else:
    print('Tie game.')