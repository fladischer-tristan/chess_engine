from position import Position
from bot import ChessBot
from schemas import ChessColor
from utils import move_to_long_algebraic

"""
simulating a game between 2 of our bots
"""

pos = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR") # init position via fen for standard chess starting-position
engine_white = ChessBot()
engine_black = ChessBot()

while True:
    white_move = engine_white.find_best_move(pos, 3, ChessColor.WHITE)
    pos.move(white_move)
    print(f"white engine plays: {move_to_long_algebraic(white_move)}")
    black_move = engine_black.find_best_move(pos, 3, ChessColor.BLACK)
    pos.move(black_move)
    print(f"black engine responds: {move_to_long_algebraic(black_move)}")