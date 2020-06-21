import numpy as np

class chunk:
    def __init__(self):
        self.data = np.zeros((16, 256, 16), dtype = 'uint8')
        self.remarkable = {'top_non_air_layer': 0}

    def from_bytes(self, string):
        raw_data = np.fromstring(bytes(string, 'utf-8'), dtype = 'uint8')
        self.data = raw_data.reshape(16, 256, 16)

    def fill_layers(self, bottom_layer, top_layer, block_type):
        for i in range(top_layer - bottom_layer):
            self.data[:,i+bottom_layer,:] = np.full((16, 16), block_type, dtype = 'uint32')

    def find_highest_non_transparent(self):
        empty_chunk_layer = np.zeros((16,16), dtype = 'uint8')
        for i in range(256):
            if not np.all(self.data[:,255-i,:] == empty_chunk_layer):
                self.remarkable['top_non_air_layer'] = 255-i
                break
            else: pass

    def return_exposed(self, corner, neighbours):
        exposed_list = []
        self.find_highest_non_transparent()
        north_chunk, south_chunk, east_chunk, west_chunk = neighbours

        edge = [0,0,0,0]
        chunk_slice = self.data[:,0:self.remarkable['top_non_air_layer']+1,:]
        for coords, blocktype in np.ndenumerate(chunk_slice):
            x, y, z = coords
            coords_in_world = (coords[0]+16*corner[0], coords[1], coords[2]+16*corner[1])
            try:
                neighbours = [self.data[x+1, y, z],
                              self.data[x-1, y, z],
                              self.data[x, y+1, z],
                              self.data[x, y-1, z],
                              self.data[x, y, z+1],
                              self.data[x, y, z-1]]
            except IndexError:
                if x == 15 and not z == 15: # 256
                    neighbours = [east_chunk[0, y, z],
                                  self.data[x-1, y, z],
                                  self.data[x, y+1, z],
                                  self.data[x, y-1, z],
                                  self.data[x, y, z+1],
                                  self.data[x, y, z-1]]
                if z == 15 and not x == 15: # 256
                    neighbours = [self.data[x+1, y, z],
                                  self.data[x-1, y, z],
                                  self.data[x, y+1, z],
                                  self.data[x, y-1, z],
                                  north_chunk[x, y, 0],
                                  self.data[x, y, z-1]]
                if x == 15 and z == 15:
                    neighbours = [east_chunk[0, y, z],
                                  self.data[x-1, y, z],
                                  self.data[x, y+1, z],
                                  self.data[x, y-1, z],
                                  north_chunk[x, y, 0],
                                  self.data[x, y, z-1]]
            if y == 0:
                neighbours[3] = 0
            if z == 0:
                neighbours[5] = south_chunk[x, y, 15]
            if x == 0:
                neighbours[1] = west_chunk[15, y, z]
            if 0 in neighbours:
                exposed_list.append(coords_in_world + tuple([blocktype]))
            neighbours = []
        return exposed_list

def return_chunk_data(line_string):
    target_chunk = chunk()
    target_chunk.from_bytes(line_string)
    return target_chunk.data
