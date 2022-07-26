from raylibpy import *
from typing import List
from Quoridor import QuoridorGame


def main():
    width = 800
    height = 800

    border = 100
    top_left_corner = Vector2(border, border)
    square_border = 15

    init_window(width, height, "quoridor bot")

    quoridor_game = QuoridorGame(9, 18, 2, top_left_corner, width - 2 * border, square_border)

    mouse_point: Vector2

    set_target_fps(60)

    current_orientation = 0

    while not window_should_close():

        mouse_point = get_mouse_position()

        if is_mouse_button_pressed(MOUSE_RIGHT_BUTTON):
            current_orientation += 1
            current_orientation %= 2

        begin_drawing()
        clear_background(RAYWHITE)

        quoridor_game.draw()

        if quoridor_game.player_tiles[quoridor_game.turn] > 0 and quoridor_game.player_selected is None:
            for rec_ind, rec in enumerate(quoridor_game.tile_squares):
                if check_collision_point_rec(mouse_point, rec):
                    if quoridor_game.is_legal_tile_square(rec_ind, current_orientation):
                        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                            quoridor_game.place_tile(rec_ind, current_orientation)
                            quoridor_game.has_legal_moves = False

                            quoridor_game.player_tiles[quoridor_game.turn] -= 1
                            quoridor_game.turn += 1
                            quoridor_game.turn %= len(quoridor_game.player_pos)
                        else:
                            quoridor_game.draw_tile(rec_ind, current_orientation, PURPLE)
                    else:
                        quoridor_game.draw_tile(rec_ind, current_orientation, RED)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            if check_collision_point_rec(mouse_point, quoridor_game.board_squares[quoridor_game.player_pos[quoridor_game.turn]]):
                quoridor_game.player_selected = quoridor_game.turn

        if is_mouse_button_released(MOUSE_LEFT_BUTTON) and quoridor_game.player_selected is not None:
            for rec_ind, rec in enumerate(quoridor_game.board_squares):
                if check_collision_point_rec(mouse_point, rec):
                    quoridor_game.player_selected = None
                    old_turn = quoridor_game.turn

                    if not quoridor_game.player_pos[quoridor_game.turn] == rec_ind:
                        quoridor_game.has_legal_moves = False
                        quoridor_game.turn += 1
                        quoridor_game.turn %= len(quoridor_game.player_pos)

                    quoridor_game.player_pos[old_turn] = rec_ind


        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
