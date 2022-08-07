import copy

from raylibpy import *
from typing import List, Union


class Move:
    def __init__(self, move_type, pos, ori=None):
        self.is_tile: int = move_type
        self.pos: int = pos
        self.ori: Union[int, None] = ori


class Tile:
    def __init__(self, rec_index, orientation):
        """

        :param rec_index: tile rectangle index
        :param orientation: tile orientation
        """
        self.rec_index = rec_index
        self.orientation = orientation


class QuoridorBoard:
    def __init__(self, side_squares, turn, total_tiles, players):
        self.side_squares = side_squares
        self.tile_count = total_tiles

        self.turn = turn

        self.player_pos: List[int] = []
        self.player_col: List[Color] = []
        self.player_tiles: List[int] = [int(total_tiles / players)] * players
        self.board_tiles: List[Tile] = []

        self.has_legal_tile_moves: bool = False
        self.legal_tile_moves: List[List[int]] = []

        self.has_legal_player_moves: bool = False
        self.player_legal_moves: List[int] = []

        self.distance = []
        self.shortest_path = []

        self.current_target = None

        self.set_player_pos(players)
        self.get_current_target()
        self.get_legal_tile_squares()

    def make_move(self, move: Move):
        if move.is_tile == 1:
            self.place_tile(move.pos, move.ori)
            self.player_tiles[self.turn] -= 1

        else:
            self.player_pos[self.turn] = move.pos

        self.new_turn()

    def get_current_target(self):
        self.current_target = [((self.turn + 1) % 2) * self.side_squares * (
                self.side_squares - 1) + i for i in
                  range(self.side_squares)]

    def new_turn(self):
        """

        :return:
        """
        self.turn += 1
        self.turn %= len(self.player_pos)

        self.has_legal_player_moves = False
        self.has_legal_tile_moves = False

        self.get_current_target()

    def place_tile(self, rec_index, orientation):
        """

        :param rec_index: inbetween tile rectangle index
        :param orientation: orientation of the tile
        :return:
        """
        self.board_tiles.append(Tile(rec_index, orientation))

    def get_shortest_path(self, current_pos):
        distance = [-1] * self.side_squares * self.side_squares

        to_search = [current_pos]
        distance[current_pos] = 0
        shortest_path = []

        depth = 0
        while len(shortest_path) == 0:
            new_search = []
            for pos in to_search:
                distance[pos] = depth
                if pos in self.current_target:
                    shortest_path.append(pos)
                    break
                for adj in self.get_legal_moves(pos):
                    if distance[adj] == -1:
                        new_search.append(adj)

            to_search = new_search
            depth += 1

            if len(to_search) == 0:
                break

        depth -= 1
        if len(shortest_path) > 0:
            while shortest_path[-1] != current_pos:
                adj_sq = self.get_adjacent_squares(shortest_path[-1])
                if adj_sq is None:
                    break

                for adj in adj_sq:
                    if distance[adj] == depth - 1:
                        shortest_path.append(adj)
                        depth -= 1
                        continue

        if len(shortest_path) > 0:
            if shortest_path[0] not in self.current_target:
                shortest_path = []

        return distance, shortest_path

    def get_adjacent_squares(self, pos):
        adj = []

        if int((pos + 1) / self.side_squares) == int(pos / self.side_squares):
            adj.append(pos + 1)
        if int((pos - 1) / self.side_squares) == int(pos / self.side_squares):
            adj.append(pos - 1)
        if pos + self.side_squares < self.side_squares * self.side_squares - 1:
            adj.append(pos + self.side_squares)
        if pos - self.side_squares > 0:
            adj.append(pos - self.side_squares)

        return adj

    def get_legal_moves(self, current_pos):
        """

        :return:
        """

        def within_bounds(pos):
            """

            :param pos: position on the board
            :return:
            """
            if self.side_squares * self.side_squares > pos >= 0:
                return True
            return False

        def not_blocked(pos, direction, ori):
            """

            :param pos: position on the board
            :param direction: direction of movement
            :param ori: orientation of blocking tile
            :return:
            """

            pos_row = int(pos / self.side_squares)
            pos_col = int(pos % self.side_squares)

            tl = pos_row * (self.side_squares + 1) + pos_col
            tr = pos_row * (self.side_squares + 1) + pos_col + 1
            bl = (pos_row + 1) * (self.side_squares + 1) + pos_col
            br = (pos_row + 1) * (self.side_squares + 1) + pos_col + 1

            bt = [tile.rec_index for tile in self.board_tiles]
            bo = [tile.orientation for tile in self.board_tiles]

            if direction == 0:
                if tl in bt:
                    if bo[bt.index(tl)] == ori:
                        return False
                if tr in bt:
                    if bo[bt.index(tr)] == ori:
                        return False

            if direction == 1:
                if bl in bt:
                    if bo[bt.index(bl)] == ori:
                        return False
                if br in bt:
                    if bo[bt.index(br)] == ori:
                        return False

            if direction == 2:
                if bl in bt:
                    if bo[bt.index(bl)] == ori:
                        return False
                if tl in bt:
                    if bo[bt.index(tl)] == ori:
                        return False

            if direction == 3:
                if br in bt:
                    if bo[bt.index(br)] == ori:
                        return False
                if tr in bt:
                    if bo[bt.index(tr)] == ori:
                        return False

            return True

        moves = []
        adj = self.get_adjacent_squares(current_pos)

        pos_u = current_pos - self.side_squares
        if within_bounds(pos_u) and not_blocked(current_pos, 0, 1) and pos_u in adj:
            moves.append(pos_u)

        pos_d = current_pos + self.side_squares
        if within_bounds(pos_d) and not_blocked(current_pos, 1, 1) and pos_d in adj:
            moves.append(pos_d)

        pos_l = current_pos - 1
        if within_bounds(pos_l) and not_blocked(current_pos, 2, 0) and pos_l in adj:
            moves.append(pos_l)

        pos_r = current_pos + 1
        if within_bounds(pos_r) and not_blocked(current_pos, 3, 0) and pos_r in adj:
            moves.append(pos_r)

        return moves

    def check_arrow_key_move(self):
        if is_key_pressed(KEY_W):
            new_pos = self.player_pos[self.turn] - self.side_squares
            if new_pos in self.player_legal_moves:
                self.player_pos[self.turn] = new_pos
                self.new_turn()
        elif is_key_pressed(KEY_A):
            new_pos = self.player_pos[self.turn] - 1
            if new_pos in self.player_legal_moves:
                self.player_pos[self.turn] = new_pos
                self.new_turn()
        elif is_key_pressed(KEY_S):
            new_pos = self.player_pos[self.turn] + self.side_squares
            if new_pos in self.player_legal_moves:
                self.player_pos[self.turn] = new_pos
                self.new_turn()
        elif is_key_pressed(KEY_D):
            new_pos = self.player_pos[self.turn] + 1
            if new_pos in self.player_legal_moves:
                self.player_pos[self.turn] = new_pos
                self.new_turn()

    def get_legal_tile_squares(self):
        """

        :return:
        """
        orientation_zero = []  # Vertical
        orientation_one = []  # Horizontal

        for tile_index in range((self.side_squares + 1) * (self.side_squares + 1)):
            if tile_index in [tile.rec_index for tile in self.board_tiles]:
                continue

            if tile_index - (self.side_squares + 1) < 0:
                continue

            if tile_index + (self.side_squares + 1) >= (self.side_squares + 1) * (self.side_squares + 1):
                continue

            if tile_index - (self.side_squares + 1) in [tile.rec_index for tile in self.board_tiles if
                                                        tile.orientation == 0]:
                continue

            if tile_index + (self.side_squares + 1) in [tile.rec_index for tile in self.board_tiles if
                                                        tile.orientation == 0]:
                continue

            test_board = copy.deepcopy(self)
            test_board.make_move(Move(Tile(tile_index, 0), tile_index))
            distance, path = test_board.get_shortest_path(test_board.player_pos[test_board.turn])
            if len(path) == 0:
                continue

            orientation_zero.append(tile_index)

        for tile_index in range((self.side_squares + 1) * (self.side_squares + 1)):
            if tile_index in [tile.rec_index for tile in self.board_tiles]:
                continue

            if tile_index - 1 < 0:
                continue

            if int(tile_index / (self.side_squares + 1)) != int((tile_index - 1) / (self.side_squares + 1)):
                continue

            if int(tile_index / (self.side_squares + 1)) != int((tile_index + 1) / (self.side_squares + 1)):
                continue

            if tile_index - 1 in [tile.rec_index for tile in self.board_tiles if tile.orientation == 1]:
                continue

            if tile_index + 1 in [tile.rec_index for tile in self.board_tiles if tile.orientation == 1]:
                continue

            test_board = copy.deepcopy(self)
            test_board.make_move(Move(Tile(tile_index, 1), tile_index))
            distance, path = test_board.get_shortest_path(test_board.player_pos[test_board.turn])
            if len(path) == 0:
                continue

            orientation_one.append(tile_index)

        self.legal_tile_moves = [orientation_zero, orientation_one]

    def is_legal_tile_square(self, rec_index, current_orientation):
        """

        :param rec_index: rec index to check if legal tile
        :param current_orientation: current orientation of the placing tile
        :return:
        """
        if not self.has_legal_tile_moves:
            self.get_legal_tile_squares()
            self.has_legal_tile_moves = True

        return rec_index in self.legal_tile_moves[current_orientation]

    def set_player_pos(self, players_count):
        """

        :param players_count: amount of players
        :return:
        """
        pos = []
        col = []

        if players_count != 2 or players_count != 4:
            print("Players Count not 2 or 4, setting to 2")
            players_count = 2

        pos.append(int(self.side_squares / 2))
        pos.append(self.side_squares * self.side_squares - int(self.side_squares / 2) - 1)
        col.append(BLUE)
        col.append(DARKBLUE)

        if players_count == 4:
            pos.append(self.side_squares * 5)
            pos.append(self.side_squares * 4 + 1)

        self.player_pos = pos
        self.player_col = col


