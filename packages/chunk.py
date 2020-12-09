import numpy as np
import time
import random

class chunk:
    indices = np.array([[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], dtype = "int8")
    def __init__(self, *args, gen=False):
        if gen:
            self.data = np.zeros((18, 257, 18), dtype="uint8")
            self.fill_layers(1, random.randint(1, 16), 9)
        else:
            world = args[0]
            self.corner = args[1]
            self.data = world.return_chunk_data(self.corner)
            self.data[:,:,16], self.data[:,:,17], self.data[16,:,:], self.data[17,:,:] = world.return_neighbour_slices(self.corner)
            self.GL_pointer = None
            self.render_array = np.zeros((16, 256, 16, 6), dtype = "int16")

    def fill_layers(self, bottom_layer, top_layer, block_type):
        for i in range(top_layer + 1 - bottom_layer):
            self.data[:16,i+bottom_layer,:16] = np.full((16, 16), block_type, dtype = 'uint8')

    def add_remove_faces(self, coords, blocktype, renderer):
        self.data[coords] = blocktype
        x, y, z = coords[0], coords[1], coords[2]
        coords_in_world = (x+16*self.corner[0], y, z+16*self.corner[1])
        neighbours = [self.data[tuple([x, y, z] + chunk.indices[i])] for i in range(6)]
        for index, i in enumerate(neighbours):
            if i == 0:
                print("Adding face")
                self.render_array[x, y, z, index] = blocktype
                continue
            if i != 0 and self.render_array[x, y, z, index] != 0:
                print("Removing face")
                self.render_array[x, y, z, index] = 0
            if i != 0 and self.render_array[x + chunk.indices[index][0], y + chunk.indices[index][1], z + chunk.indices[index][2], 2*(index % 2 == 0) - 1] != 0:
                print("Removing opposite face")
                self.render_array[x + chunk.indices[index][0], y + chunk.indices[index][1], z + chunk.indices[index][2], 2*(index % 2 == 0) - 1] = 0
        renderer.update_buffer(self.GL_pointer, self.render_array, self.top_block_layer, self.corner)

    def return_exposed(self):
        print(self.corner)
        self.top_block_layer = 0
        for i in range(256):
            if not np.all(self.data[:16,255-i,:16] == np.zeros((16, 16), dtype = 'uint8')):
                self.top_block_layer = 256-i
                break
            else: continue
        for coords, blocktype in np.ndenumerate(self.data[0:16, 0:self.top_block_layer+1, 0:16]):
            x, y, z = coords
            if blocktype == 0:
                continue
            coords_in_world = (x+16*self.corner[0], y, z+16*self.corner[1])
            neighbours = [self.data[tuple([x, y, z] + chunk.indices[i])] for i in range(6)]
            for index, item in enumerate(neighbours):
                if item == 0: self.render_array[x, y, z, index] = blocktype
        return self
    
    def return_exposed_t(self, ctx):

        dummy = ctx.buffer(reserve = 16 * 256 * 16)
