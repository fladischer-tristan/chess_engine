from schemas import ChessMove, Coordinate, ChessColor, PromotionPiece


# Maps Vertical Chess Coordinates (A, B, C...) to an index for our board
coordinate_map = {
        "a" : 0,
        "b" : 1,
        "c" : 2,
        "d" : 3,
        "e" : 4,
        "f" : 5,
        "g" : 6,
        "h" : 7,
}





def long_algebraic_to_move(long_alg_move: str) -> ChessMove:
        """
        Convert a string in long algebraic notation to an internal ChessMove

        examples of long-algebraic-notation:
        * e2-e4
        * h7-h8=Q (Promotion to queen)
        """
        
        if len(long_alg_move) < 5 or len(long_alg_move) > 7:
                raise NotationError("Algebraic move must be between 5 and 7 characters long.")
        
        if ('-') not in long_alg_move:
               raise NotationError("Algebraic move must contain '-'.")
        
        if not long_alg_move[1].isdigit() or not long_alg_move[4].isdigit():
               raise NotationError("Algebraic move must contain numbers at index 1 and 4.")
        

        starting_pos = Coordinate(
                    x=coordinate_map[long_alg_move[0]],
                    y=int(long_alg_move[1]) - 1
                )
        
        target_pos = Coordinate(
                    x=coordinate_map[long_alg_move[3]],
                    y=int(long_alg_move[4]) - 1
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

                

class NotationError(Exception):
        def __init__(self, msg):
            self.msg = msg
            super().__init__(self.msg)


def move_to_long_algebraic(move: ChessMove) -> str:
        """
        Convert internal ChessMove to a string in the long algebraic notation
        """
        pass




if __name__ == '__main__':
        long_algebraic_to_move("e2-e4")