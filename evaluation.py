from position import Position
from schemas import ChessColor
from schemas import King

"""
File holds all logic linked to evaluating a chess position
"""

# defining the static value of a piece
# since kings cannot be captured, they don't have a values
piece_values = {
    "p" : 1.0,
    'n' : 3.0,
    'b' : 3.0,
    'r' : 5.0,
    'q' : 9.0
}

def evaluate_position(position: Position) -> float:
    white_score, black_score, score = 0, 0, 0

    for y, row in enumerate(position.board):
        for x, col in enumerate(row):
            piece = position.board[y][x]

            if piece is not None and not isinstance(piece, King):
                if piece.color == ChessColor.WHITE:
                    white_score += piece_values[piece.fen_char]
                else:
                    black_score -= piece_values[piece.fen_char]

    
    score = black_score + white_score
    return score