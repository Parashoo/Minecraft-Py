import glm
import numpy as np
import sys
from OpenGL.GL import *

class render:
    def __init__(self, coords_list):
        sys.stdout.write("Creating render buffer... ")
        sys.stdout.flush()
        self.render_list = []
        for i in coords_list:
            self.render_list.append([
                0.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2],
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2],
                0.0,  1.0,  0.0,  1.0, 0.0, i[0], i[1], i[2],
                0.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2],

                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  1.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2],
                1.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2],
                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2],

                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                0.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2],
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                0.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2],
                0.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],

                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                1.0,  1.0,  0.0,  0.0, 0.0, i[0], i[1], i[2],
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  1.0,  1.0, 1.0, i[0], i[1], i[2],
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],

                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  0.0,  1.0, 1.0, i[0], i[1], i[2],
                1.0,  0.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                1.0,  0.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                0.0,  0.0,  1.0,  0.0, 0.0, i[0], i[1], i[2],
                0.0,  0.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],

                0.0,  1.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
                1.0,  1.0,  0.0,  1.0, 1.0, i[0], i[1], i[2],
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                1.0,  1.0,  1.0,  1.0, 0.0, i[0], i[1], i[2],
                0.0,  1.0,  1.0,  0.0, 0.0, i[0], i[1], i[2],
                0.0,  1.0,  0.0,  0.0, 1.0, i[0], i[1], i[2],
            ])

    def create_buffers(self):
        render_vbo, self.render_vao = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(self.render_vao)
        glBindBuffer(GL_ARRAY_BUFFER, render_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        sys.stdout.write("Done\n")
        sys.stdout.flush()

    def draw_buffer(self, program, texture):
        program.use()
        glBindTexture(GL_TEXTURE_2D, texture)
        glBindVertexArray(self.render_vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.render_list) * 36)
