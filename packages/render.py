import glm
import numpy as np
import sys, os
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

    def __init__(self, coords_list, layer_list, model_list):
        sys.stdout.write("Creating render buffer... ")
        sys.stdout.flush()
        now = time.time()
        self.render_list = []
        self.layer_list = layer_list
        self.model_list = model_list
        for i in coords_list:
            self.render_list.append([
                render.faces[i[4]][0] ,  render.faces[i[4]][1] ,  render.faces[i[4]][2] ,  render.faces[i[4]][3] , render.faces[i[4]][4] , i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][5] ,  render.faces[i[4]][6] ,  render.faces[i[4]][7] ,  render.faces[i[4]][8] , render.faces[i[4]][9] , i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][10],  render.faces[i[4]][11],  render.faces[i[4]][12],  render.faces[i[4]][13], render.faces[i[4]][14], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][15],  render.faces[i[4]][16],  render.faces[i[4]][17],  render.faces[i[4]][18], render.faces[i[4]][19], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][20],  render.faces[i[4]][21],  render.faces[i[4]][22],  render.faces[i[4]][23], render.faces[i[4]][24], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                render.faces[i[4]][25],  render.faces[i[4]][26],  render.faces[i[4]][27],  render.faces[i[4]][28], render.faces[i[4]][29], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]]])
        self.render_vbo, self.render_vao = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(self.render_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.render_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_DYNAMIC_DRAW)
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
        self.time_required = time.time() - now

    def draw_buffer(self, program, texture):
        program.use()
        glBindTexture(GL_TEXTURE_2D_ARRAY, texture)
        glBindVertexArray(self.render_vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.render_list) * 6)
        
    def update_buffer(self, camera): #TESTING FUNCTION
        glBindBuffer(GL_ARRAY_BUFFER, self.render_vbo_2)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype = 'float32'), GL_DYNAMIC_DRAW)

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
