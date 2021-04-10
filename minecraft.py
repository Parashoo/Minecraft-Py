import moderngl as mgl
import glfw
import setup

glfw.init()

game_window, game_context = setup.setup()
test_prog = setup.program(game_context, "testshader.vs")

test_prog.load_textures()

while game_window.run:
    game_window.clear()
    game_window.swap_buffers()
    