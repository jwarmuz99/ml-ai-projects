import random
from copy import deepcopy

BOARD_WIDTH  = 7
BOARD_HEIGHT = 6
AI_PLAYER    = -1
HUMAN_PLAYER = 1
NEUTRAL = 0

def valid_column(board, col):
    """Checks if a column is not full and a disc can be inserted in it"""
    return board[0][col] == 0


def make_gravity(board, col):
    """Drops the disc in to the lowest empty row of a chosen column"""
    for r in range(BOARD_HEIGHT):
        if board[r][col] == 0:
            return r


def leaf_node(board):
    """Checks if the visited by minimax node is a leaf"""
    return winning_combination(board, HUMAN_PLAYER) or winning_combination(board, AI_PLAYER) or len(all_valid_columns(board)) == 0


def drop_disc(board, col, player):
    """Drops a given player's disc into a chosen column"""
    tmp = deepcopy(board)
    for row in range(BOARD_HEIGHT-1,-1,-1):
        if tmp[row][col] == 0:
            tmp[row][col] = player
            return tmp


def all_valid_columns(board):
    """Gets a list of all columns with empty rows"""
    valid_locations = []
    for col in range(BOARD_WIDTH):
        if valid_column(board, col):
            valid_locations.append(col)
    return valid_locations


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


def utility_helper(subarray, player):
    """
    Performs part of the utility function calculations.
    It calculates the occurrences of a given player's discs in subarrays of 4 subsequent slots.
    The values assigned are arbitrary and it is possible that different values might lead to improved performance
    """
    utility = 0
    opponent = HUMAN_PLAYER
    if player == HUMAN_PLAYER:
        opponent = AI_PLAYER

    if subarray.count(player) == 4:
        utility += 100
    elif subarray.count(player) == 3 and subarray.count(NEUTRAL) == 1:
        utility += 10
    elif subarray.count(player) == 2 and subarray.count(NEUTRAL) == 2:
        utility += 5
    elif subarray.count(player) == 1 and subarray.count(NEUTRAL) == 3:
        utility += 2

    if subarray.count(opponent) == 3 and subarray.count(NEUTRAL) == 1:
        utility -= 10
    elif subarray.count(opponent) == 2 and subarray.count(NEUTRAL) == 2:
        utility -= 5

    return utility


def calculate_utility(board, player):
    """
    Performs the calculation of the utility function
    It uses a heuristic that the center column is the most valuable
    """
    utility = 0

    # horizontal
    for row_array in board:
        for c in range(BOARD_WIDTH-3):
            subarray = row_array[c:c+4]
            utility += utility_helper(subarray, player)

    # vertical
    for c in range(BOARD_WIDTH):
        col_array = [row[c] for row in board]
        for r in range(BOARD_HEIGHT-3):
            subarray = col_array[r:r+4]
            utility += utility_helper(subarray, player)

    # diagonal with positive slope
    for r in range(BOARD_HEIGHT-3):
        for c in range(BOARD_WIDTH-3):
            subarray = [board[r+i][c+i] for i in range(4)]
            utility += utility_helper(subarray, player)

    # diagonal with negative slope
    for r in range(BOARD_HEIGHT-3):
        for c in range(BOARD_WIDTH-3):
            subarray = [board[r+3-i][c+i] for i in range(4)]
            utility += utility_helper(subarray, player)

    # center column
    center_column = [row[BOARD_WIDTH//2] for row in board]
    center_count = center_column.count(player)
    utility += 2*center_count
    
    return utility


def minimax(board, depth, alpha, beta, maximizer):
    """Implements the minimax search algorithm with alpha beta pruning"""
    # gets all the valid columns
    valid_locations = all_valid_columns(board)
    # checks if the leaf node is hit
    is_terminal = leaf_node(board)
    # case for when the leaf node is found or we reached the depth limit
    if depth == 0 or is_terminal:
        # case for leaf noode
        if is_terminal:
            # assigning the utility value in case AI won
            if winning_combination(board, AI_PLAYER):
                return (None, float("inf"))
            # assigning the utility value in case user won
            elif winning_combination(board, HUMAN_PLAYER):
                return (None, float("-inf"))
            # returns a neutral utility when draw
            else: 
                return (None, 0)
        # if we reached the depth limit, we want to calculate the utility of that state
        else: 
            return (None, calculate_utility(board, AI_PLAYER))
    # case for the MAX player
    if maximizer:
        # initialize utility to negative infinity
        value = float("-inf")
        # choose a random branch of the game decision tree
        # and run the minimax AB algo on each possible next depth level game configuration
        column = random.choice(valid_locations)
        for col in valid_locations:
            # copy the board not to confuse the states so that the traversal works as expected
            tmp_board = board.copy()
            # drop a players disc in the given column
            tmp_board = drop_disc(tmp_board, col, AI_PLAYER)
            # and go to the next depth level by recursively calling the minimax function
            new_utility = minimax(tmp_board, depth-1, alpha, beta, False)[1]
            # update the best move
            if new_utility > value:
                value = new_utility
                column = col
            # and prune the tree if alpha exceeds beta
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    # run the opposite for the MIN player
    else:
        value = float("inf")
        column = random.choice(valid_locations)
        for col in valid_locations:
            tmp_board = board.copy()
            tmp_board = drop_disc(tmp_board, col, HUMAN_PLAYER)
            new_utility = minimax(tmp_board, depth-1, alpha, beta, True)[1]
            if new_utility < value:
                value = new_utility
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
