from movegen import get_pseudo_legal_moves, filter_legal_moves
from position import Position
from schemas import ChessColor

"""
For now, this file is used for testing. Later it will be our entry point.

Right now the file just initializes the board, passes a fen and gets all pseudo legal moves. then those moves are played individually and displayed in terminal.
"""

if __name__ == '__main__':
    #fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" # fen for standard chess starting position
    fen = "r1bq1rk1/ppp2ppp/2n2n2/3pp3/3PP3/2N2N2/PPP2PPP/R1BQ1RK1"
    
    pos = Position(fen)
    turn = ChessColor.WHITE

    moves = get_pseudo_legal_moves(pos, turn)

    correct_checks = 0
    failed_checks = 0

    for move in moves:
            origin_piece_old = pos.board[move.origin.y][move.origin.x]
            target_piece_old = pos.board[move.target.y][move.target.x]

            print("old board:")
            pos.print_board()

            captured_piece = pos.move(move)

            print("board after move():")
            pos.print_board()

            pos.undo_move(move, captured_piece)

            origin_piece_new = pos.board[move.origin.y][move.origin.x]
            target_piece_new = pos.board[move.target.y][move.target.x]

            print("board after undo_move():")
            pos.print_board()

            if origin_piece_new == origin_piece_old and target_piece_new == target_piece_old:
                print("Success!")
                correct_checks += 1
            else:
                print("Failed!. " \
                    f"old target: {target_piece_old}, new target: {target_piece_new}" \
                    f"old origin: {origin_piece_old}, new origin: {origin_piece_new}"
                )
                correct_checks += 1
            
            print(("#" * 100), \
                "#" * 100)
            
    print(f"correct checks: {correct_checks}, failed checks: {failed_checks}")
