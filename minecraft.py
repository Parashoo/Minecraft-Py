from glfw import get_time
import glm
import numpy as np
from OpenGL.GL import *
from math import sin, cos
from packages import utilities
from packages import chunk, render, world_gen

vertex_source_3d = 'shaders/scene.vs'
fragment_source_3d = 'shaders/scene.fs'

vertex_source_GUI = 'shaders/hud.vs'
fragment_source_GUI = 'shaders/hud.fs'

vertex_source_sky = 'shaders/sky.vs'
fragment_source_sky = 'shaders/sky.fs'

camera = utilities.camera((0, 16, 0), (0, 0, 0), (800, 600))

delta_time = 0.0
last_frame = 0.0

def main():

    global delta_time, last_frame

    fps_list = []

    test_world = world_gen.world('__DELETEME__', '-o')
    window = utilities.window()
    camera.setup_window(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    crosshair = np.array([
      0.0, 0.0, 0.0], dtype = 'float32')

    shader_program = utilities.shader(vertex_source_3d, fragment_source_3d, '330')
    shader_program.compile()

    shader_program_2d = utilities.shader(vertex_source_GUI, fragment_source_GUI, '330')
    shader_program_2d.compile()

    shader_program_sky = utilities.shader(vertex_source_sky, fragment_source_sky, '330')
    shader_program_sky.compile()

    sky = np.array([
        -1.0, 1.0, 0.0,
         1.0, 1.0, 0.0,
        -1.0,-1.0, 0.0,
         1.0,-1.0, 0.0], dtype = 'float32')

    sky_vbo, sky_vao = glGenBuffers(1), glGenVertexArrays(1)
    glBindVertexArray(sky_vao)
    glBindBuffer(GL_ARRAY_BUFFER, sky_vbo)
    glBufferData(GL_ARRAY_BUFFER, sky, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    vbo_2d, vao_2d = glGenBuffers(1), glGenVertexArrays(1)

    glBindVertexArray(vao_2d)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_2d)
    glBufferData(GL_ARRAY_BUFFER, crosshair, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    cobble_tex = utilities.texture('ressources/cobblestone.png', False)
    cobble_tex.source_open()
    cobble_tex_ID = cobble_tex.gen_texture()

    crosshair_texture = utilities.texture('ressources/icons.png', False)
    crosshair_texture.source_open_zone((0, 0, 16, 16))
    crosshair_texture_ID = crosshair_texture.gen_texture()

    exposed_list = test_world.return_all_exposed()

    shader_program.use()
    shader_program.set_int('texture0', 0)

    shader_program_2d.use()
    shader_program_2d.set_int('texture0', 0)

    camera_direction = glm.vec3()
    second_counter = 0
    frame_counter = 0

    chunk_render = render.render(exposed_list)
    chunk_render.create_buffers()

    while not window.check_if_closed():

        current_frame = get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        second_counter += delta_time
        frame_counter += 1

        window.refresh(0)

        shader_program_sky.use()
        shader_program_sky.set_float('orientation', glm.radians(camera.pitch))
        glDisable(GL_DEPTH_TEST)
        glBindVertexArray(sky_vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        camera.process_input(window, delta_time)
        camera.testing_commands(window)

        glActiveTexture(GL_TEXTURE0)

        shader_program.use()

        pos, looking, up = camera.return_vectors()
        view = glm.lookAt(pos, looking, up)
        projection = glm.perspective(glm.radians(45), window.size[0]/window.size[1], 0.1, 100)
        shader_program.set_mat4('view', glm.value_ptr(view))
        shader_program.set_mat4('projection', glm.value_ptr(projection))

        glEnable(GL_DEPTH_TEST)
        chunk_render.draw_buffer(shader_program, cobble_tex_ID)

        glBindVertexArray(0)


        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, crosshair_texture_ID)

        shader_program_2d.use()


        glBindVertexArray(vao_2d)
        glPointSize(32)
        glDrawArrays(GL_POINTS, 0, 1)

        if second_counter >= 1:
            fps_list.append(frame_counter)
            second_counter, frame_counter = 0, 0
        window.refresh(1)

    window.close()
    print('\n===== End statistics =====')
    print('Average FPS: {}'.format(np.mean(fps_list)))
    print(test_world.return_time(),'\n')

if __name__ == '__main__':
    main()
