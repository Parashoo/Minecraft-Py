import sys, os
from pathlib import Path
sys.path.append(Path(os.path.abspath(os.path.dirname(sys.argv[0]))))

if not (Path() / "setup.log").exists():
    import setup
    setup.install_packages()

import glfw
import glm
import numpy as np
import moderngl as mgl
from OpenGL.GL import *
from math import sin, cos
from PIL import Image
from packages import utilities, chunk, render, world_gen, model

rootpath = Path(os.path.abspath(os.path.dirname(sys.argv[0])))
shaderpath = rootpath / "shaders"
texturepath = rootpath / "ressources"
blocktexturepath = texturepath / "block"

vertex_source_3d = shaderpath / "scene.vs"
fragment_source_3d = shaderpath / "scene.fs"
geometry_source_3d = shaderpath / "scene.gs"

with vertex_source_3d.open() as src:
    vertex_source_3d = src.read()
with fragment_source_3d.open() as src:
    fragment_source_3d = src.read()
with geometry_source_3d.open() as src:
    geometry_source_3d = src.read()

vertex_source_GUI = shaderpath / "hud.vs"
fragment_source_GUI = shaderpath / "hud.fs"

with vertex_source_GUI.open() as src:
    vertex_source_GUI = src.read()
with fragment_source_GUI.open() as src:
    fragment_source_GUI = src.read()

vertex_source_sky = shaderpath / "sky.vs"
fragment_source_sky = shaderpath / "sky.fs"

with vertex_source_sky.open() as src:
    vertex_source_sky = src.read()
with fragment_source_sky.open() as src:
    fragment_source_sky = src.read()


camera = utilities.camera((0, 16, 0), (0, 0, 0), (800, 600))

delta_time = 0.0
last_frame = 0.0

def main():

    global delta_time, last_frame

    fps_list = []
    test_world = world_gen.world('__DELETEME__', '-o')
    window = utilities.window()
    camera.setup_window(window)
    ctx = mgl.create_context()

    window.bind_context(ctx)
    ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)
    ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
        
    scene = ctx.program(vertex_shader=vertex_source_3d, fragment_shader=fragment_source_3d, geometry_shader=geometry_source_3d, varyings = ("texture_coord", "texture_layer"))
    hud = ctx.program(vertex_shader=vertex_source_GUI, fragment_shader=fragment_source_GUI)
    sky = ctx.program(vertex_shader=vertex_source_sky, fragment_shader=fragment_source_sky)

    sky_data = np.array([     # Sky
        -1.0, 1.0, 0.0,
         1.0, 1.0, 0.0,
        -1.0,-1.0, 0.0,
         1.0,-1.0, 0.0], dtype = 'float32')

    sky_vbo = ctx.buffer(sky_data)
    sky_vao = ctx.vertex_array(sky, sky_vbo, "aPos")

    crosshair = np.array([0, 0, 0], dtype = 'float32')     # Crosshair

    vbo_2d = ctx.buffer(crosshair)
    vao_2d = ctx.vertex_array(hud, vbo_2d, "aPos")

    crosshair_file = Image.open(texturepath / "icons.png").crop((0,0,16,16))
    crosshair_texture = ctx.texture((16, 16), 4, crosshair_file.tobytes())
    crosshair_texture.filter = (mgl.NEAREST, mgl.NEAREST)

    camera_direction = glm.vec3()
    second_counter = 0
    frame_counter = 0

    all_textures, layers = render.load_all_block_textures(blocktexturepath, ctx)
    all_models = model.load_all(rootpath)

    world_render = render.render(layers, all_models, all_textures, scene, ctx)
    all_chunks = test_world.return_all_chunks()
    chunk_arrays = world_render.create_buffers_from_chunks(all_chunks) 

    last_frame = glfw.get_time()

    while not window.check_if_closed():

        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame
        second_counter += delta_time
        frame_counter += 1

        window.refresh(0, ctx)

        sky['orientation'] = glm.radians(camera.pitch)
        ctx.disable(mgl.DEPTH_TEST)
        sky_vao.render(mode=mgl.TRIANGLE_STRIP)

        camera.process_input(window, delta_time, test_world)
        camera.testing_commands(window)

        pos, looking, up = camera.return_vectors()
        view = glm.lookAt(pos, looking, up)
        projection = glm.perspective(glm.radians(45), window.size[0]/window.size[1], 0.1, 256)
        scene['view'].write(view)
        scene['projection'].write(projection)
        scene['texture0'] = 0
        all_textures.use(location=0)
        
        if glfw.get_key(window.window, glfw.KEY_U) == glfw.PRESS:
            test_world.set_block(int(pos.x), int(pos.y), int(pos.z), 1, world_render)
        ctx.enable(mgl.DEPTH_TEST)
        world_render.draw_from_chunks(all_chunks)

        hud['texture0'] = 0
        crosshair_texture.use(location=0)
        vao_2d.render(mode=mgl.POINTS)

        if second_counter >= 1:
            fps_list.append(frame_counter)
            second_counter, frame_counter = 0, 0
        window.refresh(1, ctx)

    window.close()
    print('\n===== End statistics =====')
    print("Average FPS: {}".format(np.mean(fps_list)))
    print("Render buffer creation: ", world_render.time_required)
    print(test_world.return_time())

if __name__ == '__main__':
    main()
