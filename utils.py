from schemas import ChessMove, Coordinate, ChessColor, PromotionPiece
import re


# Maps Chess Coordinates (A, B, C or 1, 2, 5...) to an index for our board
coordinate_map_x = {
        "a" : 0,
        "b" : 1,
        "c" : 2,
        "d" : 3,
        "e" : 4,
        "f" : 5,
        "g" : 6,
        "h" : 7,
}

coordinate_map_y = {
        1 : 7,
        2 : 6,
        3: 5,
        4 : 4,
        5 : 3,
        6 : 2,
        7 : 1,
        8 : 0,
}


# simply helper func to check if coordinates are in array bound 
def check_bounds(x: int, y: int) -> bool:
       return 0 <= x <= 7 and 0 <= y <= 7



def long_algebraic_to_move(long_alg_move: str) -> ChessMove:
        """
        Convert a string in long algebraic notation to an internal ChessMove

        examples of long-algebraic-notation:
                e2-e4
                h7-h8=Q (Promotion to queen)

        TODO Maybe need to add logic for promoting pieces
        """
        validate_move(long_alg_move) # Throw exception if incorrect

        starting_pos = Coordinate(
                    x=coordinate_map_x[long_alg_move[0]],
                    y=coordinate_map_y[int(long_alg_move[1])]
                )
        target_pos = Coordinate(
                    x=coordinate_map_x[long_alg_move[3]],
                    y=coordinate_map_y[int(long_alg_move[4])]
                )
        
        promotion = None
        # 7 chars means there is a promotion
        if len(long_alg_move) == 7:
                promotion = PromotionPiece(long_alg_move[6])
                
        # Debug purposes - will be removed
        print(f"start: {starting_pos}")
        print(f"target: {target_pos}")
        print(f"promotion: {promotion}")

        return ChessMove(
            origin=starting_pos,
            target=target_pos,
            promotion=promotion
        )




def move_to_long_algebraic(move: ChessMove) -> str:
        """
        Convert internal ChessMove to a string in the long algebraic notation (to display engine moves to the user)
        """

        origin_str_x, origin_str_y, target_str_x, target_str_y = "", "", "", ""

        for key, val in coordinate_map_x.items():
                if val == move.origin.x:
                      origin_str_x = str(key)
                if val == move.target.x:
                      target_str_x = str(key)

        for key, val in coordinate_map_y.items():
                if val == move.origin.y:
                      origin_str_y = str(key)
                if val == move.target.y:
                      target_str_y = str(key)

        
        return f"{origin_str_x}{origin_str_y}-{target_str_x}{target_str_y}"


def validate_move(move: str) -> None:
       MOVE_REGEX = re.compile("^[a-h][1-8][-x][a-h][1-8](?:=[QNBK])?$")
       if not MOVE_REGEX.match(move):
              raise NotationError(f"Incorrect Input: {move}")


class NotationError(Exception):
        """
        Exception related to long-algebraic-notation
        """
        def __init__(self, msg):
            self.msg = msg
            super().__init__(self.msg)


if __name__ == '__main__':
        #long_algebraic_to_move("e2-e4")
        my_chess_move = ChessMove(origin=Coordinate(x=7, y=1), target=Coordinate(x=7, y=3), color=ChessColor.BLACK, promotion=None, castling=None, en_passant=False)
        mystr = move_to_long_algebraic(my_chess_move)
        print(mystr)