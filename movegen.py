from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessMove, ChessColor, ChessCastling, Coordinate, PromotionPiece
from utils import check_bounds
from position import Position
from typing import List

"""
This File implements functions related to chess-move generation. 
"""


# finds the coordinates of a king (util function)
def find_king(position: Position, color: ChessColor) -> Coordinate:
    for y, row in enumerate(position.board):
        for x, col in enumerate(row):
            piece = position.board[y][x]
            if isinstance(piece, King) and piece.color == color:
                return Coordinate(x=x, y=y)
    raise ValueError("King not found on board!")



# set the instance-variable 'in_check' True for a King, if he is indeed in check
def set_check(position: Position, color: ChessColor) -> None:
    king_pos = find_king(position, color)
    attacked_fields = position.attacked_fields_white if color == ChessColor.BLACK else position.attacked_fields_black # attacked fields

    # check if king is attacked
    check = any(coor == king_pos for coor in attacked_fields)

    position.board[king_pos.y][king_pos.x].in_check = check # set instance variable in_check accordingly


def generate_moves(position: Position, turn: ChessColor) -> List[ChessMove]:
    """
    first calculates pseudo legal moves, then extract true legal moves and return them
    """
    pseudo_legal_moves = get_pseudo_legal_moves(position, turn) # pseudo legal moves
    true_legal_moves = filter_legal_moves(position, turn, pseudo_legal_moves) # true legal moves
    return true_legal_moves


def filter_legal_moves(position: Position, turn: ChessColor, pseudo_legal_moves: List[ChessMove]) -> List[ChessMove]:
    """
    Filter the true legal moves out of our pseudo-legal-ones and return them
    """
    legal_moves = []

    # validate every pseudo_move and only store true legal moves
    for move in pseudo_legal_moves:
        captured_piece = position.move(move) # 1. play pseudo_legal_move
        position.update_attacked_fields()
        set_check(position, turn) # set king in check if he is attacked TODO need to test if this statement breaks anything

        attacked_fields = position.attacked_fields_white if turn == ChessColor.BLACK else position.attacked_fields_black # new attacked fields
        move_valid: bool = False

        # 2. now check if king is under attack
        king_pos = find_king(position, turn)
        move_valid = not position.board[king_pos.y][king_pos.x].in_check

        # extra check for castling
        if move.castling is not None: # castling - need to check squares in between rook and king too
            if move.castling == ChessCastling.KINGSIDE:
                move_valid = all(Coordinate(x=king_pos.x-i, y=king_pos.y) not in attacked_fields for i in (0, 1))
            elif move.castling == ChessCastling.QUEENSIDE:
                move_valid = all(Coordinate(x=king_pos.x-i, y=king_pos.y) not in attacked_fields for i in (0, 1))

        # 3. move is valid if king is not under attack
        if move_valid:
            legal_moves.append(move)
        position.undo_move(move, captured_piece) # 3. reset the played pseudo_legal_move
    return legal_moves
        


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
                                if board[ny][nx] is not None and board[ny][nx].color != turn:
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
                    if position.castling_rights[turn]["queenside"]:
                    # QUEENSIDE
                        if check_bounds(x - 4, y):
                            q_target = board[y][x - 4]
                            
                            if isinstance(q_target, Rook) and q_target.color == turn:
                                if all(board[y][x - i] is None for i in range(1, 4)):
                                    moves.append(ChessMove(
                                        origin=Coordinate(x=x, y=y),
                                        target=Coordinate(x=x-2, y=y),
                                        color=turn,
                                        promotion=None,
                                        castling=ChessCastling.QUEENSIDE
                                        )
                                    )

                    if position.castling_rights[turn]["kingside"]:
                    # KINGSIDE
                        if check_bounds(x + 3, y):
                            k_target = board[y][x + 3]
                            if isinstance(k_target, Rook) and k_target.color == turn:
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