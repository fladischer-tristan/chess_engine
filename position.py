from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessColor, ChessMove, ChessCastling, Coordinate
from utils import long_algebraic_to_move, move_to_long_algebraic, check_bounds
from typing import List
import numpy as np
import time


class Position():
    """
    Represents a chess Position.
    Implements functionality to manipulate the position (move()) and search for moves (find_pseudo_legal_moves() etc.)
    Is compatible with FEN and long-algebraic-notations
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
        self.attacked_fields_black: List[Coordinate]

        self.fen = fen
        # Set board to input fen
        self.fen_to_position(self.fen)

        # When a Pawn double moves, the square in the middle will be stored here (allows simple en passant logic)
        self.en_passant_square: Coordinate | None = None



    ###############################################################################
    # Find out how many squares each Piece "sees" and updates the instance lists.
    # This might be useful to find Pinned pieces, though this function might be
    # removed if it proves useless. Some functionality might be similar to other
    # methods in this class and so, obsolete.                   
    # TODO Currently, the Pawns only check for their northern coordinates (which
    # only white should do). Need to add offset inversion so that black Pawns only 
    # check southern directions and white Pawns only check northern ones
    ###############################################################################

    def update_attacked_fields(self) -> None:
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

        # NOTE might need deepcopy instead of assignment here
        self.attacked_fields_black = attacked_fields_black
        self.attacked_fields_white = attacked_fields_white
        # DEBUG
        print(f"elapsed time in 'update_attacked_fields()': {time.perf_counter() - start}")





    def find_pseudo_legal_moves(self, turn: ChessColor) -> List[ChessMove]:
        """
        Return all pseudo_legal moves in current position
        https://www.chessprogramming.org/Pseudo-Legal_Move

        This will probably end up being a god method, needs to be refactored later
        """

        moves = [] # our List to return

        # get all pieces that match color
        pieces = [piece for row in self.board for piece in row if piece is not None and piece.color == turn]

        # Mainloop where moves should be extracted, checked and appended to List
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                piece = self.board[y][x]
                if piece in pieces:
                    piece_type = piece.fen_char
                    piece_color = piece.color
                    offsets = self.move_directions[piece_type]

                    # PAWNS TODO Needs extra logic for double move, en passant, promotion and color difference (black vs white pawns)
                    if piece_type == 'p':
                        for i, (dx, dy) in enumerate(offsets):
                            # flip direction if color is black (pawns are the only pieces that move differently based on their color)
                            if turn == ChessColor.WHITE:
                                nx = x + dx
                                ny = y + dy
                            else:
                                nx = x - dx
                                ny = y - dy

                            if check_bounds(nx, ny):
                                # Straight moves (No capture)
                                if i == 0: # single move
                                    # Square needs to be empty
                                    if self.board[ny][nx] is None:
                                        # Promotion
                                        if piece_color == ChessColor.WHITE and ny == 0 or piece_color == ChessColor.BLACK and ny == 7:
                                            for promo in ("b", "n", "q", "k"):
                                                moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=self.fen_map[promo],
                                                    )
                                                )
                                        # Regular single move
                                        else:
                                            moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    )
                                                )

                                if i == 1: # double move
                                    # Square needs to be empty
                                    if self.board[ny][nx] is None and ((piece_color == ChessColor.WHITE and y == 6) or (piece_color == ChessColor.BLACK and y == 1)):
                                        moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    )
                                                )

                                # Diagonal moves (capture) # TODO need to handle en passant her
                                elif i in (2, 3):
                                    # Square needs to be taken
                                    if self.board[ny][nx] is not None:
                                        moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    )
                                                )

                                    # en passant
                                    if self.en_passant_square is not None and (nx, ny) == (self.en_passant_square.x, self.en_passant_square.y):
                                        moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    en_passant=True
                                                    )
                                                )


                                
                    # KINGS TODO Needs extra logic for castling (but no check and checkmate validation here yet)
                    elif piece_type == 'k':
                        for dx, dy in offsets:
                            # calculate new square
                            nx = x + dx
                            ny = y + dy

                            if check_bounds(nx, ny):
                                target_piece = self.board[ny][nx]

                                if target_piece is None or target_piece.color != turn:
                                    moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    )
                                                )

                        # CASTLING
                        if not piece.has_moved:
                            # QUEENSIDE
                            q_target = self.board[y][x - 4]
                            
                            if isinstance(q_target, Rook) and q_target.has_moved is False and q_target.color is turn:
                                if all(self.board[y][x - i] is None for i in range(1, 4)):
                                    moves.append(ChessMove(
                                        origin=Coordinate(x=x, y=y),
                                        target=Coordinate(x=x-2, y=y),
                                        color=turn,
                                        promotion=None,
                                        castling=ChessCastling.QUEENSIDE
                                        )
                                    )

                            # KINGSIDE
                            k_target = self.board[y][x + 3]
                            if isinstance(k_target, Rook) and k_target.has_moved is False and k_target.color is turn:
                                if all(self.board[y][x + i] is None for i in range(1, 3)):
                                    moves.append(ChessMove(
                                        origin=Coordinate(x=x, y=y),
                                        target=Coordinate(x=x+2, y=y),
                                        color=turn,
                                        promotion=None,
                                        castling=ChessCastling.KINGSIDE
                                        )
                                    )
                                


                    # KNIGHTS
                    elif piece_type == 'n':
                        for dx, dy in offsets:
                            # calculate new square
                            nx = x + dx
                            ny = y + dy

                            if check_bounds(nx, ny):
                                target_piece = self.board[ny][nx]

                                if target_piece is None or target_piece.color != turn:
                                    moves.append(ChessMove(
                                        origin=Coordinate(x=x, y=y),
                                        target=Coordinate(x=nx, y=ny),
                                        color=turn,
                                        promotion=None
                                        )
                                    )



                    # BISHOPS, ROOKS, QUEENS
                    elif piece_type in ('b', 'r', 'q'):
                        for dx, dy in offsets:
                            # calculate new square
                            nx = x + dx
                            ny = y + dy

                            while check_bounds(nx, ny): # check if square in board
                                target_piece = self.board[ny][nx]
                                if target_piece is None: # square empty
                                    moves.append(ChessMove(
                                        origin=Coordinate(x=x, y=y),
                                        target=Coordinate(x=nx, y=ny),
                                        color=turn,
                                        promotion=None
                                        )
                                    )
                                    # new square:
                                    nx += dx
                                    ny += dy

                                else: # square taken
                                    if target_piece.color != turn:
                                        moves.append(ChessMove(
                                            origin=Coordinate(x=x, y=y),
                                            target=Coordinate(x=nx, y=ny),
                                            color=turn,
                                            promotion=None
                                            )
                                        )
                                    break # end loop because of block

        return moves
                            



    def find_legal_moves(self) -> List[ChessMove]:
        """
        Filter the true legal moves out of our pseudo-legal-ones
        """
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if self.board[y][x] is None:
                    continue
                # PIECE FOUND
                else:
                    pass



    def move(self, move: ChessMove) -> None:
        """
        Play a ChessMove on the board.
        """
        piece = self.board[move.origin.y][move.origin.x]
        fen_char = piece.fen_char
        color = piece.color
        self.board[move.origin.y][move.origin.x] = None
        self.board[move.target.y][move.target.x] = piece
        
        
    



    def fen_to_position(self, fen: str) -> None:
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


if __name__ == '__main__':
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" 
    brd = Position(starting_fen)
    brd.print_board()
    pseudo_moves = brd.find_pseudo_legal_moves(turn=ChessColor.BLACK)
    for move in pseudo_moves:
        mystr = move_to_long_algebraic(move)
        print(f"Computer plays: {mystr}")
        brd.fen_to_position(starting_fen)
        brd.move(move)
        brd.print_board()


    """while True:
        new_move = long_algebraic_to_move(str(input("Please enter a move: ")))
        brd.move(new_move)
        brd.update_attacked_fields()
        brd.print_board()
        print(f"white attacks: {len(brd.attacked_fields_white)} positions")
        print(f"black attacks: {len(brd.attacked_fields_black)} positions")
        brd.find_pseudo_legal_moves(ChessColor.WHITE)"""