from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessMove, ChessColor, ChessCastling, Coordinate, PromotionPiece
from utils import check_bounds
from position import Position
from typing import List

"""
This File implements functions related to chess-move generation. 
"""

def filter_legal_moves(self, position: Position, pseudo_legal_moves: List[ChessMove]) -> List[ChessMove]:
        """
        Filter the true legal moves out of our pseudo-legal-ones and return them
        """
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if self.board[y][x] is None:
                    continue
                # PIECE FOUND
                else:
                    pass



def get_pseudo_legal_moves(position: Position, turn: ChessColor) -> List[ChessMove]:
        """
        Return all pseudo_legal moves in current position
        https://www.chessprogramming.org/Pseudo-Legal_Move

        TODO God method, needs to be refactored eventually
        """

        board = position.board
        moves = [] # our List to return

        # get all pieces that match color
        pieces = [piece for row in board for piece in row if piece is not None and piece.color == turn]

        # Mainloop where moves should be extracted, checked and appended to List
        for y, row in enumerate(board):
            for x, col in enumerate(row):
                piece = board[y][x]
                if piece in pieces:
                    piece_type = piece.fen_char
                    piece_color = piece.color
                    offsets = position.move_directions[piece_type]

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
                                    if board[ny][nx] is None:
                                        # Promotion
                                        if piece_color == ChessColor.WHITE and ny == 0 or piece_color == ChessColor.BLACK and ny == 7:
                                            for prom in PromotionPiece:
                                                moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=prom
                                                    )
                                                )
                                        # Regular single move
                                        else:
                                            moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None
                                                    )
                                                )

                                if i == 1: # double move
                                    # Square needs to be empty
                                    if board[ny][nx] is None and ((piece_color == ChessColor.WHITE and y == 6) or (piece_color == ChessColor.BLACK and y == 1)):
                                        moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None,
                                                    double_move=True
                                                    )
                                                )

                                # Diagonal moves (capture) # TODO need to handle en passant her
                                elif i in (2, 3):
                                    # Square needs to be taken
                                    if board[ny][nx] is not None:
                                        moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None
                                                    )
                                                )

                                    # en passant
                                    if position.en_passant_square is not None and (nx, ny) == (position.en_passant_square.x, position.en_passant_square.y):
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
                                target_piece = board[ny][nx]

                                if target_piece is None or target_piece.color != turn:
                                    moves.append(ChessMove(
                                                    origin=Coordinate(x=x, y=y),
                                                    target=Coordinate(x=nx, y=ny),
                                                    color=turn,
                                                    promotion=None
                                                    )
                                                )

                        # CASTLING
                        if not piece.has_moved:
                            # QUEENSIDE
                            if check_bounds(x - 4, y):
                                q_target = board[y][x - 4]
                                
                                if isinstance(q_target, Rook) and q_target.has_moved == False and q_target.color == turn:
                                    if all(board[y][x - i] is None for i in range(1, 4)):
                                        moves.append(ChessMove(
                                            origin=Coordinate(x=x, y=y),
                                            target=Coordinate(x=x-2, y=y),
                                            color=turn,
                                            promotion=None,
                                            castling=ChessCastling.QUEENSIDE
                                            )
                                        )

                            # KINGSIDE
                            if check_bounds(x + 3, y):
                                k_target = board[y][x + 3]
                                if isinstance(k_target, Rook) and k_target.has_moved == False and k_target.color == turn:
                                    if all(board[y][x + i] is None for i in range(1, 3)):
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
                                target_piece = board[ny][nx]

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
                                target_piece = board[ny][nx]
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