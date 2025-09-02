from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import NamedTuple, Optional

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

    def to_piece(self, color: ChessColor):
        """
        returns a piece object for linked enum
        """
        if self == PromotionPiece.BISHOP:
            return Bishop(color)
        elif self == PromotionPiece.KNIGHT:
            return Knight(color)
        elif self == PromotionPiece.ROOK:
            return Rook(color)
        elif self == PromotionPiece.QUEEN:
            return Queen(color)



class ChessCastling(Enum):
    QUEENSIDE = 0
    KINGSIDE = 1


class Coordinate(NamedTuple):
    x: int
    y: int


class ChessMove(BaseModel):
    origin: Coordinate
    target: Coordinate
    color: ChessColor

    # additional fields to allow special logic (en passant, castling...)
    promotion: Optional[PromotionPiece] = None
    castling: Optional[ChessCastling] = None
    captured_piece: Optional[Pawn | Bishop | Knight | Rook | Queen] = None
    en_passant: bool = False
    double_move: bool = False

    # keep track of latest position details, so the can undo its moves after looking through the search tree
    prev_en_passant_square: Optional[Coordinate] = None
    prev_castling_rights: Optional[dict[ChessColor, dict[str, bool]]] = None

    model_config = {"arbitrary_types_allowed": True} # allow custom data structures (in our example: Pawn, Bishop...)


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