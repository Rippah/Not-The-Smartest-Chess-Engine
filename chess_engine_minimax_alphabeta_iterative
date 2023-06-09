import chess
from stockfish import Stockfish
from copy import deepcopy
import random
import chess.polyglot
import chess_display

reader = chess.polyglot.open_reader('gm2600.bin')

def random_movement(BOARD):
    return random.choice(list(BOARD.legal_moves))

point_values = {
            'p' : -100,
            'n' : -320,
            'b' : -330,
            'r' : -500,
            'q' : -900,
            'k' : -2000,
            'P' :  100,
            'N' :  320,
            'B' :  330,
            'R' :  500,
            'Q' :  900,
            'K' :  2000
               }

pawn_table_white = [
    0,   0,   0,   0,   0,   0,   0,   0,
    50,  50,  50,  50,  50,  50,  50,  50,
    10,  10,  20,  30,  30,  20,  10,  10,
    5,   5,   10,  25,  25,  10,  5,   5,
    0,   0,   0,   20,  20,  0,   0,   0,
    5,   -5,  -10, 0,   0,   -10, -5,  5,
    5,   10,  10,  -20, -20, 10,  10,  5,
    0,   0,   0,   0,   0,   0,   0,   0
]

knight_table_white = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0,   0,   0,   0,   -20, -40,
    -30, 0,   10,  15,  15,  10,  0,   -30,
    -30, 5,   15,  20,  20,  15,  5,   -30,
    -30, 0,   15,  20,  20,  15,  0,   -30,
    -30, 5,   10,  15,  15,  10,  5,   -30,
    -40, -20, 0,   5,   5,   0,   -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishop_table_white = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5,   0,   0,   0,   0,   5,   -10,
    -10, 10,  10,  10,  10,  10,  10,  -10,
    -10, 0,   10,  10,  10,  10,  0,   -10,
    -10, 5,   5,   10,  10,  5,   5,   -10,
    -10, 0,   5,   10,  10,  5,   0,   -10,
    -10, 0,   0,   0,   0,   0,   0,   -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rook_table_white = [
    0,   0,   0,   5,   5,   0,   0,   0,
    5,   0,   0,   0,   0,   0,   0,   5,
    5,   0,   0,   0,   0,   0,   0,   5,
    5,   0,   0,   0,   0,   0,   0,   5,
    5,   0,   0,   0,   0,   0,   0,   5,
    5,   0,   0,   0,   0,   0,   0,   5,
    -5,  -10, -10, -10, -10, -10, -10, -5,
    0,   0,   0,   0,   0,   0,   0,   0
]

queen_table_white = [
    -20, -10, -10, -5,  -5,  -10, -10, -20,
    -10, 0,   0,   0,   0,   0,   0,   -10,
    -10, 0,   5,   5,   5,   5,   0,   -10,
    -5,  0,   5,   5,   5,   5,   0,   -5,
    0,   0,   5,   5,   5,   5,   0,   -5,
    -10, 5,   5,   5,   5,   5,   0,   -10,
    -10, 0,   5,   0,   0,   0,   0,   -10,
    -20, -10, -10, -5,  -5,  -10, -10, -20
]

king_table_white = [
    20,  30,  10,  0,   0,   10,  30,  20,
    20,  20,  0,   0,   0,   0,   20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

pawn_table_black = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 5, 5, 5, 5, 5, 5, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
    -5, -5, -5, -5, -5, -5, -5, -5,
    -5, -5, -5, -5, -5, -5, -5, -5,
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 5, 5, 5, 5, 5, 5, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

knight_table_black = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishop_table_black = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -10, 5, 5, 10, 10, 5, 0, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 10, 10, 10, 10, 5, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rook_table_black = [
    0, 0, 0, 5, 5, 0, 0, 0,
    5, 0, 0, 0, 0, 0, 0, 5,
    5, 0, 0, 0, 0, 0, 0, 5,
    5, 0, 0, 0, 0, 0, 0, 5,
    5, 0, 0, 0, 0, 0, 0, 5,
    5, 0, 0, 0, 0, 0, 0, 5,
    -5, -10, -10, -10, -10, -10, -10, -5,
    0, 0, 0, 0, 0, 0, 0, 0
]

queen_table_black = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

king_table_black = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
]


king_table_end_game = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]


center_squares = {chess.E4, chess.E5, chess.D4, chess.D5}
center_value = 75

center_box = {chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D6, chess.E3, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6}
center_box_value = 25

def evaluate_board(BOARD):
    points = 0
    pieces = BOARD.piece_map()

    for square, piece in pieces.items():
        piece_value = point_values[str(piece)]
        points += piece_value

        if BOARD.is_attacked_by(BOARD.turn, square):
            points -= piece_value * 0.2

        if BOARD.is_attacked_by(not BOARD.turn, square):
            points += piece_value * 0.2

    return points



def evaluate_space(BOARD):
    space = len(list(BOARD.legal_moves))
    value = (space / (20 + space))

    if BOARD.turn == True:
        return value
    else:
        return -value


def minimax_movement_depth_N_alphabeta_iterative(BOARD, N, alpha, beta):
    opening_move = reader.get(BOARD)

    if opening_move is not None:
        return opening_move.move, alpha, beta, 0
    
    best_move = None
    min_value = float('inf')

    for move in BOARD.legal_moves:
        temp = deepcopy(BOARD)
        temp.push(move)

        evaluate_score = evaluate_board(temp)
        evaluate_score += evaluate_space(temp)    

        if not BOARD.turn:
            if evaluate_score <= alpha:
                return best_move, evaluate_score, beta, evaluate_score
            
            beta = min(beta, evaluate_score)

            if evaluate_score < min_value:
                min_value = evaluate_score
                best_move = move
    
    if N > 1:
        _, _, _, evaluate_score = minimax_movement_depth_N_alphabeta_iterative(temp, N - 1, alpha, beta)
        return best_move, alpha, beta, evaluate_score
    else:
        return best_move, alpha, beta, evaluate_score
        
def minimax_algorithm(BOARD):
    max_depth = 10
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    score = 0

    stockfish = Stockfish(path='Stockfish/stockfish.exe')
    stockfish.set_fen_position(BOARD.fen())
    print("Stockfish move: {}".format(stockfish.get_best_move()))

    for depth in range(1, max_depth + 1):
        current_move, alpha, beta, evaluated_score = minimax_movement_depth_N_alphabeta_iterative(BOARD, depth, alpha, beta)
        if best_move is None or evaluated_score < score:
            best_move = current_move
            score = evaluated_score

    print("Minimax move: {} \tWith the evaluation score of: {}".format(best_move, evaluated_score))
    return best_move


chess_display.chess_engine(chess_display.chess_board, minimax_algorithm, chess.BLACK)

