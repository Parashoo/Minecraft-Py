import numpy as np

class chunk:

    """Class that manages data for a 16 * 16 zone in the world."""

    def __init__(self):
        self.data = np.zeros((16, 16, 64))

    def blocks_to_vertices(self):
        texture_coords = [[0, 0], [0, 1], [1, 0], [1, 1]]
        block_coords = [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
        self.vertices = []

        for coords, texture in np.ndenumerate(self.data):
            for i in range(24):
                tci = i % 4 # Texture coordinate index
                self.vertices += [coords[0] + block_coords[i*3], coords[1] + block_coords[i*3+1], coords[2] + block_coords[i*3+2], texture_coords[tci][0], texture_coords[tci][1], texture]




