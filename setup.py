import moderngl as mgl
import glfw
import status

class context: # OpenGL rendering context
    def __init__(self):    
        self.context = mgl.create_context()
        self.context.enable(mgl.DEPTH_TEST | mgl.BLEND)
        self.context.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
    
class window: # GLFW window creation
    def __init__(self):
        
        window_creation_message = status.stm("Create window")

        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(800, 600, "__DELETEME__", None, None)
        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, resize_callback)

        window_creation_message.complete()

    def bind_context(self, context):
        self.context = context

    def clear(self):
        self.context.clear()
    
    def swap_buffers(self):
        glfw.swap_buffers(seld.window)
        glfw.poll_events()

        if glfw.window_should_close(self.window):
            self.close()

    def close(self):
        glfw.terminate()

class program:
    def __init__(self, shaderpath, context, vertex_shader, fragment_shader = None, geometry_shader = None):
        
        shaders = {'vert': vertex_shader, 'frag': fragment_shader, 'geo': geometry_shader}
        shaders_src = {'vert': None, 'frag': None, 'geo': None}
        for shader in shaders:
            if shaders[shader] != None:
                shaders_src[shader] = read_src(shaders[shader])
        self.program = context.program(vertex_shader = shaders_src['vert'], fragment_shader = shaders_src['frag'], geometry_shader = shaders_src['geo'])
        
        return self.program

def resize_callback(ctx, width, height): # Changes rendering viewport on window resize
    ctx.viewport = (0, 0, width, height)

def read_src(path):
    with path.open() as src:
        data = src.read()
    return data

def setup():
    win = window()
    ctx = context()
    win.bind_context(ctx)

    return win, ctx
