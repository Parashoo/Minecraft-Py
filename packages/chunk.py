import numpy as np

class chunk:
    def __init__(self):
        self.data = np.zeros((16, 256, 16), dtype = 'uint8')
        self.remarkable = {'top_non_air_layer': 0, 'bottom_non_opaque_layer': 0, 'corner': [0,0]}

    def from_bytes(self, string):
        raw_data = np.fromstring(bytes(string, 'utf-8'), dtype = 'uint8')
        self.data = raw_data.reshape(16, 256, 16)

    def fill_layers(self,bottom_layer, top_layer, block_type):
        for i in range(top_layer - bottom_layer):
            self.data[:,i + bottom_layer,:] = np.full((16, 16), block_type, dtype = 'uint32')

    def return_if_exposed(self, chunk_coords):
        exposed = True
        x, y, z = chunk_coords
        if not (x == 0 or x == 15 or z == 0 or z == 15 or y == 0 or y == 255):
            neighbours = (self.data[x+1,y,z],
                          self.data[x-1,y,z],
                          self.data[x,y+1,z],
                          self.data[x,y-1,z],
                          self.data[x,y,z+1],
                          self.data[x,y,z-1])
            exposed = 0 in neighbours
        else:
            exposed = True
        return exposed

    def find_highest_non_transparent(self):
        empty_chunk_layer = np.zeros((16,16), dtype = 'uint8')
        for i in range(256):
            if not np.all(self.data[:,255-i,:] == empty_chunk_layer):
                self.remarkable['top_non_air_layer'] = 255-i
                print(255-i)
                break
            else: pass
    
    def return_exposed(self, corner):
        exposed_list = []
        self.find_highest_non_transparent()
        # neighbour_chunks = [world.load_chunk(
        # central core
        print(corner)
        for coords, blocktype in np.ndenumerate(self.data[1:15, 1:self.remarkable['top_non_air_layer'], 1:15]):
            if blocktype == 0:
                pass
            x, y, z = coords
            neighbours = (self.data[x+1, y, z],
                          self.data[x-1, y, z],
                          self.data[x, y+1, z],
                          self.data[x, y-1, z],
                          self.data[x, y, z+1],
                          self.data[x, y, z-1])
            if 0 in neighbours: exposed_list.append((coords[0] + 16 * corner[0], coords[1], coords[2] + 16 * corner[1]))
            print(0 in neighbours)
        return exposed_list
        
