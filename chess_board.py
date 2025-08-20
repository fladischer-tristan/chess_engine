from schemas import Pawn, Bishop, Knight, Rook, Queen, King
from schemas import ChessPieceType, ChessColor


class Board():

    # fen dictionary
    fen_keys = {
        "p": Pawn,
        "b": Bishop,
        "n": Knight,
        "r": Rook,
        "q": Queen,
        "k": King
    }

    # Chess starting position represented as FEN
    # https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation

    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" 


    def __init__(self):
        # Chess Board
        # A 2D Array. Each element is either None, or holds a piece Object
        self.board = [[None for _ in range(8)] for x in range(8)]



    def fen_parser(self, fen: str):
        """
        Convert a FEN into a chess position using our board.
        """
        row_index, col_index = 0, 0
        iteration = 0

        for char in fen:
            iteration += 1

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
            if char.lower() in self.fen_keys:
                piece_class = self.fen_keys[char.lower()]
                color = ChessColor.WHITE if char.isupper() else ChessColor.BLACK
                self.board[row_index][col_index] = piece_class(color)
                col_index += 1




    def print_board(self):
        """
        Prints the current board to terminal.
        """
        counter = 0
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if counter % 8 == 0:
                    print()

                if self.board[y][x] == None:
                    print(".", end=" ")    

                else: 
                    for key, value in self.fen_keys.items():
                        if self.board[y][x].fen_char == key:
                            if self.board[y][x].color == ChessColor.WHITE:
                                print(key.upper(), end=" ")
                                break
                            else:
                                print(key.lower(), end=" ")
                                break

                counter = counter + 1
                
                



brd = Board()
brd.fen_parser(brd.starting_fen)
brd.print_board()