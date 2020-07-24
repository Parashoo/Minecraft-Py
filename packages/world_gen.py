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

            for index, stuff in np.ndenumerate(np.zeros((8, 8))):
                index_x, index_z = index[0] - 4, index[1] - 4
                coords_list = (index_x, index_z)
                new_chunk = chunk.chunk()
                new_chunk.fill_layers(0, random.randint(1, 16), 3)
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

    def return_all_chunk_data(self):
        now = time()
        chunk_data_list = [chunk.chunk().load_data(self.world_lines[chunk_line][:-1], eval(chunk_corner_str)).load_neighbours(self.return_neighbours(eval(chunk_corner_str))).return_exposed() for chunk_corner_str, chunk_line in self.chunk_dict.items()]
        self.time_required.append(time() - now)
        return chunk_data_list

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
    
    def return_all_exposed(self):
        now = time()
        sys.stdout.write("Calculating exposed blocks... ")
        sys.stdout.flush()
        exposed_blocks = []
        for chunk_corner_str, line in self.chunk_dict.items():
            chunk_corner = eval(chunk_corner_str)
            neighbour_chunk_lines = [
                    (chunk_corner[0], chunk_corner[1]+1),
                    (chunk_corner[0], chunk_corner[1]-1),
                    (chunk_corner[0]+1, chunk_corner[1]),
                    (chunk_corner[0]-1, chunk_corner[1])]
            neighbours = self.return_neighbours(chunk_corner)
            target = chunk.chunk()
            target.load_data(self.world_lines[line][:-1], chunk_corner)
            target.load_neighbours(neighbours)
            exposed_blocks = exposed_blocks + target.return_exposed()
        elapsed = time() - now
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        self.time_required.append(elapsed)
        return exposed_blocks

    def return_time(self):
        return 'Exposed block calculation: {}\n{}{}'.format(self.time_required[1], self.world_mode, self.time_required[0])
