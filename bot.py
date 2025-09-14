from evaluation import evaluate_position
from position import Position
from schemas import ChessColor, ChessMove
from movegen import generate_moves

"""
Implementation of a chess bot using minimax-algorithm and simple board evaluation
"""

class ChessBot():

    def minimax(self, position: Position, depth: int, maximizing: bool, color: ChessColor, alpha: float, beta: float):
        """
        implementation of the recursive minimax-algorithm
        see https://de.wikipedia.org/wiki/Minimax-Algorithmus for additional information
        """
        try:
            moves = generate_moves(position, color)
        except ValueError:
            print("No King left!")
            return evaluate_position(position)

        # stop recursion
        if depth == 0 or not moves or len(moves) == 0: # no legal moves left or search depth reached
            return evaluate_position(position)
        
        # switch color for recursive call
        next_color = ChessColor.BLACK if color == ChessColor.WHITE else ChessColor.WHITE


        # recursive calls
        # maximizer: search best move for white
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                captured_piece = position.move(move)
                new_eval = self.minimax(position, depth - 1, False, next_color, alpha, beta)
                position.undo_move(move, captured_piece)
                max_eval = max(max_eval, new_eval)
                alpha = max(alpha, new_eval)
                if beta <= alpha:
                    break # beta cutoff
            return max_eval

        # minimizer: search best move for black
        else:
            min_eval = float('inf')
            for move in moves:
                captured_piece = position.move(move)
                new_eval = self.minimax(position, depth - 1, True, next_color, alpha, beta)
                position.undo_move(move, captured_piece)
                min_eval = min(min_eval, new_eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break # alpha cutoff
            return min_eval




    def find_best_move(self, position: Position, depth: int, color: ChessColor) -> ChessMove:
        """
        root search function. calls minimax and returns best found move respective to depth
        """
        # input validation
        MAX_DEPTH = 7
        if not (0 <= depth <= MAX_DEPTH):
            raise ValueError(f"Search depth has to be in range 0 to {MAX_DEPTH}")

        best_eval = float('-inf') if color == ChessColor.WHITE else float('inf')
        next_color = ChessColor.BLACK if color == ChessColor.WHITE else ChessColor.WHITE
        maximizing = True if next_color == ChessColor.WHITE else False
        alpha, beta = float('-inf'), float('inf')

        best_move = None
        moves = generate_moves(position, color)

        for move in moves:
            captured_piece = position.move(move)
            new_eval = self.minimax(position, depth - 1, maximizing, next_color, alpha, beta)
            position.undo_move(move, captured_piece)

            if color == ChessColor.WHITE and new_eval > best_eval:
                best_eval, best_move = new_eval, move
                alpha = max(alpha, new_eval)
            elif color == ChessColor.BLACK and new_eval < best_eval:
                best_eval, best_move = new_eval, move
                beta = min(beta, new_eval)
            print(best_eval)
        return best_move
                

            


