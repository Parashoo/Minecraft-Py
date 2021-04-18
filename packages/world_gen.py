import numpy as np
from pathlib import Path
import os, sys
import random
from json import dumps, loads
from math import floor
from packages import chunk
from time import time

class world:
    def __init__(self, worldname, *options):
        rootpath = Path(os.path.abspath(os.path.dirname(sys.argv[0])))
        worlddir = rootpath / "world"
        now = time()
        self.world_mode = 'Loading existing world: '
        world_shape = (2, 2)
        if '-t' in options:
            world_shape = (1, 1)
        if not worlddir.exists():
            worlddir.mkdir()
        self.worldpath = worlddir / (worldname+".world")
        if not self.worldpath.exists() or '-o' in options:
            sys.stdout.write("Creating new world...")
            sys.stdout.flush()
            self.world_mode = 'Creating new world: '
            chunk_dict = {}

            world_file = self.worldpath.open('wb')

            writelines_list = []
            line_counter = 0

            for index, stuff in np.ndenumerate(np.zeros(world_shape)):
                index_x, index_z = index[0] - round(world_shape[0]/2), index[1] - round(world_shape[1]/2)
                coords_list = (index_x, index_z)
                new_chunk = chunk.chunk(gen=True)
                writelines_list.append(new_chunk.data.tostring()+'\n'.encode('utf-8'))
                chunk_dict[str(coords_list)] = line_counter
                line_counter += 1
            writelines_list = [(dumps(chunk_dict)+'\n').encode('utf-8')] + writelines_list
            world_file.writelines(writelines_list)
            world_file.close()
        else:
            sys.stdout.write("Loading existing world...")
            sys.stdout.flush()
        with self.worldpath.open('r') as wdata:
            wlines = wdata.readlines()
            self.chunk_dict = loads(wlines[0])
            self.world_lines = wlines[1:]
            sys.stdout.write("Done\n")
            sys.stdout.flush()

        elapsed = time() - now
        self.time_required = [elapsed]
        
    def return_chunk_data(self, corner):
        return np.fromstring(bytes(self.world_lines[self.chunk_dict[str(corner)]][:-1], 'utf-8'), dtype='uint8').reshape(18, 257, 18)
       
    def return_neighbour_slices(self, corner):
        neighbour_corners = [((corner[0], corner[1] + 1), (slice(None), slice(None), 0)),
                             ((corner[0], corner[1] - 1), (slice(None), slice(None), 15)),
                             ((corner[0] + 1, corner[1]), (0, slice(None), slice(None))),
                             ((corner[0] - 1, corner[1]), (15, slice(None), slice(None)))]
        neighbour_slices = []
        for neighbour_corner in neighbour_corners:
            if str(neighbour_corner[0]) in self.chunk_dict.keys():
                neighbour_slices.append(self.return_chunk_data(neighbour_corner[0])[neighbour_corner[1]])
            else:
                neighbour_slices.append(np.zeros((18, 257, 18), dtype = "uint8")[neighbour_corner[1]])
        return neighbour_slices

    def return_all_chunks(self):
        sys.stdout.write("Calculating exposed blocks... ")
        sys.stdout.flush()
        now = time()
        self.chunk_pointer_dict = {}
        self.chunk_list = []
        for index, chunk_info in enumerate(self.chunk_dict.items()):
            self.chunk_list.append(chunk.chunk(self, eval(chunk_info[0])))
            self.chunk_pointer_dict[eval(chunk_info[0])] = index
        self.time_required.append(time() - now)
        sys.stdout.write("Done\n")
        return self.chunk_list

    def return_neighbours(self, corner):
        neighbour_chunk_corners = [
            (corner[0], corner[1] + 1),
            (corner[0], corner[1] - 1),
            (corner[0] + 1, corner[1]),
            (corner[0] - 1, corner[1])]
        neighbours = []
        for neighbour_corner in neighbour_chunk_corners:
            try:
                neighbours.append(chunk.return_chunk_data(corner, self.world_lines[self.chunk_dict[str(neighbour_corner)]][:-1]))
            except KeyError:
                neighbours.append(np.zeros((18, 257, 18), dtype = 'uint8'))

        return neighbours

    def set_block(self, x, y, z, blocktype, render):
        target_chunk = self.return_chunk_containing_block((x, y, z))
        target_chunk.set_block(x % 16, y, z % 16, blocktype, render)
    
    def return_chunk_containing_block(self, coords):
        corner = (coords[0] // 16, coords[2] // 16)
        return self.chunk_list[self.chunk_pointer_dict[corner]]

    def return_time(self):
        return 'Exposed block calculation: {}\n{}{}'.format(self.time_required[1], self.world_mode, self.time_required[0])
