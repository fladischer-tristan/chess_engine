from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessPieceType, ChessColor


class Board():


    # fen char dictionary
    fen_keys = {
        "PAWN" : "b",
        "BISHOP" : "l",
        "KNIGHT" : "s",
        "ROOK" : "t",
        "QUEEN" : "f",
        "KING" : "k"
    }

    # Chess starting position represented as FEN
    # https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation

    starting_fen = "tslfklst/bbbbbbbbbb/8/8/8/8/BBBBBBBBBB/TSLDKLST"



    def __init__(self):
        # Initialize chess board
        self.board = [[None for _ in range(8)] for x in range(8)]


    # Update the board using a fen as input
    def fen_parser(self, fen: str):
        row_index, col_index = 0, 0


        for char in fen:
            char_is_lower = True if char.islower() else False
            print(char_is_lower)


            # Integer found - skip n fields (set board tile to none)
            try: 
                num = int(char)
                for i in range(num):
                    print(i)
                    self.board[row_index][col_index + i] = None
            except ValueError:
                pass


            # "/" found (new line)
            if char == "/":
                row_index += 1
                col_index = 0
                print(char)

            # Piece found - Set board tile to piece type
            else:
                for key, value in self.fen_keys.items():
                    if char.lower() == value or char.lower() == "d":
                        print(f"FOUND: {key} : {value}")

                        if value == "b":
                            piece = Pawn(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)
                        elif value == "l":
                            piece = Bishop(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)
                        elif value == "s":
                            piece = Knight(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)
                        elif value == "t":
                            piece = Rook(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)
                        elif value == "f" or char.lower() == "d":
                            piece = Queen(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)
                        elif value == "k":
                            piece = King(ChessColor.WHITE if char_is_lower else ChessColor.BLACK)

                        # SET PIECE
                        self.board[row_index][col_index] = piece

                        if col_index < 7:
                            col_index += 1


brd = Board()

brd.fen_parser(brd.starting_fen)
print(brd.board)