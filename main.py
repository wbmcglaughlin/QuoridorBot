from raylibpy import *
from typing import List
from Quoridor import QuoridorGame

def main():
    width = 800
    height = 800

    border = 100
    top_left_corner = Vector2(border, border)

    init_window(width, height, "quoridor bot")

    quoridor_game = QuoridorGame(9, 20, 2)

    mouse_point: Vector2

    set_target_fps(60)

    square_border = 30

    while not window_should_close():

        mouse_point = get_mouse_position()

        begin_drawing()
        clear_background(RAYWHITE)

        quoridor_game.draw_board(top_left_corner, width - 2 * border, square_border)
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()