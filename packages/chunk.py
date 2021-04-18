import numpy as np
import time
import random

class chunk:

    faces = {
            0: [ #north
              1.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  0.0,  1.0,
              0.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  1.0,  1.0],

            1: [ #south
              0.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  0.0,  0.0,
              1.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  1.0,  0.0],

            2: [ #east
              1.0,  0.0,  0.0,
              1.0,  1.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  1.0],

            3: [ #west
              0.0,  0.0,  1.0,
              0.0,  1.0,  1.0,
              0.0,  0.0,  0.0,
              0.0,  0.0,  0.0,
              0.0,  1.0,  1.0,
              0.0,  1.0,  0.0],

            4: [ #top
              0.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  1.0],

            5: [ #bottom
              0.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  0.0]

             }

    indices = np.array([[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], dtype = "int8")
    def __init__(self, *args, gen=False, empty=False):
        if empty:
            self.data = np.zeros((18, 257, 18), dtype="uint8")
        if gen:
            self.data = np.zeros((18, 257, 18), dtype="uint8")
            self.blocktype = 2
            self.fill_layers(0, random.randint(1, 16), 3)
        else:
            world = args[0]
            self.corner = args[1]
            self.data = world.return_chunk_data(self.corner)
            self.data[:,:,16], self.data[:,:,17], self.data[16,:,:], self.data[17,:,:] = world.return_neighbour_slices(self.corner)
            self.GL_pointer = None
            self.vbo = None
            self.vao = None
            self.render_array = np.zeros((16, 257, 16, 6), dtype = "int16")
    
    def gen_vertex_data(self):
        self.vertex_data = np.zeros((16 * 256 * 16 * 6 * 6, 6), dtype = "float32")
        counter = 0
        for index, block in np.ndenumerate(self.data[:16, :256, :16]):
            x, y, z = index
            neighbours = [self.data[x, y, z+1],
                          self.data[x, y, z-1],
                          self.data[x+1, y, z],
                          self.data[x-1, y, z],
                          self.data[x, y+1, z],
                          self.data[x, y-1, z],
            ]
            for i, blocktype in enumerate(neighbours):
                outputtype = block
                if blocktype != 0:
                    outputtype = 0
                self.vertex_data[counter+0, :] = [x + self.corner[0] * 16 + chunk.faces[i][0], y + chunk.faces[i][1], z + self.corner[1] * 16 + chunk.faces[i][2], 0, 0, outputtype]
                self.vertex_data[counter+1, :] = [x + self.corner[0] * 16 + chunk.faces[i][3], y + chunk.faces[i][4], z + self.corner[1] * 16 + chunk.faces[i][5], 0, 1, outputtype]
                self.vertex_data[counter+2, :] = [x + self.corner[0] * 16 + chunk.faces[i][6], y + chunk.faces[i][7], z + self.corner[1] * 16 + chunk.faces[i][8], 1, 0, outputtype]
                self.vertex_data[counter+3, :] = [x + self.corner[0] * 16 + chunk.faces[i][9], y + chunk.faces[i][10], z + self.corner[1] * 16 + chunk.faces[i][11], 1, 0, outputtype]
                self.vertex_data[counter+4, :] = [x + self.corner[0] * 16 + chunk.faces[i][12], y + chunk.faces[i][13], z + self.corner[1] * 16 + chunk.faces[i][14], 0, 1, outputtype]
                self.vertex_data[counter+5 ,:] = [x + self.corner[0] * 16 + chunk.faces[i][15], y + chunk.faces[i][16], z + self.corner[1] * 16 + chunk.faces[i][17], 1, 1, outputtype]

                counter += 6
        return self.vertex_data

    def fill_layers(self, bottom_layer, top_layer, block_type):
        for i in range(top_layer - bottom_layer):
            self.data[:16,i+bottom_layer,:16] = np.full((16, 16), self.blocktype, dtype = 'uint8')
    
    def set_block(self, x, y, z, block_type, render):
        self.data[x, y, z] = block_type
        print("Updating")
        count = x * 256 * 16 * 6
        for i in range(36):
            print(self.vertex_data[count + i, 5])
            if self.vertex_data[count + i, 5] == 0:
                print("Face added")
                self.vertex_data[count + i, 5] = block_type
            elif self.vertex_data[count + i, 5] != 0:
                print("Face removed")
                self.vertex_data[count + i, 5] = 0
        render.vbo_list[self.GL_pointer].orphan(self.vertex_data.nbytes)
        render.vbo_list[self.GL_pointer].write(self.vertex_data)
        

