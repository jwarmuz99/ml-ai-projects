from ai import *
import numpy as np
RED = '\033[1;31;40m'
GREEN = '\033[0;32;47m'
BLUE = '\033[1;34;40m'
WHITE = '\033[1;37;40m'
BOARD_WIDTH  = 7
BOARD_HEIGHT = 6
RED_AI    = 1
BLUE_AI = -1

def board_init():
    """Initializes the board"""
    Board = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
    return Board


def board_full(board):
    """Checks if the board is completely filled"""
    for col in range(BOARD_WIDTH):
        if board[0][col]==0:
            return False
    return True


def winning_combination(board, disc):
    """Checks if the given move leads to a win"""
    # horizontal combinations
    for c in range(BOARD_WIDTH-3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == disc and board[r][c+1] == disc and board[r][c+2] == disc and board[r][c+3] == disc:
                return True

    # vertical combinations
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT-3):
            if board[r][c] == disc and board[r+1][c] == disc and board[r+2][c] == disc and board[r+3][c] == disc:
                return True

    # diagonal combinations in a positive slope
    for c in range(BOARD_WIDTH-3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == disc and board[r-1][c+1] == disc and board[r-2][c+2] == disc and board[r-3][c+3] == disc:
                return True

    # diagonal combinations in a negative slope
    for c in range(BOARD_WIDTH-3):
        for r in range(BOARD_HEIGHT-3):
            if board[r][c] == disc and board[r+1][c+1] == disc and board[r+2][c+2] == disc and board[r+3][c+3] == disc:
                return True

    return False


def ai_turn(board,depth,ai_color,player_color):
    """Uses minimax algorithm to find the best move and performs it"""
    ai_move  = minimax(board, depth, float("-inf"), float("inf"), ai_color,player_color)[0]
    board = drop_disc(board, ai_move, ai_color)
    ai_won  = winning_combination(board, ai_color)
    return  board, ai_won



def GAME(red_depth, blue_depth):
    winner = None
    board = board_init()
    while True:
        if board_full(board):
            winner = 0.5
            break

        # red AI's move
        board, ai_won = ai_turn(board,red_depth,RED_AI,RED_AI)
        if ai_won:
            winner = 1
            break

        # blue AI's move
        board, ai_won = ai_turn(board,blue_depth,BLUE_AI,BLUE_AI)
        if ai_won:
            winner = 0
            break

    return winner

games = []
for red in range(1, 6):
    for blue in range(1, 6):
        games.append([red, blue, GAME(red,blue)])

results = {}
for game in games:
    try:
        results[game[1]-game[0]].append(game[2])
    except:
        results[game[1]-game[0]] = []
        results[game[1]-game[0]].append(game[2])

means = []
for diff, res in results.items():
    means.append((diff, np.mean(res)))

means.sort(key=lambda x:x[0])
for rv in means:
    print(f"Mean winning ratio for the first player when difference in depth is {rv[0]}: {rv[1]}")