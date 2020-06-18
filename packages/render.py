import glm
import numpy as np
import sys, os
from PIL import Image
from pathlib import Path
from OpenGL.GL import *

class render:
    def __init__(self, coords_list):
        sys.stdout.write("Creating render buffer... ")
        sys.stdout.flush()
        self.render_list = []
        for num, i in enumerate(coords_list):
            self.render_list.append([
                0.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  0.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2], 1,

                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  1.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2], 1,

                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,

                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,

                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  0.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  1.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,

                0.0,  1.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  0.0,  1.0, 1.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2], 1,
                0.0,  1.0,  0.0,  0.0, 1.0, i[0], i[1], i[2], 1
            ])

    def create_buffers(self):
        render_vbo, self.render_vao = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(self.render_vao)
        glBindBuffer(GL_ARRAY_BUFFER, render_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(32))
        sys.stdout.write("Done\n")
        sys.stdout.flush()

    def draw_buffer(self, program, texture):
        program.use()
        glBindTexture(GL_TEXTURE_2D_ARRAY, texture)
        glBindVertexArray(self.render_vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.render_list) * 36)

def load_all_block_textures(sourcepath):
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
        print(num, texture)
        tex_file = Image.open(texture)
        tex_data = np.array(list(tex_file.getdata()), np.int8)
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, num, 16, 16, 1, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
    glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
    return block_tex_array
