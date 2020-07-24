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
        return self

    def load_neighbours(self, neighbours):
        north_chunk, south_chunk, east_chunk, west_chunk = neighbours
        self.data[:,:,16] = north_chunk[:,:,0]
        self.data[:,:,17] = south_chunk[:,:,15]
        self.data[16,:,:] = east_chunk[0,:,:]
        self.data[17,:,:] = west_chunk[15,:,:]
        self.data[:,256,:] = np.zeros((18, 18), dtype = 'uint8')
        return self

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

def return_chunk_data(corner, data_string):
    target_chunk = chunk()
    target_chunk.load_data(data_string, corner)
    return target_chunk.data
