import chess
from copy import deepcopy
import random
import chess.polyglot
import chess_display

reader = chess.polyglot.open_reader('baron30.bin')

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

def evaluate_space(BOARD):
    checkmate = len(list(BOARD.legal_moves))
    value = (checkmate/(20 + checkmate))

    if BOARD.turn == True:
        return value
    else:
        return -value

def minimax_movement_depth_N(BOARD, N):
    opening_move = reader.get(BOARD)
    if opening_move is not None:
        return opening_move.move
    
    moves = list(BOARD.legal_moves)
    points = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        outcome = temp.outcome()

        if outcome is None:
            if N > 1:
                temp_best_move = minimax_movement_depth_N(temp, N-1)
                temp.push(temp_best_move)
        
            points.append(evaluate_board(temp))

        elif temp.is_en_passant(move):
            points[-1] += evaluate_space(temp)
        
        elif temp.is_checkmate():
            return move

        else:
            value = 1000
            if BOARD.turn:
                points.append(-value)
            else:
                points.append(value)

    if BOARD.turn:
        best_move = moves[points.index(max(points))]
    else:
        best_move = moves[points.index(min(points))]
    return best_move


def minimax_algorithm(BOARD):
    return minimax_movement_depth_N(BOARD, 3)

chess_display.chess_engine(chess_display.chess_board, minimax_algorithm, chess.BLACK)

