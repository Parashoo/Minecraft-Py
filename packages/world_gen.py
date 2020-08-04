import numpy as np
from pathlib import Path
import os, sys
import random
from json import dumps, loads
from math import floor
from packages import chunk
from time import time

class world:
    """
    Class that handles world generation and world reading
    """
    def __init__(self, worldname, *options):
        """
        world.world() takes 1 argument:
          - worldname: name of the world to be created or read. This will search for a file named [worldname].world; if it exists, it will open it and read its contents, otherwise it will generate a new world with that name.
        Additionally, world.world() may take the following option:
          - [-o] will force generation of a new world, overwriting any with the same name.
        """
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
            chunk_array = np.full((10, 10), -1, dtype = "int32") # Create array keeping track of lines at which chunk data is located

            world_file = self.worldpath.open('wb')

            writelines_list = []
            line_counter = 0

            for index in np.ndindex(8, 8):
                new_chunk = chunk.chunk(gen=True)
                writelines_list.append(new_chunk.data.tobytes())
                chunk_array[index[0]+1, index[1]+1] = line_counter
                line_counter += 1
                print(index, line_counter)
            writelines_list = [chunk_array.tobytes()]+ writelines_list
            world_file.write(">end>".encode('utf-8').join(writelines_list))
            world_file.close()
            print(chunk_array)
        else:
            sys.stdout.write("Loading existing world...")
            sys.stdout.flush()
        with self.worldpath.open('rb') as wdata:
            wlines = wdata.read().split(">end>".encode('utf-8'))
            self.chunk_array = np.fromstring(wlines[0], dtype="int32").reshape(10, 10)
            self.world_lines = wlines[1:]
            sys.stdout.write("Done\n")
            sys.stdout.flush()

        elapsed = time() - now
        self.time_required = [elapsed]

    def return_chunk_data(self, corner):
        if self.chunk_array[corner] == -1:
            return np.zeros((18, 257, 18), dtype="uint8")
        else: 
            return np.fromstring(self.world_lines[self.chunk_array[corner]], dtype='uint8').reshape(18, 257, 18)
        
       
    def return_neighbour_slices(self, corner):
        return [
          self.return_chunk_data((corner[0], corner[1] + 1))[:16,:,0],
          self.return_chunk_data((corner[0], corner[1] - 1))[:16,:,15],
          self.return_chunk_data((corner[0] + 1, corner[1]))[0,:,:16],
          self.return_chunk_data((corner[0] - 1, corner[1]))[15,:,:16]
        ]

    def return_all_chunks(self):
        sys.stdout.write("Calculating exposed blocks... ")
        sys.stdout.flush()
        now = time()
        self.chunk_list = []
        for corner in np.ndindex(8, 8):
            new_chunk = chunk.chunk(self, corner)
            self.chunk_list.append(new_chunk.return_exposed())
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
                neighbours.append(chunk.return_chunk_data(corner, self.world_lines[self.chunk_array[str(neighbour_corner)]][:-1]))
            except KeyError:
                neighbours.append(np.zeros((18, 257, 18), dtype = 'uint8'))

        return neighbours

    def return_all_exposed(self):
        now = time()
        sys.stdout.write("Calculating exposed blocks... ")
        sys.stdout.flush()
        exposed_blocks = []
        for chunk_corner_str, line in self.chunk_array.items():
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
