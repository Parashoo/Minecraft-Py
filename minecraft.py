import glfw
import glm
import numpy as np
from OpenGL.GL import *
from math import sin, cos

import sys, os
from pathlib import Path
sys.path.append(Path(os.path.abspath(os.path.dirname(sys.argv[0]))))
from packages import utilities, chunk, render, world_gen, model

rootpath = Path(os.path.abspath(os.path.dirname(sys.argv[0])))
shaderpath = rootpath / "shaders"
texturepath = rootpath / "ressources"
blocktexturepath = texturepath / "block"

vertex_source_3d = shaderpath / "scene.vs"
fragment_source_3d = shaderpath / "scene.fs"

vertex_source_GUI = shaderpath / "hud.vs"
fragment_source_GUI = shaderpath / "hud.fs"

vertex_source_sky = shaderpath / "sky.vs"
fragment_source_sky = shaderpath / "sky.fs"

camera = utilities.camera((0, 16, 0), (0, 0, 0), (800, 600))

delta_time = 0.0
last_frame = 0.0

def main():

    global delta_time, last_frame

    fps_list = []

    test_world = world_gen.world('__DELETEME__')
    window = utilities.window()
    camera.setup_window(window)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    crosshair = np.array([
      0.0, 0.0, 0.0], dtype = 'float32')

    shader_program_scene = utilities.shader(vertex_source_3d, fragment_source_3d, '450')
    shader_program_scene.compile()

    shader_program_hud = utilities.shader(vertex_source_GUI, fragment_source_GUI, '450')
    shader_program_hud.compile()

    shader_program_sky = utilities.shader(vertex_source_sky, fragment_source_sky, '450')
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

    crosshair_texture = utilities.texture(texturepath / "icons.png", crop = (0,0,16,16))
    crosshair_texture_ID = crosshair_texture.gen_texture()

    exposed_list = test_world.return_all_exposed()

    shader_program_scene.use()
    shader_program_scene.set_int('texture0', 0)

    shader_program_hud.use()
    shader_program_hud.set_int('texture0', 0)

    camera_direction = glm.vec3()
    second_counter = 0
    frame_counter = 0

    all_textures, layers = render.load_all_block_textures(blocktexturepath)
    all_models = model.load_all(rootpath)

    world_render = render.render(exposed_list, layers, all_models)

    while not window.check_if_closed():

        current_frame = glfw.get_time()
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

        shader_program_scene.use()

        pos, looking, up = camera.return_vectors()
        view = glm.lookAt(pos, looking, up)
        projection = glm.perspective(glm.radians(45), window.size[0]/window.size[1], 0.1, 256)
        shader_program_scene.set_mat4('view', glm.value_ptr(view))
        shader_program_scene.set_mat4('projection', glm.value_ptr(projection))

        glEnable(GL_DEPTH_TEST)
        world_render.draw_buffer(shader_program_scene, all_textures)
        if glfw.get_key(window.window, glfw.KEY_U) == glfw.PRESS:
            world_render.update_buffer(camera)

        glBindVertexArray(0)


        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, crosshair_texture_ID)

        shader_program_hud.use()


        glBindVertexArray(vao_2d)
        glPointSize(32)
        glDrawArrays(GL_POINTS, 0, 1)

        if second_counter >= 1:
            fps_list.append(frame_counter)
            second_counter, frame_counter = 0, 0
        window.refresh(1)

    window.close()
    print('\n===== End statistics =====')
    print("Average FPS: {}".format(np.mean(fps_list)))
    print("Render buffer creation: ", world_render.time_required)
    print(test_world.return_time())

if __name__ == '__main__':
    main()
