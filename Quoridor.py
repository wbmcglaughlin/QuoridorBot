from raylibpy import *
from typing import List


class QuoridorGame:
    def __init__(self, side_squares: int, total_tiles: int, players: int):
        self.side_squares = side_squares
        self.tile_count = total_tiles

        self.player_tiles: List[int] = []
        self.board_tiles = []

    def draw_board(self, position: Vector2, width: int, border: float):
        draw_rectangle(position.x, position.y, width, width, GOLD)
        square_width = (width - border * (self.side_squares  + 1)) / self.side_squares

        for i in range(self.side_squares):
            for j in range(self.side_squares):
                draw_rectangle(position.x + (i * (square_width + border)) + border,
                               position.y + (j * (square_width + border)) + border,
                               square_width,
                               square_width,
                               BLACK)
