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
        vbo = self.context.buffer(render_list.tobytes())
        vao = self.context.vertex_array(self.program, [(vbo, "3f4 2f4 3f4 1f4 /v", "aPos", "aTexCoord", "cube_coord", "blockType")])            
        print("Success")
        return vbo, vao
       
    def create_buffers_from_world(self, coords_list):
        sys.stdout.write("Creating render buffer... ")
        now = time.time()
        sys.stdout.flush()
        self.render_vbo, self.render_vao, self.render_size = self.create_buffer(coords_list)
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        self.time_required = time.time() - now
    
    def create_buffers_from_chunks(self, chunk_list):
        self.vbo_list, self.vao_list = [], []
        sys.stdout.write("Creating buffers... ")
        sys.stdout.flush()
        now = time.time()
        for index, chunk in enumerate(chunk_list):
            new_vbo, new_vao = self.create_buffer(chunk.exposed_list)
            self.vbo_list.append(new_vbo)
            self.vao_list.append(new_vao)
        self.time_required = time.time() - now
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        return self.vao_list

    def update_buffer(self, pointer, new_data):
        #glBindVertexArray(self.vao_list[pointer])
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo_list[pointer])
        #draw_data = self.generate_vertex_data(new_data)
        #self.sizes_list[pointer] = draw_data.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, 256, 9, None)
        #print(draw_data.size - self.previous_draw_data.size)
        #glBufferSubData(GL_ARRAY_BUFFER, 0, draw_data.nbytes, draw_data)
        #self.previous_draw_data = draw_data

    def draw_from_chunks(self, array_list):
        for index, array in enumerate(self.vao_list):
            array.render()

    def draw_buffer(self): ### DEPRECATED ###
        self.program.use()
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
        glBindVertexArray(self.render_vao)
        glDrawArrays(GL_TRIANGLES, 0, self.render_size * 6)

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
