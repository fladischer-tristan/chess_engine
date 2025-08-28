from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessColor, ChessMove, Coordinate
from utils import long_algebraic_to_move
from typing import List
import numpy as np
import time


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
    N, E, S, W = np.array([0, -1]), np.array([1, 0]), np.array([0, 1]), np.array([-1, 0])

    move_directions = {
        "p" : (N, N+E, N+W, N+N),
        "n" : (N+N+E, N+N+W, E+E+N, E+E+S, S+S+E, S+S+W, W+W+N, W+W+S),
        "b" : (N+E, N+W, S+E, S+W),
        "r" : (N, E, S, W),
        "q" : (N, E, S, W, N+E, N+W, S+E, S+W),
        "k" : (N, E, S, W, N+E, N+W, S+E, S+W)
    }

    # Need this extra Dictionary because Pawns are the only pieces
    # that are able to move without attacking (N, N+N). These moves
    # are intentionally left out of here.
    attack_directions = {
        "p" : (N+E, N+W),
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

        # List of all attacked fields
        self.attacked_fields_black: List[Coordinate]
        self.attacked_fields_black: List[Coordinate]

        # Set board to input fen
        self.fen_to_position(fen)




    def update_attacked_fields(self):
        start = time.perf_counter() # DEBUG
        attacked_fields_black: List[Coordinate] = []
        attacked_fields_white: List[Coordinate] = []


        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                piece = self.board[y][x]
                
                if piece == None:
                    continue

                #PIECE FOUND
                else:
                    kind = piece.fen_char.lower()
                    attack_list = (
                        attacked_fields_white if piece.color == ChessColor.WHITE else attacked_fields_black
                    )
                    offsets = self.attack_directions[kind]

                    for dx, dy in offsets:
                        if kind in ("p", "n", "k"): # Pieces with fixed movements
                            new_x, new_y = x + dx, y + dy
                            if 0 <= new_x < 8 and 0 <= new_y < 8:
                                attack_list.append(Coordinate(x=new_x, y=new_y))

                        else: # Sliding Pieces
                            new_x, new_y = x + dx, y + dy

                            # Multiple attacked fields in the same direction
                            while 0 <= new_x < 8 and 0 <= new_y < 8:
                                attack_list.append(Coordinate(x=new_x, y=new_y))
                                if self.board[new_y][new_x] is not None:
                                    break # Piece blocks
                                new_x += dx
                                new_y += dy

        self.attacked_fields_black = attacked_fields_black
        self.attacked_fields_white = attacked_fields_white

        # DEBUG
        print(f"elapsed time in 'update_attacked_fields()': {time.perf_counter() - start}")



    def find_legal_moves(self) -> List[ChessMove]:
        """
        Return all legal moves in current position
        """
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if self.board[y][x] is None:
                    continue
                # PIECE FOUND
                else:
                    pass



    def move(self, move: ChessMove):
        """
        Play a ChessMove and update board.
        """
        fen_char = self.board[move.origin.y][move.origin.x].fen_char
        color = self.board[move.origin.y][move.origin.x].color
        self.board[move.origin.y][move.origin.x] = None
        self.board[move.target.y][move.target.x] = self.fen_map[fen_char](color)
        
        
    



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
        pass


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


if __name__ == '__main__':
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" 
    brd = Position(starting_fen)
    brd.print_board()
    brd.update_attacked_fields()
    print(f"white attacks: {len(brd.attacked_fields_white)} positions")
    print(f"black attacks: {len(brd.attacked_fields_black)} positions")

    while True:
        new_move = long_algebraic_to_move(str(input("Please enter a move: ")))
        brd.move(new_move)
        brd.update_attacked_fields()
        brd.print_board()
        print(f"white attacks: {len(brd.attacked_fields_white)} positions")
        print(f"black attacks: {len(brd.attacked_fields_black)} positions")