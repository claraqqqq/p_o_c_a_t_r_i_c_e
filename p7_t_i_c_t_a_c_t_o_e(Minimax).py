"""
Mini-max Tic-Tac-Toe Player

test cases to run
1
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], \
                       [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], \
                       [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), \
                       provided.PLAYERX)   

2
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], \
                       [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], \
                       [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), \
                       provided.PLAYERO)

3
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.EMPTY, provided.PLAYERX, provided.PLAYERX], \
                       [provided.PLAYERO, provided.EMPTY, provided.PLAYERX], \
                       [provided.PLAYERO, provided.PLAYERX, provided.EMPTY]]), \
                       provided.PLAYERO) #returned bad move (1, (2, 2))

4
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], \
                       [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], \
                       [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), \
                       provided.PLAYERX)

5
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], \
                       [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], \
                       [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), \
                       provided.PLAYERX) 

6
print mm_move(provided.TTTBoard(2, False, \
                       [[provided.EMPTY, provided.EMPTY], \
                       [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)

7  
print mm_move(provided.TTTBoard(3,False,\
                       [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], \
                       [provided.EMPTY, provided.PLAYERX, provided.PLAYERX], \
                       [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]),provided.PLAYERO)    

8
print mm_move(provided.TTTBoard(3, False, \
                       [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], \
                       [provided.EMPTY, provided.EMPTY, provided.EMPTY], \
                       [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), \
                       provided.PLAYERO) 

"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)


# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):

    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    
    Your recursive function should call itself on each child of the 
    current board position and then pick the move that maximizes 
    (or minimizes, as appropriate) the score. 
    
    return 0, (-1, -1)
    """
    
    result_list_x = []
    result_list_o = []
    
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1, -1)
    
    for empty_square in board.get_empty_squares():
        board_clone = board.clone()
        
        board_clone.move(empty_square[0], empty_square[1], player)
        other_player = provided.switch_player(player)
      
        (score, (dummy_x, dummy_y)) = mm_move(board_clone, other_player)        
        best_score = score
        best_move = (empty_square[0], empty_square[1])

        element = best_score, best_move
        
        if player == provided.PLAYERX:
            result_list_x.append(element)
        else:
            result_list_o.append(element)
    
    if player == provided.PLAYERX: 
        best_score = result_list_x[0][0]
        best_move = result_list_x[0][1]
        for index in range(len(result_list_x)):
            if best_score < result_list_x[index][0]:
                best_score = result_list_x[index][0]
                best_move = result_list_x[index][1]
        return best_score, best_move
    elif player == provided.PLAYERO:
        best_score = result_list_o[0][0]
        best_move = result_list_o[0][1]
        for index in range(len(result_list_o)):
            if best_score > result_list_o[index][0]:
                best_score = result_list_o[index][0]
                best_move = result_list_o[index][1] 
        return best_score, best_move

    
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


