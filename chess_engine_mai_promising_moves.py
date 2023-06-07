import chess
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
center_box_value = 10

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

    
def evaluate_center_control(BOARD):
    center_control = 0
    for square in center_squares:
        piece = BOARD.piece_at(square)
        if piece is not None:
            if piece.color == BOARD.turn:
                center_control += center_value
            else:
                center_control -= center_value
    
    for square in center_box:
        piece = BOARD.piece_at(square)
        if piece is not None:
            if piece.color == BOARD.turn:
                center_control += center_box_value
            else:
                center_control -= center_box_value

    return center_control


def evaluate_piece_safety(BOARD, piece, position):
    threats = BOARD.attackers(not BOARD.turn, position)
    threat_value = 0

    if threats:
        escape_moves = [move for move in BOARD.legal_moves if move.to_square not in threats]
        if escape_moves:
            return 0

        threat_value -= point_values[str(piece)]

        for move in BOARD.legal_moves:
            if move.from_square == position and move.to_square in threats:
                attacked_piece = BOARD.piece_at(move.to_square)
                if attacked_piece is not None:
                    threat_value -= 2 * point_values[str(attacked_piece)]
                    if point_values[str(attacked_piece)] >= point_values[str(piece)]:
                        threat_value -= 5 * point_values[str(attacked_piece)]
                    return threat_value

    return 0


def evaluate_piece_mobility(BOARD):
    mobility_points = 0
    for square in BOARD.piece_map():
        if BOARD.piece_at(square).color == BOARD.turn:
            mobility_points += len(list(BOARD.generate_legal_moves(square)))
    return mobility_points


def evaluate_position(BOARD):
    total_evaluation = 0

    for row in range(8):
        for col in range(8):
            piece = BOARD.piece_at(row*8 + col)

            if piece != '.':
                piece_value = 0
                if piece is not None:
                    piece_value = point_values[str(piece)]
                
                if piece == 'p':
                    position_value = pawn_table_white[row * 8 + col]
                elif piece == 'n':
                    position_value = knight_table_white[row * 8 + col]
                elif piece == 'b':
                    position_value = bishop_table_white[row * 8 + col]
                elif piece == 'r':
                    position_value = rook_table_white[row * 8 + col]
                elif piece == 'q':
                    position_value = queen_table_white[row * 8 + col]
                elif piece == 'k':
                    if 'Q' not in ''.join(BOARD): 
                        position_value = king_table_end_game[row * 8 + col]
                    else:
                        position_value = king_table_white[row * 8 + col]
                elif piece == 'P':
                    position_value = pawn_table_black[row * 8 + col]
                elif piece == 'N':
                    position_value = knight_table_black[row * 8 + col]
                elif piece == 'B':
                    position_value = bishop_table_black[row * 8 + col]
                elif piece == 'R':
                    position_value = rook_table_black[row * 8 + col]
                elif piece == 'Q':
                    position_value = queen_table_black[row * 8 + col]
                elif piece == 'K':
                    if 'q' not in ''.join(BOARD): 
                        position_value = king_table_end_game[row * 8 + col]
                    else:
                        position_value = king_table_black[row * 8 + col]
                else:
                    position_value = 0

                total_evaluation += piece_value * position_value * 0.01

    return total_evaluation


def min_max_movement_depth_N_alphabeta_iterative(BOARD, N, alpha, beta):
    opening_move = reader.get(BOARD)

    if opening_move is not None:
        return opening_move.move, alpha, beta
    if N == 0:
        return random_movement(BOARD), alpha, beta

    best_move = None
    min_value = float('inf')
    max_value = float('-inf')

    for move in BOARD.legal_moves:
        temp = deepcopy(BOARD)
        temp.push(move)

        evaluate_score = evaluate_board(temp)
        evaluate_score += evaluate_space(temp)
        evaluate_score += evaluate_center_control(temp)
        evaluate_score += evaluate_piece_safety(temp, BOARD.piece_at(move.from_square), move.from_square)
        evaluate_score += evaluate_piece_mobility(temp)
        evaluate_score += evaluate_position(temp)

        if BOARD.turn:
            if evaluate_score >= beta:
                return best_move, alpha, beta

            alpha = max(alpha, evaluate_score)
            
            if evaluate_score > max_value:
                max_value = evaluate_score
                best_move = move
        else:
            if evaluate_score <= alpha:
                return best_move, alpha, beta

            beta = min(beta, evaluate_score)

            if evaluate_score < min_value:
                min_value = evaluate_score
                best_move = move


    return best_move, alpha, beta

def min_max_algorithm(BOARD):
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for depth in range(1, 20):
        current_move, alpha, beta = min_max_movement_depth_N_alphabeta_iterative(BOARD, depth, alpha, beta)
        if current_move is not None:
            best_move = current_move

    return best_move

chess_display.chess_engine(chess_display.chess_board, min_max_algorithm, chess.BLACK)
