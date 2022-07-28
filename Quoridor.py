from raylibpy import *
from typing import List, Union


class QuoridorGame:
    def __init__(self,
                 side_squares: int,
                 total_tiles: int,
                 players: int,
                 position: Vector2,
                 width: int,
                 border: int):

        """

        :param side_squares: amount of squares on one side
        :param total_tiles: total tiles shared equally between all players
        :param players: number of players
        :param position: board corner position
        :param width: board width
        :param border: board height
        """

        self.side_squares = side_squares
        self.tile_count = total_tiles

        self.position = position
        self.width = width
        self.border = border
        self.square_width = (self.width - self.border * (self.side_squares + 1)) / self.side_squares

        self.player_pos: List[int] = []
        self.player_col: List[Color] = []
        self.player_tiles: List[int] = [int(total_tiles / players)] * players
        self.board_tiles: List[Tile] = []

        self.player_selected: Union[int, None] = None

        self.turn = 0

        self.has_legal_tile_moves: bool = False
        self.legal_tile_moves: List[List[int]] = []

        self.has_legal_player_moves: bool = False
        self.player_legal_moves: List[int] = []
        self.distance = []

        self.board_squares = self.get_board_squares()
        self.tile_squares = self.get_tile_squares()

        self.set_player_pos(players)

    def new_turn(self):
        """

        :return:
        """
        self.turn += 1
        self.turn %= len(self.player_pos)

        self.has_legal_player_moves = False
        self.has_legal_tile_moves = False

    def draw(self):
        """

        :return:
        """
        draw_rectangle(self.position.x, self.position.y, self.width, self.width, Color(220, 220, 220, 255))

        for rec in self.board_squares:
            draw_rectangle_rec(rec, LIGHTGRAY)

        for rec in self.tile_squares:
            draw_rectangle_rec(rec, BROWN)

        draw_text(f'Turn: {self.turn}', 10, 10, 30, BLACK)
        for i in range(len(self.player_pos)):
            draw_text(f'Player {i} Tiles: {self.player_tiles[i]}',
                      300,
                      i * 25 + 10,
                      20,
                      BLACK)

        if not self.has_legal_player_moves:
            self.player_legal_moves = self.get_legal_moves(self.player_pos[self.turn])
            target = [((self.turn + 1) % 2) * self.side_squares * (self.side_squares - 1) + i for i in range(self.side_squares)]
            self.get_shortest_path(self.player_pos[self.turn], target)
            self.has_legal_player_moves = True

        for index, val in enumerate(self.distance):
            col = Color(255, 255 * val / max(self.distance) / 2, 255, 255)
            draw_rectangle_rec(self.board_squares[index], col)
            draw_text(str(val), self.board_squares[index].x, self.board_squares[index].y, 30, WHITE)

        self.draw_legal_moves()
        self.draw_tiles()
        self.draw_players()

    def place_tile(self, rec_index, orientation):
        """

        :param rec_index: inbetween tile rectangle index
        :param orientation: orientation of the tile
        :return:
        """
        self.board_tiles.append(Tile(rec_index, orientation))

    def draw_players(self):
        """

        :return:
        """
        for player_ind, player_pos in enumerate(self.player_pos):
            if player_ind != self.player_selected:
                draw_circle(self.board_squares[player_pos].x + self.square_width / 2,
                            self.board_squares[player_pos].y + self.square_width / 2,
                            self.square_width / 4,
                            self.player_col[player_ind])
            else:
                draw_circle(get_mouse_x(),
                            get_mouse_y(),
                            self.square_width / 4,
                            self.player_col[player_ind])

    def draw_tile(self, rec, ori, col):
        """

        :param rec: tile rectangle
        :param ori: tile orientation
        :param col: tile colour
        :return:
        """
        if ori == 0:
            draw_rectangle(
                self.tile_squares[rec].x,
                self.tile_squares[rec].y - self.square_width,
                self.border,
                int(self.square_width * 2 + self.border),
                col
            )
        else:
            draw_rectangle(
                self.tile_squares[rec].x - self.square_width,
                self.tile_squares[rec].y,
                int(self.square_width * 2 + self.border),
                self.border,
                col
            )

    def draw_tiles(self):
        """

        :return:
        """
        for tile in self.board_tiles:
            self.draw_tile(tile.rec_index, tile.orientation, DARKPURPLE)

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

    def get_board_squares(self):
        """

        :return:
        """
        board_squares = []

        for j in range(self.side_squares):
            for i in range(self.side_squares):
                rec = Rectangle(self.position.x + (i * (self.square_width + self.border)) + self.border,
                                self.position.y + (j * (self.square_width + self.border)) + self.border,
                                self.square_width,
                                self.square_width)

                board_squares.append(rec)

        return board_squares

    def get_shortest_path(self, current_pos, target):
        distance = [-1] * self.side_squares * self.side_squares

        to_search = [current_pos]
        distance[current_pos] = 0

        depth = 0
        while True:
            new_search = []
            for pos in to_search:
                distance[pos] = depth
                if pos in target:
                    break
                for adj in self.get_legal_moves(pos):
                    if distance[adj] == -1:
                        new_search.append(adj)

            to_search = new_search
            depth += 1

            if len(to_search) == 0:
                break

        self.distance = distance

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

    def draw_legal_moves(self):
        """

        :return:
        """
        if self.player_legal_moves is not None:
            for legal_move in self.player_legal_moves:
                draw_circle(self.board_squares[legal_move].x + self.square_width / 2,
                            self.board_squares[legal_move].y + self.square_width / 2,
                            self.square_width / 8,
                            BROWN)

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

    def get_tile_squares(self):
        """

        :return:
        """
        recs = []

        square_width = (self.width - self.border * (self.side_squares + 1)) / self.side_squares

        for j in range(self.side_squares + 1):
            for i in range(self.side_squares + 1):
                recs.append(Rectangle(
                    self.position.x + (i * (square_width + self.border)),
                    self.position.y + (j * (square_width + self.border)),
                    self.border,
                    self.border
                ))

        return recs

    def get_legal_tile_squares(self):
        """

        :return:
        """
        orientation_zero = []  # Vertical
        orientation_one = []  # Horizontal

        for tile_index, tile_square in enumerate(self.tile_squares):
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

            orientation_zero.append(tile_index)

        for tile_index, tile_square in enumerate(self.tile_squares):
            if int(tile_index / (self.side_squares + 1)) != int((tile_index - 1) / (self.side_squares + 1)):
                continue

            if int(tile_index / (self.side_squares + 1)) != int((tile_index + 1) / (self.side_squares + 1)):
                continue

            if tile_index - 1 in [tile.rec_index for tile in self.board_tiles if tile.orientation == 1]:
                continue

            if tile_index + 1 in [tile.rec_index for tile in self.board_tiles if tile.orientation == 1]:
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


class Tile:
    def __init__(self, rec_index, orientation):
        """

        :param rec_index: tile rectangle index
        :param orientation: tile orientation
        """
        self.rec_index = rec_index
        self.orientation = orientation
