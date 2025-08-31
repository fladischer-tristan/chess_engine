import unittest
from utils import long_algebraic_to_move
from schemas import ChessMove, Coordinate

class UtilsTest(unittest.TestCase):

    def test_Long_algebraic_to_move(self):
        test_obj_one = ChessMove(
            origin=Coordinate(x=4, y=7),
            target=Coordinate(x=4, y=4),
            promotion=None
        )
        self.assertEqual(long_algebraic_to_move("e2-e4"), test_obj_one)


if __name__ == '__main__':
    unittest.main()
