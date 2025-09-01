from movegen import get_pseudo_legal_moves
from position import Position
from schemas import ChessColor

"""
For now, this file is used for testing. Later it will be our entry point.

Right now the file just initializes the board, passes a fen and gets all pseudo legal moves. then those moves are played individually and displayed in terminal.
"""

if __name__ == '__main__':
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" # fen for standard chess starting position
    prom_fen = "QQQQQQQQ/QQQQQQQQ/QQQQQQQQ/QQQQQQQQ/QQQQQQQQ/QQQQQQQQ/QQQQQQQQ/QQQQQQQQ"
    pos = Position(prom_fen)
    pos.print_board()
    print("_---------------------------_")

    # get all pseudo legal moves in our current position
    pseudo_moves = get_pseudo_legal_moves(pos, ChessColor.WHITE)

    print(len(pseudo_moves))
    for move in pseudo_moves:
        pos.move(move) # play the move
        pos.print_board() # display in terminal
        pos.fen_to_position(prom_fen) # reset position
        print('\n\n' + ('#' * 50)) 