import moderngl as mgl
import numpy as np
from PIL import Image

def setup():
    ctx = mgl.create_context(standalone=True)
    with open('transform.vs') as src: 
        transform_vert = src.read()
    with open('transform.gs') as src: 
        transform_geo = src.read()

    prog = ctx.program(vertex_shader=transform_vert, geometry_shader = transform_geo, varyings = 'type')
    data_tex = ctx.texture3d((16, 16, 16), 1, data=np.full((16, 16, 16), 150, dtype='f4'), dtype = 'f4')

    return ctx, prog, data_tex

def main():
    ctx, prog, tex = setup()
    prog['data'] = 0
    tex.use(location=0)
    dummy = ctx.buffer(reserve = 16 * 16 * 4)
    dummy2 = ctx.buffer(reserve = 16 * 16 * 4)
    dummy_vao = ctx.vertex_array(prog, [])
    dummy_vao.transform(dummy2, mode=mgl.POINTS, vertices = 16 * 16)
    Image.frombytes('F', (16, 16), dummy2.read()).show()

if __name__=='__main__':
    main()
    