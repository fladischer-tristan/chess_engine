from evaluation import evaluate_position
from position import Position
from schemas import ChessColor, ChessMove
from movegen import generate_moves
from validation import compare_positions

"""
Implementation of a chess bot using minimax-algorithm and simple board evaluation
"""

class ChessBot():

    def minimax(self, position: Position, depth: int, maximizing: bool, color: ChessColor):
        """
        implementation of the recursive minimax-algorithm
        see https://de.wikipedia.org/wiki/Minimax-Algorithmus for additional information
        """
        try:
            moves = generate_moves(position, color)
        except ValueError:
            print("NO KING!!!!!!")
            return evaluate_position(position)

        # stop recursion
        if depth == 0 or not moves or len(moves) == 0: # no legal moves left or search depth reached
            return evaluate_position(position)
        
        # switch color for recursive call
        next_color = ChessColor.BLACK if color == ChessColor.WHITE else ChessColor.WHITE


        # recursive calls
        if maximizing:
            max_eval = float('-inf')
            for move in moves:

                #test_pos_1 = position

                captured_piece = position.move(move)
                new_eval = self.minimax(position, depth - 1, False, next_color)
                position.undo_move(move, captured_piece)

                #test_pos_2 = position
                #diffs = compare_positions(test_pos_1, test_pos_2)
                #print(diffs)

                max_eval = max(max_eval, new_eval)
            return max_eval

        else:
            min_eval = float('inf')
            for move in moves:

                #test_pos_1 = position

                captured_piece = position.move(move)
                new_eval = self.minimax(position, depth - 1, True, next_color)
                position.undo_move(move, captured_piece)

                #test_pos_2 = position
                #diffs = compare_positions(test_pos_1, test_pos_2)
                #print(diffs)

                min_eval = min(min_eval, new_eval)
            return min_eval




    def find_best_move(self, position: Position, depth: int, color: ChessColor) -> ChessMove:
        """
        root search function. calls minimax and returns best found move respective to depth
        """
        # input validation
        MAX_DEPTH = 7
        if not (0 <= depth <= MAX_DEPTH):
            raise ValueError(f"Search depth has to be in range 0 to {MAX_DEPTH}")

        moves = generate_moves(position, color) # W
        best_eval = float('-inf') if color == ChessColor.WHITE else float('inf')
        best_move = None
        next_color = ChessColor.BLACK if color == ChessColor.WHITE else ChessColor.WHITE
        maximizing = True if color == ChessColor.WHITE else False

        for move in moves:
            
            #test_pos_1 = position

            captured_piece = position.move(move)
            new_eval = self.minimax(position, depth - 1, maximizing, next_color)
            position.undo_move(move, captured_piece)

            #test_pos_2 = position
            #diffs = compare_positions(test_pos_1, test_pos_2)
            #print(diffs)

            if color == ChessColor.WHITE and new_eval > best_eval:
                best_eval, best_move = new_eval, move
            elif color == ChessColor.BLACK and new_eval < best_eval:
                best_eval, best_move = new_eval, move

        return best_move
                

            


