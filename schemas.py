from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod


# Enum for chess pieces
class ChessPieceType(Enum):
    PAWN = "P"
    BISHOP = "B"
    KNIGHT = "N"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"


# Enum for chess colors black and white
class ChessColor(Enum):
    BLACK = 0
    WHITE = 1


# Class for representing a board position
class Coordinate(BaseModel):
    x: int
    y: int



# Parent class
class Piece:
    def __init__(self, piece_type: ChessPieceType):
        self.piece_type = piece_type
        

    # Interface for children classes, since each child moves differently (Pawns, rooks, etc.)
    @abstractmethod
    def move(origin: Coordinate, target: Coordinate, board):
        pass


     
# Child Classes
class Pawn(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.PAWN)

        self.fen_char = "p"
        self.color = color
        self.piece_value = 100 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass


class Bishop(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.BISHOP)

        self.fen_char = "b"
        self.color = color
        self.piece_value = 300 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass


class Knight(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.KNIGHT)

        self.fen_char = "n"
        self.color = color
        self.piece_value = 300 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass


class Rook(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.ROOK)

        self.fen_char = "r"
        self.color = color
        self.piece_value = 500 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass



class Queen(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.PAWN)

        self.fen_char = "q"
        self.color = color
        self.piece_value = 900 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass


class King(Piece):
    def __init__(self, color: ChessColor):
        super().__init__(piece_type = ChessPieceType.PAWN)

        self.fen_char = "k"
        self.color = color
        self.piece_value = 5000 # TODO ADD CONSTANTS TABLE FOR VALUES


    # Moving from x1,y1 to x2,y2 on the board
    def move(origin: Coordinate, target: Coordinate, board):
        pass





