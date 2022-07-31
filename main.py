from raylibpy import *
from typing import List
from Quoridor import QuoridorGame


def main():
    # GAME WINDOW SIZING
    width = 800
    height = 800

    # BOARD DIMENSIONS
    border = 100
    top_left_corner = Vector2(border, border)
    square_border = 15

    # Initialising Window
    init_window(width, height, "quoridor bot")

    # Creating Game Class
    quoridor_game = QuoridorGame(9, 18, 2, top_left_corner, width - 2 * border, square_border)

    # Mouse Point
    mouse_point: Vector2

    # Game Conditions
    set_target_fps(120)

    # Game Constants
    current_orientation = 0

    # Game Loop
    while not window_should_close():
        # Get mouse positions each loop
        mouse_point = get_mouse_position()

        # Switching orientation on mouse right click
        if is_mouse_button_pressed(MOUSE_RIGHT_BUTTON):
            current_orientation += 1
            current_orientation %= 2

        # Begin Drawing
        begin_drawing()
        clear_background(RAYWHITE)

        # Draw Quoridor Game
        quoridor_game.draw()

        # If the current player has tiles remaining and player is not being held/dragged
        if quoridor_game.current_board.player_tiles[quoridor_game.current_board.turn] > 0 and quoridor_game.player_selected is None:
            for rec_ind, rec in enumerate(quoridor_game.tile_squares):
                if check_collision_point_rec(mouse_point, rec):
                    # If is legal move
                    if quoridor_game.current_board.is_legal_tile_square(rec_ind, current_orientation):
                        # If left mouse button is pressed, place tile
                        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                            quoridor_game.current_board.place_tile(rec_ind, current_orientation)

                            quoridor_game.current_board.player_tiles[quoridor_game.current_board.turn] -= 1
                            quoridor_game.current_board.new_turn()

                        # If left mouse button is not pressed, display tile
                        else:
                            quoridor_game.draw_tile(rec_ind, current_orientation, PURPLE)
                    # Draw red tile, meaning invalid position
                    else:
                        quoridor_game.draw_tile(rec_ind, current_orientation, RED)

        # Moving player with mouse keys
        quoridor_game.current_board.check_arrow_key_move()

        # Select a player to move
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            if check_collision_point_rec(mouse_point, quoridor_game.board_squares[quoridor_game.current_board.player_pos[quoridor_game.current_board.turn]]):
                quoridor_game.player_selected = quoridor_game.current_board.turn

        # Left mouse is released and currently holding player
        if is_mouse_button_released(MOUSE_LEFT_BUTTON) and quoridor_game.player_selected is not None:
            old_pos = quoridor_game.current_board.player_pos[quoridor_game.current_board.turn]
            for rec_ind, rec in enumerate(quoridor_game.board_squares):
                if check_collision_point_rec(mouse_point, rec):
                    quoridor_game.player_selected = None
                    old_turn = quoridor_game.current_board.turn

                    # If legal move, update board
                    if not quoridor_game.current_board.player_pos[quoridor_game.current_board.turn] == rec_ind and rec_ind in quoridor_game.current_board.player_legal_moves:
                        quoridor_game.current_board.player_pos[old_turn] = rec_ind
                        quoridor_game.current_board.new_turn()
                    # Otherwise, return to old position
                    else:
                        quoridor_game.current_board.player_pos[old_turn] = old_pos

        # End drawing loop
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()
