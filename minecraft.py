import moderngl as mgl
import glfw
import setup
import chunk, camera


glfw.init()

game_window, game_context = setup.setup()

print(glfw.get_window_size(game_window.window))

test_prog = setup.program(game_context, vertex_shader="raw.vs", fragment_shader="uncooked.fs")
test_prog.load_texture_array()

test_chunk = chunk.chunk()
test_chunk.blocks_to_vertices()

test_camera = camera.camera(game_window)

test_face = [0, 0, 0, 0, 0, 0,
             0, 0, 1, 0, 1, 0,
             1, 0, 0, 1, 0, 0,
             1, 0, 1, 1, 1, 0]
test_buffer = game_context.buffer(bytes(test_face))
test_array = game_context.vertex_array(test_prog.program, [(test_buffer, "3f4 2f4 1f4", "position", "texture_coords", "texture_ID")])

while game_window.run:
    test_array.render()
    game_window.clear()
    game_window.swap_buffers()
    