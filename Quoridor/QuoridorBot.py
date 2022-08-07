import copy

from Quoridor.QuoridorBoard import QuoridorBoard, Move


class QuoridorBot:
    def __init__(self):
        self.weight = 0

    def get_move(self, current_board: QuoridorBoard):
        best_move = None
        best_move_score = self.weight
        current_pos = current_board.player_pos[current_board.turn]
        opposition_pos = current_board.player_pos[(current_board.turn + 1) % len(current_board.player_pos)]

        if current_board.player_tiles[current_board.turn] > 0:
            for ori, tile_move_pos in enumerate(current_board.legal_tile_moves):
                for tile_pos in tile_move_pos:
                    test_board = copy.deepcopy(current_board)

                    move = Move(1, tile_pos, ori)

                    test_board.make_move(move)

                    distance, path = test_board.get_shortest_path(opposition_pos)

                    if len(path) > best_move_score:
                        best_move = move
                        best_move_score = len(path)

        for move_pos in current_board.get_legal_moves(current_pos):
            test_board = copy.deepcopy(current_board)

            move = Move(0, move_pos)

            test_board.make_move(move)

            distance, path = test_board.get_shortest_path(opposition_pos)

            if len(path) > best_move_score:
                best_move = move
                best_move_score = len(path)

        return best_move
