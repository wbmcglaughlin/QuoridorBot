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

        self.board_squares = self.get_board_squares()
        self.tile_squares = self.get_tile_squares()

        self.set_player_pos(players)

    def draw(self):
        draw_rectangle(self.position.x, self.position.y, self.width, self.width, GOLD)

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

        self.draw_players()

        if not self.has_legal_player_moves:
            self.get_legal_moves()
            self.has_legal_player_moves = True

        self.draw_legal_moves()

        self.draw_tiles()

    def place_tile(self, rec_index, orientation):
        self.board_tiles.append(Tile(rec_index, orientation))

    def draw_players(self):
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
        for tile in self.board_tiles:
            self.draw_tile(tile.rec_index, tile.orientation, DARKPURPLE)

    def set_player_pos(self, players_count):
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
        board_squares = []

        for j in range(self.side_squares):
            for i in range(self.side_squares):
                rec = Rectangle(self.position.x + (i * (self.square_width + self.border)) + self.border,
                                self.position.y + (j * (self.square_width + self.border)) + self.border,
                                self.square_width,
                                self.square_width)

                board_squares.append(rec)

        return board_squares

    def get_legal_moves(self):
        def within_bounds(pos):
            if self.side_squares * self.side_squares > pos >= 0:
                return True
            return False

        def not_blocked(pos, direction, ori):
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

        self.player_legal_moves = []

        pos_u = self.player_pos[self.turn] - self.side_squares
        if within_bounds(pos_u) and not_blocked(self.player_pos[self.turn], 0, 1):
            self.player_legal_moves.append(pos_u)

        pos_d = self.player_pos[self.turn] + self.side_squares
        if within_bounds(pos_d) and not_blocked(self.player_pos[self.turn], 1, 1):
            self.player_legal_moves.append(pos_d)

        pos_l = self.player_pos[self.turn] - 1
        if within_bounds(pos_l) and not_blocked(self.player_pos[self.turn], 2, 0):
            self.player_legal_moves.append(pos_l)

        pos_r = self.player_pos[self.turn] + 1
        if within_bounds(pos_r) and not_blocked(self.player_pos[self.turn], 3, 0):
            self.player_legal_moves.append(pos_r)

    def draw_legal_moves(self):
        if self.player_legal_moves is not None:
            for legal_move in self.player_legal_moves:
                draw_circle(self.board_squares[legal_move].x + self.square_width / 2,
                            self.board_squares[legal_move].y + self.square_width / 2,
                            self.square_width / 8,
                            BROWN)

    def get_tile_squares(self):
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
        if not self.has_legal_tile_moves:
            self.get_legal_tile_squares()
            self.has_legal_tile_moves = True

        return rec_index in self.legal_tile_moves[current_orientation]


class Tile:
    def __init__(self, rec_index, orientation):
        self.rec_index = rec_index
        self.orientation = orientation
