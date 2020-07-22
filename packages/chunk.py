import numpy as np
import time
from OpenGL.GL import *

class chunk:
    faces = ['east', 'west', 'top', 'bottom', 'north', 'south']
    def __init__(self):
        self.data = np.zeros((18, 257, 18), dtype = 'uint8')

    def load_data(self, string, corner):
        raw_data = np.fromstring(bytes(string, 'utf-8'), dtype = 'uint8')
        self.data = raw_data.reshape(18, 257, 18)
        self.corner = corner

    def load_neighbours(self, neighbours):
        north_chunk, south_chunk, east_chunk, west_chunk = neighbours
        self.data[:,:,16] = north_chunk[:,:,0]
        self.data[:,:,17] = south_chunk[:,:,15]
        self.data[16,:,:] = east_chunk[0,:,:]
        self.data[17,:,:] = west_chunk[15,:,:]
        self.data[:,256,:] = np.zeros((18, 18), dtype = 'uint8')

    def fill_layers(self, bottom_layer, top_layer, block_type):
        for i in range(top_layer - bottom_layer):
            self.data[:16,i+bottom_layer,:16] = np.full((16, 16), block_type, dtype = 'uint32')

    def return_exposed(self):
        empty_chunk_layer = np.zeros((16,16), dtype = 'uint8')
        self.top_block_layer = 0
        for i in range(256):
            if not np.all(self.data[:16,255-i,:16] == empty_chunk_layer):
                self.top_block_layer = 255-i
                break
            else: pass
        exposed_list = []
        for coords, blocktype in np.ndenumerate(self.data[0:16, 0:self.top_block_layer+1, 0:16]):
            x, y, z = coords
            if blocktype == 0:
                pass
            print(x, z, self.corner)
            coords_in_world = (x+16*self.corner[0], y, z+16*self.corner[1])
            neighbours = [self.data[x+1, y, z],
                          self.data[x-1, y, z],
                          self.data[x, y+1, z],
                          self.data[x, y-1, z],
                          self.data[x, y, z+1],
                          self.data[x, y, z-1]]
            exposed_faces = [index for index, item in enumerate(neighbours) if item == 0]
            for i in exposed_faces:
                exposed_list.append(coords_in_world + (blocktype,) + (chunk.faces[i],))
            neighbours = []
        return exposed_list

    def chunk_render(self, layer_list, model_list):
        exposed_blocks = self.return_exposed()
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

        now = time.time()
        self.render_list = []
        self.layer_list = layer_list
        self.model_list = model_list
        for i in exposed_blocks:
            self.render_list.append([
                faces[i[4]][0] ,  faces[i[4]][1] ,  faces[i[4]][2] ,  faces[i[4]][3] , faces[i[4]][4] , i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                faces[i[4]][5] ,  faces[i[4]][6] ,  faces[i[4]][7] ,  faces[i[4]][8] , faces[i[4]][9] , i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                faces[i[4]][10],  faces[i[4]][11],  faces[i[4]][12],  faces[i[4]][13], faces[i[4]][14], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                faces[i[4]][15],  faces[i[4]][16],  faces[i[4]][17],  faces[i[4]][18], faces[i[4]][19], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                faces[i[4]][20],  faces[i[4]][21],  faces[i[4]][22],  faces[i[4]][23], faces[i[4]][24], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]],
                faces[i[4]][25],  faces[i[4]][26],  faces[i[4]][27],  faces[i[4]][28], faces[i[4]][29], i[0], i[1], i[2], layer_list[model_list[i[3]]["textures"][i[4]]]])
        render_vbo, render_vao = glGenBuffers(1), glGenVertexArrays(1)
        glBindVertexArray(render_vao)
        glBindBuffer(GL_ARRAY_BUFFER, render_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.render_list, dtype='float32'), GL_STREAM_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(32))
        glEnableVertexAttribArray(3)
        
        return render_vbo, render_vao, len(self.render_list) * 6


def return_chunk_data(corner, data_string):
    target_chunk = chunk()
    target_chunk.load_data(data_string, corner)
    return target_chunk.data
