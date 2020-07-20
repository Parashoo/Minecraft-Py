import numpy as np

class chunk:
    faces = ['east', 'west', 'top', 'bottom', 'north', 'south']
    def __init__(self):
        self.data = np.zeros((18, 257, 18), dtype = 'uint8')
        self.remarkable = {'top_non_air_layer': 0}

    def load_data(self, string):
        raw_data = np.fromstring(bytes(string, 'utf-8'), dtype = 'uint8')
        self.data = raw_data.reshape(18, 257, 18)

    def load_neighbours(self, neighbours):        
        north_chunk, south_chunk, east_chunk, west_chunk = neighbours
        self.data[:,:,16] = north_chunk[:,:,1]
        self.data[:,:,-1] = south_chunk[:,:,15]
        self.data[16,:,:] = east_chunk[0,:,:]
        self.data[-1,:,:] = west_chunk[15,:,:]
        self.data[:,-1,:] = np.zeros((18, 18), dtype = 'uint8')

    def fill_layers(self, bottom_layer, top_layer, block_type):
        for i in range(top_layer - bottom_layer):
            self.data[:16,i+bottom_layer,:16] = np.full((16, 16), block_type, dtype = 'uint32')
    def find_highest_non_transparent(self):
        empty_chunk_layer = np.zeros((16,16), dtype = 'uint8')
        for i in range(256):
            if not np.all(self.data[:,255-i,:] == empty_chunk_layer):
                self.remarkable['top_non_air_layer'] = 255-i
                return 255 - i
                break
            else: pass
    def return_exposed(self, corner):
        exposed_list = []
        for coords, blocktype in np.ndenumerate(self.data[0:15, 0:self.find_highest_non_transparent(), 0:15]):
            print(coords)
            x, y, z = coords
            if blocktype == 0:
                pass
            coords_in_world = (x+16*corner[0], y, z+16*corner[1])
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

def return_chunk_data(line_string):
    target_chunk = chunk()
    target_chunk.load_data(line_string)
    return target_chunk.data
