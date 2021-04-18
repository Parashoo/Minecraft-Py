import glm
import numpy as np
import sys, os

from PIL import Image
from pathlib import Path
import moderngl as mgl
import time
import ctypes

class render:
    """
    Class that manages VBO and VAO creation, as well as drawing these.
    """
    model_faces = {
        0: "north",
        1: "south",
        2: "east",
        3: "west",
        4: "top",
        5: "bottom",
    }
    faces = {
            0: [
              1.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  0.0,  1.0,
              0.0,  0.0,  1.0,
              1.0,  1.0,  1.0,
              0.0,  1.0,  1.0],

            1: [
              0.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  0.0,  0.0,
              1.0,  0.0,  0.0,
              0.0,  1.0,  0.0,
              1.0,  1.0,  0.0],

            2: [
              1.0,  0.0,  0.0,
              1.0,  1.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  1.0],

            3: [
              0.0,  0.0,  1.0,
              0.0,  1.0,  1.0,
              0.0,  0.0,  0.0,
              0.0,  0.0,  0.0,
              0.0,  1.0,  1.0,
              0.0,  1.0,  0.0],

            4: [
              0.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  0.0,
              1.0,  1.0,  0.0,
              0.0,  1.0,  1.0,
              1.0,  1.0,  1.0],

            5: [
              0.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  1.0,
              1.0,  0.0,  1.0,
              0.0,  0.0,  0.0,
              1.0,  0.0,  0.0]

             }

    def __init__(self, layer_list, model_list, texture, program, context):
        """
        Initialization of a render class.
        Required arguments:
            - layer_list: a list containing pointers for the GL_TEXTURE_2D_ARRAY's layers.
            - model_list: a list containing block models.
            - texture: a pointer to the GL_TEXTURE_2D_ARRAY mentioned above.
            - program: the shader program to be used.
        """
        self.layer_list = layer_list
        self.model_list = model_list
        self.texture = texture
        self.program = program
        self.context = context
        self.previous_draw_data = np.array([], dtype = "float32")

    def generate_face_data(self, face, corner):
        now = time.time()
        x, y, z = face[0] + corner[0] *16, face[1], face[2] + corner[1] * 16
        face_vertex_data = [
        render.faces[face[4]][0] + x,  render.faces[face[4]][1] + y,  render.faces[face[4]][2] + z,  0.0, 1.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]],
        render.faces[face[4]][3] + x,  render.faces[face[4]][4] + y,  render.faces[face[4]][5] + z,  0.0, 0.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]],
        render.faces[face[4]][6] + x,  render.faces[face[4]][7] + y,  render.faces[face[4]][8] + z,  1.0, 1.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]],
        render.faces[face[4]][9] + x,  render.faces[face[4]][10]+ y,  render.faces[face[4]][11]+ z,  1.0, 1.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]],
        render.faces[face[4]][12]+ x,  render.faces[face[4]][13]+ y,  render.faces[face[4]][14]+ z,  0.0, 0.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]],
        render.faces[face[4]][15]+ x,  render.faces[face[4]][16]+ y,  render.faces[face[4]][17]+ z,  1.0, 0.0, self.layer_list[self.model_list[face[3]]["textures"][face[4]]]]
        return face_vertex_data

    def generate_vertex_data(self, data, corner):
        now = time.time()
        render_list = []
        print("a")
        for index, i in np.ndenumerate(data[:,:,:,:]):
            x = index[0] + corner[0] * 16
            y = index[1]
            z = index[2] + corner[1] * 16
            f = index[3]
            if i == 0:
                render_list.append([
                render.faces[f][0] + x,  render.faces[f][1] + y,  render.faces[f][2] + z,  0.0, 1.0, 0,
                render.faces[f][3] + x,  render.faces[f][4] + y,  render.faces[f][5] + z,  0.0, 0.0, 0,
                render.faces[f][6] + x,  render.faces[f][7] + y,  render.faces[f][8] + z,  1.0, 1.0, 0,
                render.faces[f][9] + x,  render.faces[f][10]+ y,  render.faces[f][11]+ z,  1.0, 1.0, 0,
                render.faces[f][12]+ x,  render.faces[f][13]+ y,  render.faces[f][14]+ z,  0.0, 0.0, 0,
                render.faces[f][15]+ x,  render.faces[f][16]+ y,  render.faces[f][17]+ z,  1.0, 0.0, 0])
            else:
                render_list.append([
                render.faces[f][0] + x,  render.faces[f][1] + y,  render.faces[f][2] + z,  0.0, 1.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]],
                render.faces[f][3] + x,  render.faces[f][4] + y,  render.faces[f][5] + z,  0.0, 0.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]],
                render.faces[f][6] + x,  render.faces[f][7] + y,  render.faces[f][8] + z,  1.0, 1.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]],
                render.faces[f][9] + x,  render.faces[f][10]+ y,  render.faces[f][11]+ z,  1.0, 1.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]],
                render.faces[f][12]+ x,  render.faces[f][13]+ y,  render.faces[f][14]+ z,  0.0, 0.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]],
                render.faces[f][15]+ x,  render.faces[f][16]+ y,  render.faces[f][17]+ z,  1.0, 0.0, self.layer_list[self.model_list[i]["textures"][render.model_faces[f]]]])
        return render_list

    def create_buffer(self, data):
        """ Create a VBO and a VAO for the data passed as argument.
        data should be a list of faces and coordinates structured as returned by chunk.return_neighbours().
        Returns pointers to the buffer and array created, as well as the size of the buffer created (for drawing purposes).
        """
        print(len(data))
        vbo = self.context.buffer(data, dynamic=True)
        vao = self.context.vertex_array(self.program, [(vbo, "3f4 2f4 1f4 /v", "aPos", "aTexCoord", "blockType")])
        return vbo, vao

    def create_buffers_from_chunks(self, chunk_list):
        self.vbo_list, self.vao_list = [], []
        sys.stdout.write("Creating buffers... ")
        sys.stdout.flush()
        now = time.time()
        for index, chunk in enumerate(chunk_list):
            print("Buffering chunk ", index)
            new_vbo, new_vao = self.create_buffer(chunk.gen_vertex_data())
            self.vbo_list.append(new_vbo)
            self.vao_list.append(new_vao)
            chunk.GL_pointer = index
            chunk.vbo, chunk.vao = new_vbo, new_vao
        self.time_required = time.time() - now
        sys.stdout.write("Done\n")
        sys.stdout.flush()
        return self.vao_list

    def update_buffer(self, chunk):
        self.vbo_list[chunk.GL_pointer].write(chunk.vertex_data)

    def draw_from_chunks(self, chunk_list):
        for index, chunk in enumerate(chunk_list):
            chunk.vao.render(mode = mgl.TRIANGLES, vertices = int(self.vbo_list[index].size / 24))

def load_all_block_textures(sourcepath, context):
    layer_list = {}
    texture_list = []

    for num, texture in enumerate(sourcepath.iterdir()):
        tex_file = Image.open(texture)
        texture_list.append(list(tex_file.getdata()))
        layer_list.update({str(texture)[len(str(sourcepath))+1:]: num})
    texture_array_data = np.array(texture_list, dtype = "uint8")
    block_tex_array = context.texture_array((16, 16, len(texture_list)), 4, texture_array_data)
    block_tex_array.build_mipmaps()
    block_tex_array.filter = (mgl.LINEAR_MIPMAP_NEAREST, mgl.NEAREST)
    return block_tex_array, layer_list
