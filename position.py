from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessColor, ChessMove, Coordinate
from typing import List, NamedTuple


class Position():
    """
    Represents a chess Position.
    """
    
    # fen dictionary to map fen keys to our Piece Objects
    fen_map = {
        "p": Pawn,
        "b": Bishop,
        "n": Knight,
        "r": Rook,
        "q": Queen,
        "k": King
    }

    # Move directions/offsets for every piece
    N, E, S, W = (0, -1), (1, 0), (0, 1), (-1, 0)

    directions = {
        "p" : (N, N+E, N+W, N+N),
        "n" : (N+N+E, N+N+W, E+E+N, E+E+S, S+S+E, S+S+W, W+W+N, W+W+S),
        "b" : (N+E, N+W, S+E, S+W),
        "r" : (N, E, S, W),
        "q" : (N, E, S, W, N+E, N+W, S+E, S+W),
        "k" : (N, E, S, W, N+E, N+W, S+E, S+W)
    }


    def __init__(self, fen: str):
        # Chess Board
        # A 2D Array. Each element is either None, or a piece Object
        self.board: List[List[None | Pawn | Knight | Bishop | Rook | Queen | King]] = [[None for _ in range(8)] for x in range(8)]

        # List of all current legal moves
        self.legal_moves: List[ChessMove]

        # Set board to input fen
        self.fen_to_position(fen)


    def move(self, algebraic_move: str, color: ChessColor) -> ChessMove:
        """
        Translates the input string (in the format of the algebraic-notation) into a move on the internal board.
        """
        #TODO
        raise NotImplementedError



    def find_legal_moves(self) -> List[ChessMove]:
        """
        Return all legal moves in current position
        """
        for y, row in enumerate(self.board):
            for x, col in enumerate(self.board):
                raise NotImplementedError


    def fen_to_position(self, fen: str):
        """
        Translates a FEN into a chess position on the internal board.
        https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation

        """
        row_index, col_index = 0, 0

        for char in fen:
            # Integer
            if char.isdigit():
                num = int(char)
                for i in range(num):
                    self.board[row_index][col_index] = None
                    col_index += 1
                continue

            # Slash
            if char == "/":
                row_index += 1
                col_index = 0
                continue

            # Letter
            if char.lower() in self.fen_map:
                piece_class = self.fen_map[char.lower()]
                color = ChessColor.WHITE if char.isupper() else ChessColor.BLACK
                self.board[row_index][col_index] = piece_class(color)
                col_index += 1


    def position_to_fen():
        """
        Generates fen based on current position
        """
        # TODO
        raise NotImplementedError


    def print_board(self):
        """
        Prints the current position to terminal.
        """
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                # Print new line after 8th char
                if x % 8 == 0:
                    print()

                # Print . for empty field
                if self.board[y][x] == None:
                    print(".", end=" ")    

                # Print fen character for a taken field
                else: 
                    for key, value in self.fen_map.items():
                        if self.board[y][x].fen_char == key:
                            if self.board[y][x].color == ChessColor.WHITE:
                                print(key.upper(), end=" ")
                                break
                            else:
                                print(key.lower(), end=" ")
                                break
    
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" 
brd = Position(starting_fen)
brd.print_board()