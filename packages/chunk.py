import numpy as np

class chunk:
    def __init__(self, coords):
        self.data = np.zeros((16, 256, 16), dtype = 'uint32')
        self.corner = np.array(coords)
        
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
        






