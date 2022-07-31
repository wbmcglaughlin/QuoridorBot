from Quoridor.QuoridorBoard import Tile, QuoridorBoard, Move
from typing import List, Union


class QuoridorBot:
    def __init__(self):
        pass

    def get_move(self, current_board: QuoridorBoard):
        legal_tile_moves = current_board.get_legal_tile_squares()

        return Move(Tile(11, 1), 10)
