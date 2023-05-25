import chess 
import chess_display
import random
from copy import deepcopy

def random_movement(BOARD):
    return random.choice(list(BOARD.legal_moves))

point_values = {
            'p' : -1,
            'n' : -3,
            'b' : -3,
            'r' : -5,
            'q' : -9,
            'k' : 0,
            'P' : 1,
            'N' : 3,
            'B' : 3,
            'R' : 5,
            'Q' : 9,
            'K' : 0
         }

def evaluate_board(BOARD):
    points = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        points += point_values[str(pieces[key])]
        
    return points

def min_max_movement(BOARD):
    moves = list(BOARD.legal_moves)
    points = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        points.append(evaluate_board(temp))

        if BOARD.turn == True:
            best_move = moves[points.index(max(points))]
        else:
            best_move = moves[points.index(min(points))]
        
        return best_move
    

def min_max_movement_depth_N(BOARD, N):
    moves = list(BOARD.legal_moves)
    points = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        
        if N > 1:
            temp_best_move = min_max_movement_depth_N(temp, N-1)
            temp.push(temp_best_move)

        points.append(evaluate_board(temp))

        if BOARD.turn == True:
            best_move = moves[points.index(max(points))]
        else:
            best_move = moves[points.index(min(points))]
        
        return best_move
    
def min_max_algorithm(BOARD):
    return min_max_movement_depth_N(BOARD, 3)

    
chess_display.chess_engine(chess_display.chess_board, min_max_algorithm, chess.BLACK)