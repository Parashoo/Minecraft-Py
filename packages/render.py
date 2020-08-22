import glm
import numpy as np
import sys, os
import multiprocessing as mp
from PIL import Image
from pathlib import Path
from OpenGL.GL import *
import time

class render:
    """
    Class that manages VBO and VAO creation, as well as drawing these.
    """
    faces = {
            "south": [
              0.0,  0.0,  0.0,  1.0, 1.0,
              1.0,  0.0,  0.0,  0.0, 1.0,
              1.0,  1.0,  0.0,  0.0, 0.0,
              1.0,  1.0,  0.0,  0.0, 0.0,
              0.0,  1.0,  0.0,  1.0, 0.0,
              0.0,  0.0,  0.0,  1.0, 1.0],

            "north": [
              0.0,  0.0,  1.0,  1.0, 1.0,
              1.0,  0.0,  1.0,  0.0, 1.0,
              1.0,  1.0,  1.0,  0.0, 0.0,
              1.0,  1.0,  1.0,  0.0, 0.0,
              0.0,  1.0,  1.0,  1.0, 0.0,
              0.0,  0.0,  1.0,  1.0, 1.0],

            "west": [
              0.0,  1.0,  1.0,  1.0, 0.0,
              0.0,  1.0,  0.0,  0.0, 0.0,
              0.0,  0.0,  0.0,  0.0, 1.0,
              0.0,  0.0,  0.0,  0.0, 1.0,
              0.0,  0.0,  1.0,  1.0, 1.0,
              0.0,  1.0,  1.0,  1.0, 0.0],

            "east": [
              1.0,  1.0,  1.0,  1.0, 0.0,
              1.0,  1.0,  0.0,  0.0, 0.0,
              1.0,  0.0,  0.0,  0.0, 1.0,
              1.0,  0.0,  0.0,  0.0, 1.0,
              1.0,  0.0,  1.0,  1.0, 1.0,
              1.0,  1.0,  1.0,  1.0, 0.0],

            "bottom": [
              0.0,  0.0,  0.0,  0.0, 1.0,
              1.0,  0.0,  0.0,  1.0, 1.0,
              1.0,  0.0,  1.0,  1.0, 0.0,
              1.0,  0.0,  1.0,  1.0, 0.0,
              0.0,  0.0,  1.0,  0.0, 0.0,
              0.0,  0.0,  0.0,  0.0, 1.0],

            "top": [
              0.0,  1.0,  0.0,  0.0, 1.0,
              1.0,  1.0,  0.0,  1.0, 1.0,
              1.0,  1.0,  1.0,  1.0, 0.0,
              1.0,  1.0,  1.0,  1.0, 0.0,
              0.0,  1.0,  1.0,  0.0, 0.0,
              0.0,  1.0,  0.0,  0.0, 1.0]
             }

    def __init__(self, layer_list, model_list, texture, program):
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

    def generate_vertex_data(self, data):
        render_list = []
        for i in data:
            render_list.append([
                render.faces[i[4]][0] ,  render.faces[i[4]][1] ,  render.faces[i[4]][2] ,  render.faces[i[4]][3] , render.faces[i[4]][4] , i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][5] ,  render.faces[i[4]][6] ,  render.faces[i[4]][7] ,  render.faces[i[4]][8] , render.faces[i[4]][9] , i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][10],  render.faces[i[4]][11],  render.faces[i[4]][12],  render.faces[i[4]][13], render.faces[i[4]][14], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][15],  render.faces[i[4]][16],  render.faces[i[4]][17],  render.faces[i[4]][18], render.faces[i[4]][19], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][20],  render.faces[i[4]][21],  render.faces[i[4]][22],  render.faces[i[4]][23], render.faces[i[4]][24], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][25],  render.faces[i[4]][26],  render.faces[i[4]][27],  render.faces[i[4]][28], render.faces[i[4]][29], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]]])
        return np.array(render_list, dtype = "float32")

    def create_buffer(self, data):
        """
        Create a VBO and a VAO for the data passed as argument.
        data should be a list of faces and coordinates structured as returned by chunk.return_neighbours().
        Returns pointers to the buffer and array created, as well as the size of the buffer created (for drawing purposes).
        """
        render_list = self.generate_vertex_data(data)
        vbo, vao = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, render_list, GL_STREAM_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0)) # Model space
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12)) # Texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(20)) # World space
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(32)) # Texture array index
        glEnableVertexAttribArray(3)
        return vbo, vao, len(render_list) * 6, render_list
       
    def create_buffers_from_world(self, coords_list):
        sys.stdout.write("Creating render buffer... ")
        now = time.time()
        sys.stdout.flush()
        self.render_vbo, self.render_vao, self.render_size = self.create_buffer(coords_list)
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        self.time_required = time.time() - now
    
    def create_buffers_from_chunks(self, chunk_list):
        self.vbo_list, self.vao_list, self.sizes_list, self.data_list = [], [], [], []
        sys.stdout.write("Creating buffers... ")
        sys.stdout.flush()
        now = time.time()
        for index, chunk in enumerate(chunk_list):
            new_vbo, new_vao, new_size, new_render_list = self.create_buffer(chunk.exposed_list)
            self.vbo_list.append(new_vbo)
            self.vao_list.append(new_vao)
            self.sizes_list.append(new_size)
            self.data_list.append(new_render_list)
            chunk.GL_pointer = index

        self.time_required = time.time() - now
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        return self.vao_list, self.sizes_list
    
    def update_buffer(self, pointer, new_data):
        glBindVertexArray(self.vao_list[pointer])
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_list[pointer])
        draw_data = self.generate_vertex_data(new_data)
        draw_data.dtype = "uint8"
        #glInvalidateBufferSubData(self.vbo_list[0], 0, glGetBufferParameteriv(GL_ARRAY_BUFFER, GL_BUFFER_SIZE))
        glBufferData(GL_ARRAY_BUFFER, np.array(draw_data), GL_DYNAMIC_DRAW)

    def draw_from_chunks(self, array_list, size_list):
        for index, array in enumerate(array_list):
            self.program.use()
            glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
            glBindVertexArray(array)
            glDrawArrays(GL_TRIANGLES, 0, size_list[index])

    def draw_buffer(self): ### DEPRECATED ###
        self.program.use()
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
        glBindVertexArray(self.render_vao)
        glDrawArrays(GL_TRIANGLES, 0, self.render_size * 6)

def load_all_block_textures(sourcepath):
    layer_list = {}
    block_tex_array = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D_ARRAY, block_tex_array)
    glTexStorage3D(GL_TEXTURE_2D_ARRAY,
      3, #Max mipmap level
      GL_RGBA8, #File format
      16, 16, #Image size
      20 #Layer count
    )
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)
    for num, texture in enumerate(sourcepath.iterdir()):
        tex_file = Image.open(texture)
        tex_data = np.array(list(tex_file.getdata()), np.int8)
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, num, 16, 16, 1, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
        layer_list.update({str(texture)[len(str(sourcepath))+1:]: num})
    glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
    return block_tex_array, layer_list
