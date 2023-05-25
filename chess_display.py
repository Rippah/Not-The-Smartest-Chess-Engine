import chess
import pygame
import math


X = 1024
Y = 1024

chess_screen = pygame.display.set_mode((X, Y))
pygame.init()

GREY = (160, 145, 145)
YELLOW = (247, 220, 111)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

chess_board = chess.Board()

chess_pieces = {
                    'p' : pygame.image.load('images/black_pawn.png'),
                    'n' : pygame.image.load('images/black_knight.png'),
                    'b' : pygame.image.load('images/black_bishop.png'),
                    'r' : pygame.image.load('images/black_rook.png'),
                    'q' : pygame.image.load('images/black_queen.png'),
                    'k' : pygame.image.load('images/black_king.png'),
                    'P' : pygame.image.load('images/white_pawn.png'),
                    'N' : pygame.image.load('images/white_knight.png'),
                    'B' : pygame.image.load('images/white_bishop.png'),
                    'R' : pygame.image.load('images/white_rook.png'),
                    'Q' : pygame.image.load('images/white_queen.png'),
                    'K' : pygame.image.load('images/white_king.png')
               }

def update_pieces(chess_screen, chess_board):
    for i in range(64):
        chess_piece = chess_board.piece_at(i)
        if chess_piece == None:
            pass
        else:
            chess_screen.blit(chess_pieces[str(chess_piece)], ((i%8)*128, (1024 - 128) - (i//8)*128))
    for i in range(7):
        i = i+1
        pygame.draw.line(chess_screen, BLACK, (0, i*128), (1024, i*128))
        pygame.draw.line(chess_screen, BLACK, (i*128, 0), (i*128, 1024))
    pygame.display.flip()


def fill_screen(chess_screen):
    for row in range(8):
        for col in range(8):
            x = col * 128
            y = row * 128
            if (row + col) % 2 == 0:
                tile_color = YELLOW
            else:
                tile_color = BROWN

            pygame.draw.rect(chess_screen, tile_color, (x, y, 128, 128))


def change_turn(turn):
    pygame.draw.rect(chess_screen, BLACK, (1024, 0, 1200, Y))
    text_turn = "White's Turn"
    if turn == 1:
        text_turn = "Black's Turn"
    font = pygame.font.Font(None, 24)
    text = font.render(text_turn, True, BROWN)
    text_rect = text.get_rect(center=(X + (1024 - X) // 2, Y // 2))
    chess_screen.blit(text, text_rect)


def chess_1v1(BOARD):
    fill_screen(chess_screen)
    pygame.display.set_caption('Chess Engine')
    pygame.display.flip()
    turn = 0

    index_moves = []
    status = True

    while (status):
        update_pieces(chess_screen,BOARD)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                fill_screen(chess_screen)
                pos = pygame.mouse.get_pos()

                square = (math.floor(pos[0]/128),math.floor(pos[1]/128))
                index = (7-square[1])*8+(square[0])
                
                if index in index_moves: 
                    move = moves[index_moves.index(index)]
                    BOARD.push(move)
                    turn = (turn + 1) % 2

                    index=None
                    index_moves = []
                    
                else:
                    chess_piece = BOARD.piece_at(index)
                    if chess_piece == None:
                        pass
                    else:
                        all_moves = list(BOARD.legal_moves)
                        moves = []
                        for move in all_moves:
                            if move.from_square == index:
                                moves.append(move)
                                tile = move.to_square

                                TileX = 128*(tile%8)
                                TileY = 128*(7-tile//8)

                                pygame.draw.rect(chess_screen, GREY, pygame.Rect(TileX, TileY, 128, 128), 5)
                        
                        index_moves = [a.to_square for a in moves]
     
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)

    pygame.quit()

def chess_engine(BOARD, ai, ai_color):    
    fill_screen(chess_screen)
    pygame.display.set_caption('Chess Engine')
    index_moves = []

    status = True
    while (status):
        update_pieces(chess_screen,BOARD)
        
        if BOARD.turn == ai_color:
            BOARD.push(ai(BOARD))
            fill_screen(chess_screen)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    status = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    fill_screen(chess_screen)
                    pos = pygame.mouse.get_pos()

                    square = (math.floor(pos[0]/128),math.floor(pos[1]/128))
                    index = (7-square[1])*8+(square[0])
                    
                    if index in index_moves: 
                        
                        move = moves[index_moves.index(index)]
                        BOARD.push(move)
                        index=None
                        index_moves = []
                        
                    else:
                        piece = BOARD.piece_at(index)
                        
                        if piece == None:
                            pass
                        else:
                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for move in all_moves:
                                if move.from_square == index:
                                    moves.append(move)

                                    tile = move.to_square
                                    TileX = 128*(tile % 8) + 64
                                    TileY = 128*(7-tile // 8) + 64

                                    pygame.draw.circle(chess_screen, GREY, (TileX, TileY), 15)

                            index_moves = [a.to_square for a in moves]
     
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()