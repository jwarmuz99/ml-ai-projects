from ai import *
import time
import random
RED = '\033[1;31;40m'
GREEN = '\033[0;32;47m'
BLUE = '\033[1;34;40m'
WHITE = '\033[1;37;40m'
BOARD_WIDTH  = 7
BOARD_HEIGHT = 6
AI_PLAYER    = -1
HUMAN_PLAYER = 1

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


def display_board(Board):
    print('')
    print('')
    print("\t  1 | 2 | 3 | 4 | 5 | 6 | 7 ")
    print("\t  _   _   _   _   _   _   _")

    for i in range(0, BOARD_HEIGHT, 1):
        print("\t",end="")
        for j in range(BOARD_WIDTH):
            if Board[i][j] == 1:
                print("| " + BLUE + 'x' +WHITE, end=" ")
            elif Board[i][j] == -1:
                print("| " + RED + "o" +WHITE, end=" ")
            else:
                print("| " + " ", end=" ")

        print("|")
    print('')


def user_turn(board):
    """Serves the user's turn"""
    Col = input('Choose a Column between 1 and 7: ')
    if not(Col.isdigit()):
        print("CHOOSE AN INTEGER")
        return user_turn(board)

    user_ply = int(Col) - 1
    
    if (not(valid_column(board, user_ply))) or (user_ply < 0 or user_ply > 6):
        print("CHOOSE A VALID COLUMN NUMBER")
        return user_turn(board)

    board = drop_disc(board, user_ply, HUMAN_PLAYER)
    user_won  = winning_combination(board, HUMAN_PLAYER)
    return board, user_won


def player_winning_message(board):
    """Displays the congratulation message and asks if the user wants to play again"""
    display_board(board)
    print('                    '+BLUE+"YOU WON, HUMAN!\n" +WHITE)
    restart = True if input('DO YOU WANT TO PLAY AGAIN(y/n)?'+WHITE).lower() == 'y' else False
    if restart:
        GAME()
    return True


def ai_turn(board,depth):
    """Uses minimax algorithm to find the best move and performs it"""
    print(RED+"I'M THINKING..."+WHITE)
    time.sleep(random.randint(0,3))
    ai_move  = minimax(board, depth, float("-inf"), float("inf"), AI_PLAYER)[0]
    board = drop_disc(board, ai_move, AI_PLAYER)
    ai_won  = winning_combination(board, AI_PLAYER)
    return  board, ai_won


def ai_winning_message(board):
    """Displays a bragging message and asks if the user wants to get beaten again"""
    display_board(board)
    print('                     '+RED+"(A)I WON!\n" +WHITE)
    restart = True if input('DO YOU WANT TO PLAY AGAIN(y/n)?'+WHITE).lower() == 'y' else False
    if restart:
        GAME()
    return True


def GAME():
    depth = int(input(RED+"ON A SCALE FROM 1 TO 5, HOW SMART DO YOU WANT ME TO GET? "+WHITE))
    board = board_init()
    player_starts = True if input(RED+'DO YOU WANNA START(y/n)? '+WHITE).lower() == 'y' else False
    print(RED+"ALRIGHT, LET'S GO!"+WHITE)
    display_board(board)
    game_over = False
    while not game_over:
        if board_full(board):
            print('                     '+"GAME OVER, IT'S A DRAW\n")
            restart = True if input('DO YOU WANT TO PLAY AGAIN(y/n)?'+WHITE).lower() == 'y' else False
            if restart:
                GAME()
            break

        if player_starts:
            # Player's move
            board, user_won = user_turn(board)
            if user_won:
                game_over = player_winning_message(board)
                if game_over:
                    break
            display_board(board)

            # AI's move
            board, ai_won = ai_turn(board,depth)
            if ai_won:
                game_over = ai_winning_message(board)
                if game_over:
                    break
            display_board(board)

        else:
            # AI's move
            board, ai_won = ai_turn(board,depth)
            if ai_won:
                game_over = ai_winning_message(board)
                if game_over:
                    break
            display_board(board)

            # Player's move
            board, user_won = user_turn(board)
            if user_won:
                game_over = player_winning_message(board)
                if game_over:
                    break

            display_board(board)


print(RED+"HEY HUMAN, IT'S AI :)"+WHITE)
print(RED+"LET'S PLAY A GAME!"+WHITE)
GAME()
