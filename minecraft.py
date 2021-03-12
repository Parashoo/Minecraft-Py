import moderngl as mgl
import setup


game_window, game_context = setup.setup()

while True:
    game_window.clear()
    game_window.swap_buffers()
    