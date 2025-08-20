from __future__ import annotations
from enum import Enum
from pydantic import BaseModel

"""
This File hods different Classes that serve as Blueprints, Models or Datastructures for the Engine.
The Focus lies mainly in having consistent and readable code.
"""

class ChessColor(Enum):
    BLACK = 0
    WHITE = 1


class ChessMove(BaseModel):
    piece: Pawn | Knight | Bishop | Rook | Queen | King
    origin: Coordinate
    target: Coordinate


class Coordinate(BaseModel):
    x: int
    y: int

     

###############################################################################
# Each of the following classes represents a Piece.                      
# The usefulness of these will determine wheter they will stay.        
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
        self.checkmated: bool = False