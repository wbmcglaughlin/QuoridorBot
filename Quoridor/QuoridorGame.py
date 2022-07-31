import time

import raylibpy as rl

rl.draw_line_ex = lambda start_pos, end_pos, thick, color: rl._rl.DrawLineEx(rl._vec2(start_pos), rl._vec2(end_pos),
                                                                             rl._float(thick), rl._color(color))

from typing import List, Union
from raylibpy import *
from Quoridor.QuoridorBoard import QuoridorBoard
from Quoridor.QuoridorBot import QuoridorBot


class QuoridorGame:
    def __init__(self,
                 player_types: List[Union[QuoridorBot, None]],
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

        self.player_types = player_types
        self.current_board = QuoridorBoard(side_squares, 0, total_tiles, players)

        self.position = position
        self.width = width
        self.border = border
        self.square_width = (self.width - self.border * (side_squares + 1)) / side_squares

        self.player_selected: Union[int, None] = None
        self.orientation = 0

        self.board_squares = self.get_board_squares()
        self.tile_squares = self.get_tile_squares()

    def draw(self):
        """

        :return:
        """
        draw_rectangle(self.position.x, self.position.y, self.width, self.width, Color(220, 220, 220, 255))

        for rec in self.board_squares:
            draw_rectangle_rec(rec, LIGHTGRAY)

        for rec_index, rec in enumerate(self.tile_squares):
            if rec_index in self.current_board.legal_tile_moves[self.orientation]:
                draw_rectangle_rec(rec, BROWN)
            else:
                draw_rectangle_rec(rec, RED)

        draw_text(f'Turn: {self.current_board.turn}', 10, 10, 30, BLACK)
        for i in range(len(self.current_board.player_pos)):
            draw_text(f'Player {i} Tiles: {self.current_board.player_tiles[i]}',
                      300,
                      i * 25 + 10,
                      20,
                      BLACK)

        if not self.current_board.has_legal_player_moves:
            self.current_board.player_legal_moves = self.current_board.get_legal_moves(
                self.current_board.player_pos[self.current_board.turn])
            self.current_board.distance, self.current_board.shortest_path = self.current_board.get_shortest_path(
                self.current_board.player_pos[self.current_board.turn])
            self.current_board.has_legal_player_moves = True

        for index, val in enumerate(self.current_board.distance):
            col = Color(255, 255 * val / max(self.current_board.distance) / 2, 255, 255)
            draw_rectangle_rec(self.board_squares[index], col)
            draw_text(str(val), self.board_squares[index].x, self.board_squares[index].y, 30, WHITE)

        for index, val in enumerate(self.current_board.shortest_path):
            if index != 0:
                last = self.current_board.shortest_path[index - 1]
                draw_line_ex(Vector2(self.board_squares[val].x + self.board_squares[val].width / 2,
                                     self.board_squares[val].y + self.board_squares[val].height / 2),
                             Vector2(self.board_squares[last].x + self.board_squares[last].width / 2,
                                     self.board_squares[last].y + self.board_squares[last].height / 2),
                             5,
                             PURPLE)

        self.draw_legal_moves()
        self.draw_tiles()
        self.draw_players()

    def loop(self):
        if not self.player_types[self.current_board.turn]:
            mouse_point = get_mouse_position()
            # If the current player has tiles remaining and player is not being held/dragged
            if self.current_board.player_tiles[self.current_board.turn] > 0 and self.player_selected is None:
                for rec_ind, rec in enumerate(self.tile_squares):
                    if check_collision_point_rec(mouse_point, rec):
                        # If is legal move
                        if self.current_board.is_legal_tile_square(rec_ind, self.orientation):
                            # If left mouse button is pressed, place tile
                            if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                                self.current_board.place_tile(rec_ind, self.orientation)

                                self.current_board.player_tiles[self.current_board.turn] -= 1
                                self.current_board.new_turn()

                            # If left mouse button is not pressed, display tile
                            else:
                                self.draw_tile(rec_ind, self.orientation, PURPLE)
                        # Draw red tile, meaning invalid position
                        else:
                            self.draw_tile(rec_ind, self.orientation, RED)

            # Moving player with mouse keys
            self.current_board.check_arrow_key_move()

            # Select a player to move
            if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                if check_collision_point_rec(mouse_point, self.board_squares[self.current_board.player_pos[self.current_board.turn]]):
                    self.player_selected = self.current_board.turn

            # Left mouse is released and currently holding player
            if is_mouse_button_released(MOUSE_LEFT_BUTTON) and self.player_selected is not None:
                old_pos = self.current_board.player_pos[self.current_board.turn]
                for rec_ind, rec in enumerate(self.board_squares):
                    if check_collision_point_rec(mouse_point, rec):
                        self.player_selected = None
                        old_turn = self.current_board.turn

                        # If legal move, update board
                        if not self.current_board.player_pos[
                                   self.current_board.turn] == rec_ind and rec_ind in self.current_board.player_legal_moves:
                            self.current_board.player_pos[old_turn] = rec_ind
                            self.current_board.new_turn()
                        # Otherwise, return to old position
                        else:
                            self.current_board.player_pos[old_turn] = old_pos
        else:
            print("Calculating Bot Move")
            start = time.time()
            bot = self.player_types[self.current_board.turn]
            move = bot.get_move(self.current_board)
            self.current_board.make_move(move)
            print(f"Finished Calculating: {(time.time() - start):2f} s")

    def draw_players(self):
        """

        :return:
        """
        for player_ind, player_pos in enumerate(self.current_board.player_pos):
            if player_ind != self.player_selected:
                draw_circle(self.board_squares[player_pos].x + self.square_width / 2,
                            self.board_squares[player_pos].y + self.square_width / 2,
                            self.square_width / 4,
                            self.current_board.player_col[player_ind])
            else:
                draw_circle(get_mouse_x(),
                            get_mouse_y(),
                            self.square_width / 4,
                            self.current_board.player_col[player_ind])

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
        for tile in self.current_board.board_tiles:
            self.draw_tile(tile.rec_index, tile.orientation, DARKPURPLE)

    def get_board_squares(self):
        """

        :return:
        """
        board_squares = []

        for j in range(self.current_board.side_squares):
            for i in range(self.current_board.side_squares):
                rec = Rectangle(self.position.x + (i * (self.square_width + self.border)) + self.border,
                                self.position.y + (j * (self.square_width + self.border)) + self.border,
                                self.square_width,
                                self.square_width)

                board_squares.append(rec)

        return board_squares

    def draw_legal_moves(self):
        """

        :return:
        """
        if self.current_board.player_legal_moves is not None:
            for legal_move in self.current_board.player_legal_moves:
                draw_circle(self.board_squares[legal_move].x + self.square_width / 2,
                            self.board_squares[legal_move].y + self.square_width / 2,
                            self.square_width / 8,
                            BROWN)

    def get_tile_squares(self):
        """

        :return:
        """
        recs = []

        square_width = (self.width - self.border * (
                self.current_board.side_squares + 1)) / self.current_board.side_squares

        for j in range(self.current_board.side_squares + 1):
            for i in range(self.current_board.side_squares + 1):
                recs.append(Rectangle(
                    self.position.x + (i * (square_width + self.border)),
                    self.position.y + (j * (square_width + self.border)),
                    self.border,
                    self.border
                ))

        return recs
