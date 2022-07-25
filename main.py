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

    quoridor_game = QuoridorGame(9, 20, 2, top_left_corner, width - 2 * border, square_border)

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

        for rec_ind, rec in enumerate(quoridor_game.tile_squares):
            if check_collision_point_rec(mouse_point, rec):
                if quoridor_game.is_legal_tile_square(rec_ind, current_orientation):
                    if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                        quoridor_game.place_tile(rec_ind, current_orientation)
                        quoridor_game.has_legal_moves = False

                    else:
                        quoridor_game.draw_tile(rec_ind, current_orientation, PURPLE)
                else:
                    quoridor_game.draw_tile(rec_ind, current_orientation, RED)

        end_drawing()

    close_window()


if __name__ == '__main__':
    main()