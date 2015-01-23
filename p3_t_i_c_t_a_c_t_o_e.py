"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 300    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
  
    
# Add your functions here.
    
def mc_trial(board, player):
    """
    takes a current board and the next player to move. 
    The function should play a game starting with the given player 
    by making random moves, alternating between players. 
    The function should return when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything.
    """
    # while board.check_win() == None:
    while (board.check_win() != 2) and (board.check_win() != 3) and (board.check_win() != 4) and (len(board.get_empty_squares()) != 0):
        empty = board.get_empty_squares()
        pos = random.choice(empty)
        board.move(pos[0], pos[1], player)
        # play_next = switch_player(player)
        if player == 2:
            player = 3
        else:
            player = 2 
    return 5


def mc_update_scores(scores, board, player): 
    """
    This function takes a grid of scores (a list of lists) with the 
    same dimensions as the Tic-Tac-Toe board, a board from a completed game, 
    and which player the machine player is. 
    The function should score the completed board and update the scores grid. 
    As the function updates the scores grid directly, 
    it does not return anything
    """
    result = board.check_win()
    pos_all = tuple((row, col) for row in range(board.get_dim()) 
                               for col in range(board.get_dim()))
       
    if result == player:
        for (row, col) in pos_all:
            if board.square(row, col) == player:
                scores[row][col] += MCMATCH
            elif board.square(row, col) == 1:
                scores[row][col] += 0
            else:
                scores[row][col] -= MCOTHER
    elif result == 4:
        scores = scores
    else:
        for (row, col) in pos_all:
            if board.square(row, col) == player:
                scores[row][col] -= MCMATCH
            elif board.square(row, col) == 1:
                scores[row][col] += 0
            else:
                scores[row][col] += MCOTHER
    
                
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with the maximum score 
    and randomly return one of them as a (row, column) tuple. 
    It is an error to call this function with a board that has no empty 
    squares (there is no possible next move), 
    so your function may do whatever it wants in that case. 
    The case where the board is full will not be tested.
    """
    if len(board.get_empty_squares()) == 0:
        return None
    # first turn of selection
    max_score = -1000000000000000       
    for empty in board.get_empty_squares():
        if scores[empty[0]][empty[1]] > max_score:
            max_score = scores[empty[0]][empty[1]]
    # second turn of selection
    best_score = []
    for empty in board.get_empty_squares():
        if scores[empty[0]][empty[1]] == max_score:
            best_score.append(empty)
    pos_choose = random.randrange(len(best_score))
    return best_score[pos_choose]


def mc_move(board, player, trials): 
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. 
    The function should use the Monte Carlo simulation described above to 
    return a move for the machine player in the form of a (row, column) tuple.
    Be sure to use the other functions you have written!
    """
    scores = [[0 for dummy_row in range(board.get_dim())]
                 for dummy_col in range(board.get_dim())]
    for dummy_trial in range(trials):
       board_test = board.clone()
       while mc_trial(board_test, player) != 5:
            mc_trial(board_test, player)
       mc_update_scores(scores, board_test, player)             
    return get_best_move(board, scores)    
        
    
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
