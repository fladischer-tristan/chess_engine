from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import NamedTuple

"""
This File declares different Classes that serve as Blueprints, Models or Datastructures for the Engine.
NO LOGIC in this file. Focus is on clean and somewhat modular code
"""

class ChessColor(Enum):
    BLACK = 0
    WHITE = 1


class PromotionPiece(Enum):
    BISHOP = "B"
    KNIGHT ="N"
    ROOK = "R"
    QUEEN = "Q"


class ChessCastling(Enum):
    QUEENSIDE = 0
    KINGSIDE = 1


class ChessMove(BaseModel):
    origin: Coordinate
    target: Coordinate
    color: ChessColor
    promotion: None | PromotionPiece = None
    castling: None | ChessCastling = None
    en_passant: bool = False


class Coordinate(NamedTuple):
    x: int
    y: int

     

###############################################################################
# Each of the following classes represents a Piece.                      
# NOTE: Some attributes might not be useful. Might get refactored     
###############################################################################


class Pawn():
    def __init__(self, color: ChessColor):
        self.fen_char: str = "p"
        self.color: ChessColor = color
        self.piece_value: int = 100 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False



class Bishop():
    def __init__(self, color: ChessColor):
        self.fen_char = "b"
        self.color = color
        self.piece_value = 300 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False



class Knight():
    def __init__(self, color: ChessColor):
        self.fen_char: str = "n"
        self.color: ChessColor = color
        self.piece_value: int = 300 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False



class Rook():
    def __init__(self, color: ChessColor):
        self.fen_char: str = "r"
        self.color: ChessColor = color
        self.piece_value: int = 500 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False
        self.has_moved: bool = False



class Queen():
    def __init__(self, color: ChessColor):
        self.fen_char: str = "q"
        self.color: ChessColor = color
        self.piece_value: int = 900 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False



class King():
    def __init__(self, color: ChessColor):
        self.fen_char: str = "k"
        self.color: ChessColor = color
        self.piece_value: int = 5000 # TODO ADD CONSTANTS TABLE FOR VALUES
        self.pinned: bool = False
        self.in_check: bool = False
        self.has_moved: bool = False