from evaluation import evaluate_position
from position import Position
from schemas import ChessColor
from movegen import generate_moves

"""
Implementation of a chess bot using minimax-algorithm and simple board evaluation
"""

class ChessBot():
    def __init__(self, depth: int):
        self.depth = depth
    
    def minimax(position: Position, depth: int, color: ChessColor):
        """
        implementation of the recursive minimax-algorithm
        see https://de.wikipedia.org/wiki/Minimax-Algorithmus for additional information
        """
        
        moves = generate_moves(position, color)

        # here logic for search functions (min and max)


    def min(pos: Position, color: ChessColor, depth: int):
        max_score = 9999999999 # will get replaced by math.inf eventually




    def max(pos: Position, color: ChessColor, depth: int):
        min_score = -9999999999 # will get replaced by -math.inf eventually

