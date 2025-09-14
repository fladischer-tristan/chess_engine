from position import Position
from schemas import ChessColor
from schemas import King

"""
File holds all logic linked to evaluating a chess position
"""

# defining the static value of a piece
# since kings cannot be captured, they don't have values
piece_values = {
    "p" : 100.0,
    'n' : 300.0,
    'b' : 300.0,
    'r' : 500.0,
    'q' : 900.0
}

# position-square-tables - bonus scores for well positioned pieces, negative bonus for badly positioned pieces
pst = {
    "p" : [
        [0,0,0,0,0,0,0,0],
        [5,5,5,-5,-5,5,5,5],
        [1,1,2,3,3,2,1,1],
        [0.5,0.5,1,2.5,2.5,1,0.5,0.5],
        [0,0,0,10,10,0,0,0],
        [0.5,-0.5,-1,0,0,-1,-0.5,0.5],
        [0.5,1,1,-2,-2,1,1,0.5],
        [0,0,0,0,0,0,0,0]
    ],

    "n" : [
        [-5,-4,-3,-3,-3,-3,-4,-5],
        [-4,-2, 0, 0, 0, 0,-2,-4],
        [-3, 0, 1, 1.5, 1.5, 1, 0,-3],
        [-3, 0.5,1.5,2, 2, 1.5,0.5,-3],
        [-3, 0, 1.5,2, 2, 1.5, 0,-3],
        [-3, 0.5,1,1.5,1.5,1,0.5,-3],
        [-4,-2, 0,0.5,0.5,0,-2,-4],
        [-5,-4,-3,-3,-3,-3,-4,-5]
    ],

    "b" : [
        [-2,-1,-1,-1,-1,-1,-1,-2],
        [-1, 0, 0, 0, 0, 0, 0,-1],
        [-1, 0, 0.5,1,1,0.5,0,-1],
        [-1,0.5,0.5,1,1,0.5,0.5,-1],
        [-1,0,1,1,1,1,0,-1],
        [-1,1,1,1,1,1,1,-1],
        [-1,0.5,0,0,0,0,0.5,-1],
        [-2,-1,-1,-1,-1,-1,-1,-2]
    ],

    "r" : [
        [0,0,0,0,0,0,0,0],
        [0.5,1,1,1,1,1,1,0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [-0.5,0,0,0,0,0,0,-0.5],
        [0,0,0,0.5,0.5,0,0,0]
    ],

    "q" : [
        [-2,-1,-1,-0.5,-0.5,-1,-1,-2],
        [-1,0,0,0,0,0,0,-1],
        [-1,0,0.5,0.5,0.5,0.5,0,-1],
        [-0.5,0,0.5,0.5,0.5,0.5,0,-0.5],
        [0,0,0.5,0.5,0.5,0.5,0, -0.5],
        [-1,0.5,0.5,0.5,0.5,0.5,0,-1],
        [-1,0,0.5,0,0,0,0,-1],
        [-2,-1,-1,-0.5,-0.5,-1,-1,-2]
    ],

    "k" : [
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-3,-4,-4,-5,-5,-4,-4,-3],
        [-2,-3,-3,-4,-4,-3,-3,-2],
        [-1,-2,-2,-2,-2,-2,-2,-1],
        [2,2,0,0,0,0,2,2],
        [2,3,1,0,0,1,3,2]
    ]
}

def evaluate_position(position: Position) -> float:
    white_score, black_score, score = 0, 0, 0

    for y, row in enumerate(position.board):
        for x, col in enumerate(row):
            piece = position.board[y][x]

            # Material scores
            if piece is None:
                continue
            
            if isinstance(piece, King):
                continue

            p_type = piece.fen_char
            color = piece.color
        
            if piece.color == ChessColor.WHITE:
                white_score += piece_values[piece.fen_char]
            else:
                black_score += piece_values[piece.fen_char]

            # Positional scores
            if color == ChessColor.WHITE:
                white_score += pst[p_type][y][x]
            else:
                black_score += pst[p_type][7-y][x]

            # mobility scores
            attacked_squares_black = len(position.attacked_fields_black)
            attacked_squares_white = len(position.attacked_fields_white)

            black_score += attacked_squares_black
            white_score += attacked_squares_white
    
    score = -black_score + white_score
    return score