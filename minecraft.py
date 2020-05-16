import glfw
import glm
import numpy as np
from OpenGL.GL import *
from math import sin, cos
from packages import shader_utils, window_utils, texture_utils, camera_utils

vertex_source_3d = 'shaders/scene.vs'
fragment_source_3d = 'shaders/scene.fs'

vertex_source_GUI = 'shaders/hud.vs'
fragment_source_GUI = 'shaders/hud.fs'

camera = camera_utils.camera((0, 0, -3), (0, 0, 1), (800, 600))

last_x, last_y = 400, 300
yaw, pitch = -90, 0
first_mouse = True

delta_time = 0.0
last_frame = 0.0

def main():
    global delta_time, last_frame

    window = window_utils.window()
    camera.setup_window(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    crosshair = np.array([
      0.0, 0.0, 0.0], dtype = 'float32')

    vertices = np.array([
      -0.5, -0.5, -0.5,  0.0, 0.0,
       0.5, -0.5, -0.5,  1.0, 0.0,
       0.5,  0.5, -0.5,  1.0, 1.0,
       0.5,  0.5, -0.5,  1.0, 1.0,
      -0.5,  0.5, -0.5,  0.0, 1.0,
      -0.5, -0.5, -0.5,  0.0, 0.0,

      -0.5, -0.5,  0.5,  0.0, 0.0,
       0.5, -0.5,  0.5,  1.0, 0.0,
       0.5,  0.5,  0.5,  1.0, 1.0,
       0.5,  0.5,  0.5,  1.0, 1.0,
      -0.5,  0.5,  0.5,  0.0, 1.0,
      -0.5, -0.5,  0.5,  0.0, 0.0,

      -0.5,  0.5,  0.5,  1.0, 0.0,
      -0.5,  0.5, -0.5,  1.0, 1.0,
      -0.5, -0.5, -0.5,  0.0, 1.0,
      -0.5, -0.5, -0.5,  0.0, 1.0,
      -0.5, -0.5,  0.5,  0.0, 0.0,
      -0.5,  0.5,  0.5,  1.0, 0.0,

       0.5,  0.5,  0.5,  1.0, 0.0,
       0.5,  0.5, -0.5,  1.0, 1.0,
       0.5, -0.5, -0.5,  0.0, 1.0,
       0.5, -0.5, -0.5,  0.0, 1.0,
       0.5, -0.5,  0.5,  0.0, 0.0,
       0.5,  0.5,  0.5,  1.0, 0.0,

      -0.5, -0.5, -0.5,  0.0, 1.0,
       0.5, -0.5, -0.5,  1.0, 1.0,
       0.5, -0.5,  0.5,  1.0, 0.0,
       0.5, -0.5,  0.5,  1.0, 0.0,
      -0.5, -0.5,  0.5,  0.0, 0.0,
      -0.5, -0.5, -0.5,  0.0, 1.0,

      -0.5,  0.5, -0.5,  0.0, 1.0,
       0.5,  0.5, -0.5,  1.0, 1.0,
       0.5,  0.5,  0.5,  1.0, 0.0,
       0.5,  0.5,  0.5,  1.0, 0.0,
      -0.5,  0.5,  0.5,  0.0, 0.0,
      -0.5,  0.5, -0.5,  0.0, 1.0
      ], dtype='float32')

    indexes = np.array([
      0, 1, 3,
      1, 2, 3
      ], dtype='int32')

    cube_offsets = [
      glm.vec3( 0.0, 0.0, 0.0),
      glm.vec3( 2.0, 5.0,-15.0),
      glm.vec3(-1.5,-2.2,-2.5),
      glm.vec3(-3.8,-2.9,-12.3),
      glm.vec3( 2.4,-0.4,-3.5),
      glm.vec3(-1.7, 3.0,-7.5),
      glm.vec3( 1.3,-2.0, -2.5),
      glm.vec3( 1.5, 2.0, -2.5),
      glm.vec3( 1.5, 0.2, -1.5),
      glm.vec3(-1.3, 1.0, -1.5)
      ]

    shader_program = shader_utils.shader(vertex_source_3d, fragment_source_3d, '330')
    shader_program.compile()

    shader_program_2d = shader_utils.shader(vertex_source_GUI, fragment_source_GUI, '330')
    shader_program_2d.compile()

    vbo, vao, ebo = glGenBuffers(1), glGenVertexArrays(1), glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexes, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    vbo_2d, vao_2d = glGenBuffers(1), glGenVertexArrays(1)

    glBindVertexArray(vao_2d)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_2d)
    glBufferData(GL_ARRAY_BUFFER, crosshair, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    texture0 = texture_utils.texture('ressources/cobblestone.png', False)
    texture0.source_open()
    texture0_ID = texture0.gen_texture()

    crosshair_texture = texture_utils.texture('ressources/icons.png', False)
    crosshair_texture.source_open_zone((0, 0, 16, 16))
    crosshair_texture_ID = crosshair_texture.gen_texture()

    shader_program.use()
    shader_program.set_int('texture0', 0)

    shader_program_2d.use()
    shader_program_2d.set_int('texture0', 0)

    camera_direction = glm.vec3()
    yaw = -90.0
    second_counter = 0
    frame_counter = 0

    while not window.check_if_closed():

        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        second_counter += delta_time
        frame_counter += 1

        window.refresh(0)

        camera.process_input(window, delta_time)
        camera.testing_commands(window)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture0_ID)

        shader_program.use()

        pos, looking, up = camera.return_vectors()
        view = glm.lookAt(pos, looking, up)
        projection = glm.perspective(glm.radians(45), window.size[0]/window.size[1], 0.1, 100)

        shader_program.set_mat4('view', glm.value_ptr(view))
        shader_program.set_mat4('projection', glm.value_ptr(projection))

        glBindVertexArray(vao)

        for i, offset in enumerate(cube_offsets):

            model = glm.mat4(1.0)
            model = glm.translate(model, offset)

            angle = 20 * i
            model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))

            shader_program.set_mat4('model', glm.value_ptr(model))

            glDrawArrays(GL_TRIANGLES, 0, 36)

        glBindVertexArray(0)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, crosshair_texture_ID)

        shader_program_2d.use()
        glBindVertexArray(vao_2d)
        glPointSize(32)
        glDrawArrays(GL_POINTS, 0, 1)

        if second_counter >= 1:
            print(frame_counter)
            second_counter, frame_counter = 0, 0

        window.refresh(1)

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)

    window.close()

if __name__ == '__main__':
    main()
