from raylibpy import *
from typing import List


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
        self.player_tiles: List[int] = []
        self.board_tiles: List[Tile] = []

        self.board_squares = self.get_board_squares()
        self.tile_squares = self.get_tile_squares()

        self.set_player_pos(players)

    def draw(self):
        draw_rectangle(self.position.x, self.position.y, self.width, self.width, GOLD)

        for rec in self.board_squares:
            draw_rectangle_rec(rec, LIGHTGRAY)

        for rec in self.tile_squares:
            draw_rectangle_rec(rec, BROWN)

        self.draw_players()

        self.draw_tiles()

    def place_tile(self, rec_index, orientation):
        self.board_tiles.append(Tile(rec_index, orientation))

    def draw_players(self):
        for player_ind, player_pos in enumerate(self.player_pos):
            draw_circle(self.board_squares[player_pos].x + self.square_width / 2,
                        self.board_squares[player_pos].y + self.square_width / 2,
                        self.square_width / 4,
                        self.player_col[player_ind])

    def draw_tiles(self):
        for tile in self.board_tiles:
            if tile.orientation == 0:
                draw_rectangle(
                    self.tile_squares[tile.rec_index].x,
                    self.tile_squares[tile.rec_index].y - self.square_width,
                    self.border,
                    int(self.square_width * 2 + self.border),
                    PURPLE
                )
            else:
                draw_rectangle(
                    self.tile_squares[tile.rec_index].x - self.square_width,
                    self.tile_squares[tile.rec_index].y,
                    int(self.square_width * 2 + self.border),
                    self.border,
                    PURPLE
                )

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

        recs.pop(-1)
        recs.pop(-self.side_squares)
        recs.pop(self.side_squares)
        recs.pop(0)

        return recs

    def is_legal_tile_square(self, rec_index):
        for tile in self.board_tiles:
            if tile.rec_index == rec_index:
                return False

        return True

class Tile:
    def __init__(self, rec_index, orientation):
        self.rec_index = rec_index
        self.orientation = orientation
