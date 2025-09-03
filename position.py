from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessColor, ChessMove, ChessCastling, Coordinate
from utils import check_bounds
from typing import List
import numpy as np
import time
import copy


class Position():
    """
    Represents a chess Position.
    Implements functionality to manipulate the position such as move(), fen_to_position()...
    Is compatible with FEN-Notation and the long-algebraic-notation
    """
    # for mapping fen characters to our objects:
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
        "p" : (N, N+N, N+E, N+W),
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



    def __init__(self, fen: str) -> None:
        # Chess Board
        # A 2D Array. Each element is either None, or a piece Object
        self.board: List[List[None | Pawn | Knight | Bishop | Rook | Queen | King]] = [[None for _ in range(8)] for x in range(8)]

        # List of all current legal moves
        self.legal_moves: List[ChessMove]

        # List of all attacked fields
        self.attacked_fields_black: List[Coordinate]
        self.attacked_fields_white: List[Coordinate]

        self.fen = fen
        # Set starting position 
        self.fen_to_position(self.fen)

        # When a Pawn double moves, the square in the middle will be stored here (allows simple en passant logic)
        self.en_passant_square: Coordinate | None = None

        # dict for storing castling rights
        self.castling_rights = {
            ChessColor.WHITE : {"kingside" : True, 'queenside' : True},
            ChessColor.BLACK : {"kingside" : True, 'queenside' : True}
        }



    ###############################################################################
    # Check how many squares are threatened by both colors. Threatened does not 
    # necessairily mean that there is a piece on that square!
    ###############################################################################

    def update_attacked_fields(self) -> None:
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
                            n_dy = dy
                            if kind == "p" and piece.color == ChessColor.BLACK:
                                n_dy = -dy  # invert pawn direction (for black pawns)

                            new_x, new_y = x + dx, y + n_dy
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



    def move(self, move: ChessMove) -> None | Pawn | Bishop | Knight | Rook | Queen:
        """
        Play a ChessMove on the board, returns captured piece if any
        """

        piece = self.board[move.origin.y][move.origin.x]
        p_type = piece.fen_char
        color = piece.color
        captured_piece = None

        move.prev_en_passant_square = self.en_passant_square
        move.prev_castling_rights = copy.deepcopy(self.castling_rights)

        def regular_move(origin: Coordinate, target: Coordinate):
            n_piece = self.board[origin.y][origin.x]
            self.board[origin.y][origin.x] = None
            self.board[target.y][target.x] = n_piece

        if p_type in ("b", "n", "q", "r"):
            captured_piece = self.board[move.target.y][move.target.x]
            regular_move(move.origin, move.target) 
            if p_type == "r":  
                # set castling rights to false
                if self.castling_rights[color]["kingside"] and move.origin.x == 7:
                    self.castling_rights[color]["kingside"] = False
                elif self.castling_rights[color]["queenside"] and move.origin.x == 0:
                    self.castling_rights[color]["queenside"] = False

        elif p_type == "p":
            if not move.en_passant:
                captured_piece = self.board[move.target.y][move.target.x]

            # Double Move - set en passant square
            if move.double_move:
                self.en_passant_square = Coordinate(x=move.target.x, y=move.target.y+1) if color == ChessColor.WHITE else Coordinate(x=move.target.x, y=move.target.y-1)
                regular_move(move.origin, move.target)
            else:
                self.en_passant_square = None # RESET last en passant square
                regular_move(move.origin, move.target)

            # Promotion
            if move.promotion is not None:
                self.board[move.target.y][move.target.x] = move.promotion.to_piece(color)

            # En Passant
            if move.en_passant:
                cap_y = move.target.y + 1 if color == ChessColor.WHITE else move.target.y - 1
                captured_piece = self.board[cap_y][move.target.x]
                self.board[cap_y][move.target.x] = None

        elif p_type == "k":
            if move.castling is not None:
                captured_piece = self.board[move.target.y][move.target.x]
                regular_move(move.origin, move.target)
                rk_move: ChessMove
                if move.castling == ChessCastling.KINGSIDE:
                    # rook-kingside moves as well:
                    rk_move = ChessMove(
                        origin=Coordinate(x=move.origin.x+3, y=move.origin.y),
                        target=Coordinate(x=move.origin.x+1, y=move.origin.y),
                        color=color
                    )
                else:
                    # rook-queenside moves as well:
                    rk_move = ChessMove(
                        origin=Coordinate(x=move.origin.x-4, y=move.origin.y),
                        target=Coordinate(x=move.origin.x-1, y=move.origin.y),
                        color=color
                    )
                # finally, move rook over king
                regular_move(rk_move.origin, rk_move.target)
            else:
            # no castling:
                captured_piece = self.board[move.target.y][move.target.x]
                regular_move(move.origin, move.target)
            self.castling_rights[color]["kingside"], self.castling_rights[color]["queenside"] = False, False # disable castling rights
        return captured_piece




    def undo_move(self, move: ChessMove, captured_piece: None | Pawn | Bishop | Knight | Rook | Queen) -> None:
        """
        Undoes a move. Needed for in-place search algorithm. Otherwise we would need thousands of position objects. 
        """
        color = move.color

        # restore states
        self.en_passant_square = move.prev_en_passant_square
        self.castling_rights = move.prev_castling_rights

        # Captured piece:
        if captured_piece is not None:
            self.board[move.origin.y][move.origin.x] = self.board[move.target.y][move.target.x]

            # Promotion
            if move.promotion is not None:
                self.board[move.origin.y][move.origin.x] = Pawn(color) # restore promoted piece back to Pawn
            
            # no en passant: restore captured piece at target square
            if not move.en_passant:
                self.board[move.target.y][move.target.x] = captured_piece
            # en passant: restore captured Pawn at correct sqaure, clean up target Square
            else:
                y_cap = move.target.y + 1 if color == ChessColor.WHITE else move.target.y -1 # y coor lost pawn
                self.board[y_cap][move.target.x] = captured_piece
                self.board[move.target.y][move.target.x] = None  # clear target square

        # No captured piece:
        else:
            # castling
            if move.castling is not None:
                x_pos_rook = move.target.x + 1 if move.castling == ChessCastling.QUEENSIDE else move.target.x - 1
                origin_x_rook = 0 if move.castling == ChessCastling.QUEENSIDE else 7

                # revert king move
                self.board[move.origin.y][move.origin.x] = self.board[move.target.y][move.target.x]
                self.board[move.target.y][move.target.x] = None

                # revert rook move
                self.board[move.target.y][origin_x_rook] = self.board[move.target.y][x_pos_rook]
                self.board[move.target.y][x_pos_rook] = None

            else:
            # no castling - regular move
                self.board[move.origin.y][move.origin.x] = self.board[move.target.y][move.target.x]
                self.board[move.target.y][move.target.x] = None
            

        
        
    def fen_to_position(self, fen: str) -> None:
        """
        Translates a FEN into a chess position on the internal board.
        https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation

        TODO currently, only the board arrangements work. We also need to add the other 5 FEN fields (e.g. castling rights, turn_color...)

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


    def position_to_fen(self) -> str:
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