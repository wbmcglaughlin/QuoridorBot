import copy
import random

from Quoridor.QuoridorBoard import Tile, QuoridorBoard, Move
from typing import List, Union


class QuoridorBot:
    def __init__(self):
        pass

    def get_move(self, current_board: QuoridorBoard):
        best_move = None
        best_move_score = 0
        current_pos = current_board.player_pos[current_board.turn]
        opposition_pos = current_board.player_pos[(current_board.turn + 1) % len(current_board.player_pos)]
        current_board.get_legal_moves(current_pos)
        current_board.get_legal_tile_squares()

        for ori, tile_move_pos in enumerate(current_board.legal_tile_moves):
            for tile_pos in tile_move_pos:
                test_board = copy.deepcopy(current_board)

                move = Move(Tile(tile_pos, ori), tile_pos)

                test_board.make_move(move)

                distance, path = test_board.get_shortest_path(opposition_pos)

                if len(path) > best_move_score:
                    best_move = move
                    best_move_score = len(path)

        for move_pos in current_board.get_legal_moves(current_pos):
            test_board = copy.deepcopy(current_board)

            move = Move(None, move_pos)

            test_board.make_move(move)

            distance, path = test_board.get_shortest_path(opposition_pos)

            if len(path) > best_move_score:
                best_move = move
                best_move_score = len(path)

        return best_move
