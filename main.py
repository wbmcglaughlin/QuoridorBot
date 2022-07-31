from raylibpy import *
from Quoridor.QuoridorGame import QuoridorGame
from Quoridor.QuoridorBot import QuoridorBot


def main():
    # GAME WINDOW SIZING
    width = 800
    height = 800

    # BOARD DIMENSIONS
    border = 100
    tl_corner = Vector2(border, border)
    square_border = 15

    # Creating Game Class
    quoridor_game = QuoridorGame([QuoridorBot(), None],
                                 9,
                                 18,
                                 2,
                                 tl_corner,
                                 width - 2 * border,
                                 square_border)

    # Mouse Point
    mouse_point: Vector2

    # Initialising Window
    init_window(width, height, "quoridor bot")

    # Game Conditions
    set_target_fps(120)

    # Game Loop
    while not window_should_close():
        # Switching orientation on mouse right click
        if is_mouse_button_pressed(MOUSE_RIGHT_BUTTON):
            quoridor_game.orientation += 1
            quoridor_game.orientation %= 2

        # Begin Drawing
        begin_drawing()
        clear_background(RAYWHITE)

        # Draw Quoridor Game
        quoridor_game.draw()

        # Check Inputs and Display
        quoridor_game.loop()

        # End drawing loop
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
