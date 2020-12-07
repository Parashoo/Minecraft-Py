import glm
import numpy as np
import sys, os

from PIL import Image
from pathlib import Path
import moderngl as mgl
import time
import ctypes

class render:
    """
    Class that manages VBO and VAO creation, as well as drawing these.
    """
    model_faces = {
        0: "north",
        1: "south",
        2: "east",
        3: "west",
        4: "top",
        5: "bottom",
    }
    faces = {
            0: [
              1.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  0.0,  1.0,
              0.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  1.0,  1.0],

            1: [
              0.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  0.0,  0.0,
              1.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  1.0,  0.0],

            2: [
              1.0,  0.0,  0.0,
              1.0,  1.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  1.0],

            3: [
              0.0,  0.0,  1.0,
              0.0,  1.0,  1.0,
              0.0,  0.0,  0.0,
              0.0,  0.0,  0.0,
              0.0,  1.0,  1.0,
              0.0,  1.0,  0.0],

            4: [
              0.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  1.0],

            5: [
              0.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  0.0]

             }

    def __init__(self, layer_list, model_list, texture, program, context):
        """
        Initialization of a render class.
        Required arguments:
            - layer_list: a list containing pointers for the GL_TEXTURE_2D_ARRAY's layers.
            - model_list: a list containing block models.
            - texture: a pointer to the GL_TEXTURE_2D_ARRAY mentioned above.
            - program: the shader program to be used.
        """
        self.layer_list = layer_list
        self.model_list = model_list
        self.texture = texture
        self.program = program
        self.context = context
        self.previous_draw_data = np.array([], dtype = "float32")

    def create_buffer(self, data):
        """ Create a VBO and a VAO for the data passed as argument.
        data should be a list of faces and coordinates structured as returned by chunk.return_neighbours().
        Returns pointers to the buffer and array created, as well as the size of the buffer created (for drawing purposes).
        """
        render_list = data.flatten()
        vbo = self.context.buffer(render_list)
        vao = self.context.vertex_array(self.program, [(vbo, "1i2 /v", "blocktype")])
        return vbo, vao

    def create_buffers_from_chunks(self, chunk_list):
        self.vbo_list, self.vao_list, self.corner_list = [], [], []
        sys.stdout.write("Creating buffers... ")
        sys.stdout.flush()
        now = time.time()
        for index, chunk in enumerate(chunk_list):
            print("Buffering chunk ", index)
            new_vbo, new_vao = self.create_buffer(chunk.render_array)
            self.vbo_list.append(new_vbo)
            self.vao_list.append(new_vao)
            self.corner_list.append(chunk.corner)
            chunk.GL_pointer = index
        self.time_required = time.time() - now
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        return self.vao_list

    def update_buffer(self, pointer, new_data, top, corner):
        data = np.array(self.generate_vertex_data(new_data, top, corner), dtype="float32")
        print("Updating buffer")
        self.vbo_list[pointer].orphan(data.nbytes)
        self.vbo_list[pointer].write(data)

    def draw_from_chunks(self, array_list):
        for index, array in enumerate(self.vao_list):
            self.program['corner'] = self.corner_list[index]
            array.render(mode=mgl.POINTS)

def load_all_block_textures(sourcepath, context):
    layer_list = {}
    texture_list = []

    for num, texture in enumerate(sourcepath.iterdir()):
        tex_file = Image.open(texture)
        texture_list.append(list(tex_file.getdata()))
        layer_list.update({str(texture)[len(str(sourcepath))+1:]: num})
    texture_array_data = np.array(texture_list, dtype = "uint8")
    block_tex_array = context.texture_array((16, 16, len(texture_list)), 4, texture_array_data)
    block_tex_array.build_mipmaps()
    block_tex_array.filter = (mgl.LINEAR_MIPMAP_NEAREST, mgl.NEAREST)
    return block_tex_array, layer_list
