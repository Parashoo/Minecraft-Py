import moderngl as mgl
import numpy as np
import glfw
import status

from pathlib import Path
from PIL import Image

def setup_context():
    """Creates an OpenGL context, enables depth testing and texture blending and sets the blend functions."""

    ctx = mgl.create_context()
    ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)
    ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
    return ctx

class window: # GLFW window creation

    '''Creates a window object.'''

    def __init__(self):
        
        window_creation_message = status.status_message("Create window")

        glfw.init()
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(800, 600, "__DELETEME__", None, None)
        self.run = True

        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, resize_callback)

        window_creation_message.complete()

    def bind_context(self, context): 
        '''Binds an OpenGL rendering context to the window. 
            
            - context: a moderngl context object'''
        self.context = context

    def clear(self):
        self.context.clear()
    
    def swap_buffers(self): # Swap rendering buffers
        glfw.swap_buffers(self.window)
        glfw.poll_events()

        if glfw.window_should_close(self.window):
            self.close()

    def close(self):
        '''Closes the window and terminates the GLFW library.'''
        glfw.destroy_window(self.window)
        glfw.terminate()
        self.run = False
        

class program:

    shader_path = Path() / 'shaders'
    '''Class that manages shader programs.'''
    def __init__(self, context, vertex_shader, fragment_shader = None, geometry_shader = None):
        
        shaders_name = {'vert': vertex_shader, 'frag': fragment_shader, 'geo': geometry_shader}
        shaders_code = {'vert': None, 'frag': None, 'geo': None}
        for shader in shaders_name:
            if shaders_name[shader] != None:
                shaders_code[shader] = read_src(program.shader_path / shaders_name[shader])
        self.program = context.program(vertex_shader = shaders_code['vert'], fragment_shader = shaders_code['frag'], geometry_shader = shaders_code['geo'])
        self.context = context

    def load_texture_array(self):
        """Loads all textures in the 'Minecraft-Py/textures' into an array texture."""

        texture_path = Path() / 'textures'
        texture_data_list = []
        for texture in texture_path.iterdir():
            texture_data_list.append(Image.open(texture).getdata())
        texture_array_data = np.array(texture_data_list, dtype="uint8")
        self.texture_array = self.context.texture_array((16, 16, len(texture_array_data)), 4, texture_array_data)
        self.texture_array.build_mipmaps()
        self.texture_array.filter = (mgl.LINEAR_MIPMAP_NEAREST, mgl.NEAREST)

    def use_texture_array(self, location = 0):
        self.texture_array.use(location)


def resize_callback(ctx, width, height): # Changes rendering viewport on window resize
    ctx.viewport = (0, 0, width, height)

def read_src(path):
    with path.open() as src:
        data = src.read()
    return data

def setup():
    win = window()
    ctx = setup_context()
    win.bind_context(ctx)

    return win, ctx
