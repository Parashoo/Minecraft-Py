import numpy as np
import os.path
from json import dumps, loads
from math import floor
from packages import chunk
from time import time

class world:
    def __init__(self, worldname, path, *options):

        now = time()
        self.world_mode = 'Loading existing world: '
        self.wname = path+'/world/'+worldname+'.world'
        if not (os.path.isfile(self.wname) or '-o' in options):
            self.world_mode = 'Creating new world: '
            chunk_dict = {}
            world_file = open(self.wname, 'wb')
            writelines_list = []
            line_counter = 0
            for index, stuff in np.ndenumerate(np.zeros((8, 8))):
                index_x, index_z = index[0] - 4, index[1] - 4
                coords_list = (index_x, index_z)
                new_chunk = chunk.chunk()
                new_chunk.fill_layers(0, index[0] + index[1], 5)
                writelines_list.append(new_chunk.data.tostring()+'\n'.encode('utf-8'))
                chunk_dict[str(coords_list)] = line_counter
                line_counter += 1
            writelines_list = [(dumps(chunk_dict)+'\n').encode('utf-8')] + writelines_list
            world_file.writelines(writelines_list)
            world_file.close()

        with open(self.wname, 'r') as wdata:
            wlines = wdata.readlines()
            self.chunk_dict = loads(wlines[0])
            self.world_lines = wlines[1:]

        elapsed = time() - now
        self.time_required = [elapsed]

    def get_block(self, x, y, z):
        target_chunk = chunk.chunk()
        coords_in_chunk = (x % 16, y, z % 16)
        chunk_coords = [x // 16, z // 16]

        wline = self.chunk_dict[str(chunk_coords)]
        chunk_data = self.world_lines[wline][:-1]
        target_chunk.from_bytes(chunk_data)

        return target_chunk.data[tuple(coords_in_chunk)]
        del target_chunk, chunk_data

    def set_block(self, coords, type):
        target_chunk = chunk.chunk()
        chunk_coords = [coords[0] // 16, coords[2] // 16]
        coords_in_chunk = [i % 16 for i in coords]
        chunk_data = self.world_lines[self.chunk_dict[str(chunk_coords)]][:-1]
        target_chunk.from_bytes(chunk_data)

        target_chunk.data[tuple(coords)] = type
        self.world_lines[self.chunk_dict[str(chunk_coords)]] = '/ch->da:{}\n'.format(target_chunk.data.tobytes())

        with open(self.wname+'.world', 'w') as file:
            file.writelines(self.worldlines)

    def return_all_exposed(self):
        now = time()
        exposed_blocks = []
        for chunk_corner_str, line in self.chunk_dict.items():
            chunk_corner = eval(chunk_corner_str)
            neighbour_lines = {
                    'north': (chunk_corner[0], chunk_corner[1]+1),
                    'south': (chunk_corner[0], chunk_corner[1]-1),
                    'east': (chunk_corner[0]+1, chunk_corner[1]),
                    'west': (chunk_corner[0]-1, chunk_corner[1])}
            neighbours = []
            for direction in neighbour_lines:
                try:
                    neighbours.append(chunk.return_chunk_data(self.world_lines[self.chunk_dict[str(neighbour_lines[direction])]][:-1]))
                except KeyError:
                    neighbours.append(np.zeros((16, 256, 16), dtype = 'uint8'))
            target = chunk.chunk()
            target.from_bytes(self.world_lines[line][:-1])
            exposed_blocks = exposed_blocks + target.return_exposed(chunk_corner, neighbours)
        elapsed = time() - now

        self.time_required.append(elapsed)
        return exposed_blocks

    def return_time(self):
        return 'Exposed block calculation: {}\n{}{}'.format(self.time_required[1], self.world_mode, self.time_required[0])
