import glm
import numpy as np
import sys, os
import multiprocessing as mp
from PIL import Image
from pathlib import Path
from OpenGL.GL import *
import time

class render:
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
        self.layer_list = layer_list
        self.model_list = model_list
        self.texture = texture
        self.program = program

    def create_from_world(self, coords_list):
        sys.stdout.write("Creating render buffer... ")
        sys.stdout.flush()
        self.fgbuffer, self.bgbuffer = 0, 0
        self.fgarray, self.bgarray = 0, 0
        now = time.time()
        self.render_list = []
        for i in coords_list:
            self.render_list.append([
                render.faces[i[4]][0] ,  render.faces[i[4]][1] ,  render.faces[i[4]][2] ,  render.faces[i[4]][3] , render.faces[i[4]][4] , i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][5] ,  render.faces[i[4]][6] ,  render.faces[i[4]][7] ,  render.faces[i[4]][8] , render.faces[i[4]][9] , i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][10],  render.faces[i[4]][11],  render.faces[i[4]][12],  render.faces[i[4]][13], render.faces[i[4]][14], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][15],  render.faces[i[4]][16],  render.faces[i[4]][17],  render.faces[i[4]][18], render.faces[i[4]][19], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][20],  render.faces[i[4]][21],  render.faces[i[4]][22],  render.faces[i[4]][23], render.faces[i[4]][24], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][25],  render.faces[i[4]][26],  render.faces[i[4]][27],  render.faces[i[4]][28], render.faces[i[4]][29], i[0], i[1], i[2], self.layer_list[self.model_list[i[3]]["textures"][i[4]]]])
        self.render_vbo, self.render_vao = glGenBuffers(1), glGenVertexArrays(1)
        self.render_vbo_2, self.render_vao_2 = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(self.render_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.render_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STREAM_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(32))
        glEnableVertexAttribArray(3)
        glBindVertexArray(self.render_vao_2)
        glBindBuffer(GL_ARRAY_BUFFER, self.render_vbo_2)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STREAM_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(32))
        glEnableVertexAttribArray(3)
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        self.fgbuffer, self.fgarray = self.render_vbo, self.render_vao
        self.bgbuffer, self.bgarray = self.render_vbo_2, self.render_vao_2
        self.time_required = time.time() - now

    def draw_from_chunks(self, array_list, size_list):
        for index, array in enumerate(array_list):
            self.program.use()
            glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
            glBindVertexArray(array)
            glDrawArrays(GL_TRIANGLES, 0, size_list[index])

    def swap_buffers(self):
        auxbuffer, auxarray = self.bgbuffer, self.bgarray
        self.bgbuffer, self.bgarray = self.fgbuffer, self.fgarray
        self.fgbuffer, self.fgarray = auxbuffer, auxarray
        print("Buffers swapped")
        del auxbuffer, auxarray

    def update_bgbuffer(self):
        glBindVertexArray(self.bgarray)
        glBindBuffer(GL_ARRAY_BUFFER, self.bgbuffer)
        glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STREAM_DRAW)

    def draw_buffer(self):
        self.program.use()
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
        glBindVertexArray(self.fgarray)
        glDrawArrays(GL_TRIANGLES, 0, len(self.render_list) * 6)

    def draw_and_update(self):
        draw = mp.Process(target = self.draw_buffer, args = (self.program, self.texture))
        update = mp.Process(target = self.update_bgbuffer, args = ())
        draw.start()
        update.start()

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
