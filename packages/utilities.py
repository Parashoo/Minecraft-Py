import glfw
import numpy as np
import glm
import time
import sys, os

from OpenGL.GL import *
from PIL import Image

class camera:

    def __init__(self, position, front, window_size):
        self.pos = glm.vec3(position[0], position[1], position[2])
        self.front = glm.vec3(front[0], front[1], front[2])
        self.up = glm.vec3(0, 1, 0)
        self.move = glm.vec3(front[0], 0, front[2])

        self.sprint = False
        self.sprint_press = 0
        self.coords_toggle = False

        self.last_x, self.last_y = window_size[0]/2, window_size[1]/2
        self.pitch = glm.asin(self.front.y)
        self.yaw = glm.acos(self.front.x / glm.cos(self.pitch))

        self.sensitivity = 0.2

        self.first_mouse = True

    def setup_window(self, parent):
        glfw.set_input_mode(parent.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos_callback(parent.window, self.mouse_callback)

    def mouse_callback(self, parent, x, y):
        if self.first_mouse:
            self.last_x, self.last_y = x, y
            self.first_mouse = False

        x_offset, y_offset = x - self.last_x, y - self.last_y
        self.last_x, self.last_y = x, y

        x_offset *= self.sensitivity
        y_offset *= self.sensitivity

        self.yaw += x_offset
        self.pitch -= y_offset

        if self.pitch > 89.95:
            self.pitch = 89.95
        if self.pitch < -89.95:
            self.pitch = -89.95

        direction = glm.vec3(
          glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
          glm.sin(glm.radians(self.pitch)),
          glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(direction)
        self.move.x = direction.x / glm.cos(glm.radians(self.pitch))
        self.move.z = direction.z / glm.cos(glm.radians(self.pitch))

    def process_input(self, parent, delta_time):
        camera_speed = [4.13 * delta_time, 5 * delta_time]
        sprint_speed = camera_speed[0]
        if self.sprint:
            sprint_speed = 10 * delta_time
        if glfw.get_key(parent.window, glfw.KEY_W) == glfw.PRESS:
            self.pos += sprint_speed * self.move
        if glfw.get_key(parent.window, glfw.KEY_W) == glfw.RELEASE:
            self.sprint = False
        if glfw.get_key(parent.window, glfw.KEY_S) == glfw.PRESS:
            self.pos -= camera_speed[0] * self.move
        if glfw.get_key(parent.window, glfw.KEY_A) == glfw.PRESS:
            self.pos -= glm.normalize(glm.cross(self.move, self.up)) * camera_speed[0]
        if glfw.get_key(parent.window, glfw.KEY_D) == glfw.PRESS:
            self.pos += glm.normalize(glm.cross(self.move, self.up)) * camera_speed[0]
        if glfw.get_key(parent.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.pos += self.up * camera_speed[1]
        if glfw.get_key(parent.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.pos -= self.up * camera_speed[1]
        if glfw.get_key(parent.window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            self.sprint = True

    def testing_commands(self, parent):
        if glfw.get_key(parent.window, glfw.KEY_H) == glfw.PRESS:
            self.pos = glm.vec3(0, 0, -3)
        if glfw.get_key(parent.window, glfw.KEY_PAGE_DOWN) == glfw.PRESS:
            self.pos.y -= 50
        if glfw.get_key(parent.window, glfw.KEY_PAGE_UP) == glfw.PRESS:
            self.pos.y += 50
        if glfw.get_key(parent.window, glfw.KEY_C) == glfw.PRESS:
            if not self.coords_toggle:
                nice_coords = [int(i) for i in self.pos]
                print('x: {} y: {} z: {}'.format(nice_coords[0], nice_coords[1], nice_coords[2]))
                self.coords_toggle = True
        if glfw.get_key(parent.window, glfw.KEY_C) == glfw.RELEASE:
            self.coords_toggle = False
        if glfw.get_key(parent.window, glfw.KEY_F) == glfw.PRESS:
            directions_dict = {
                (1,0): 'east',
                (0,1): 'north',
                (-1,0): 'west',
                (0,-1): 'south'}
            direction_tuple = (round(self.move.x), round(self.move.z))
            if not self.direction_toggle:
                try:
                    print('facing: {}'.format(directions_dict[direction_tuple]))
                except KeyError:
                    print("Some combination of north, south, east and west that I'm too lazy to specify")
                self.direction_toggle = True
        if glfw.get_key(parent.window, glfw.KEY_F) == glfw.RELEASE:
            self.direction_toggle = False
        if glfw.get_key(parent.window, glfw.KEY_O) == glfw.PRESS:
            print('ASDFGHJKLÖ')
            print(self.pitch)
    def return_vectors(self):
        return self.pos, self.pos + self.front, self.up

    def set_sensitivity(self, new_sensitivity):
        self.sensitivity = new_sensitivity

class shader:
    def __init__(self, vertex_shader_path, fragment_shader_path, version_string):

        with open(vertex_shader_path, 'r') as file:
            self.vertex_shader_data = file.read() % version_string

        with open(fragment_shader_path, 'r') as file:
            self.fragment_shader_data = file.read() % version_string

    def compile(self):

        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, self.vertex_shader_data)
        glCompileShader(vertexShader)

        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(vertexShader)
            print('Error: Vertex shader compilation failed\n', infoLog)

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, self.fragment_shader_data)
        glCompileShader(fragmentShader)

        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(fragmentShader)
            print('Error: Fragment shader compilation failed\n', infoLog)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertexShader)
        glAttachShader(self.program, fragmentShader)
        glLinkProgram(self.program)

        success = glGetProgramiv(self.program, GL_LINK_STATUS)

        if not success:
            infoLog = glGetProgramInfoLog(self.program)
            print('Error: Shader program linking failed\n', infoLog)

        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

    def use(self):
        glUseProgram(self.program)

    def set_bool(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def set_int(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def set_float(self, name, value):
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_vec2_o(self, name, object):
        glUniform2fv(glGetUniformLocation(self.program, name), 1, object)

    def set_vec2_f(self, name, x, y):
        glUniform2f(glGetUniformLocation(self.program, name), x, y)

    def set_vec3_o(self, name, object):
        glUniform3fv(glGetUniformLocation(self.program, name), 1, object)

    def set_vec3_f(self, name, x, y, z):
        glUniform3f(glGetUniformLocation(self.program, name), x, y, z)

    def set_vec4_o(self, name, object):
        glUniform4fv(glGetUniformLocation(self.program, name), 1, object)

    def set_vec4_f(self, name, x, y, z, w):
        glUniform4f(glGetUniformLocation(self.program, name), x, y, z, w)

    def set_mat2(self, name, object):
        glUniformMatrix2fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, object)

    def set_mat3(self, name, object):
        glUniformMatrix3fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, object)

    def set_mat4(self, name, object):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, object)

class texture:
    def __init__(self, source, **kwargs):
        self.source = source
        try:
            self.tex_file = Image.open(self.source)
        except FileNotFoundError:
            print('\033[1m\033[91m[TEXTURE ERROR]: Given file does not exist\033[0m\n')
            self.tex_file = Image.open('ressources/block/missing.png')
        if 'flip' in kwargs.keys():
            self.tex_file = self.tex_file.rotate(180)
        if 'crop' in kwargs.keys():
            self.tex_file = self.tex_file.crop(kwargs['crop'])

    def gen_texture(self):
        self.tex_ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_ID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.tex_width, self.tex_height, self.tex_data = self.tex_file.size[0], self.tex_file.size[1], np.array(list(self.tex_file.getdata()), np.int8)

        if self.tex_data.any():
            if self.tex_file.mode == 'RGB':
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.tex_width, self.tex_height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.tex_data)
                glGenerateMipmap(GL_TEXTURE_2D)
            elif self.tex_file.mode == 'RGBA':
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.tex_width, self.tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.tex_data)
                glGenerateMipmap(GL_TEXTURE_2D)
            else:
                print('[TEXTURE ERROR]: Texture file is not a supported pixel type\n')
        else:
            print('[TEXTURE ERROR]: Could not load texture file')

        del self.tex_width, self.tex_height, self.tex_data
        return self.tex_ID

class window:
    def __init__(self, *options, **even_more_options):
        sys.stdout.write("Creating window... ")
        sys.stdout.flush()
        OpenGL_version = '3.3'
        self.size = [800, 600]
        title = '__DELETEME__'
        if options:
            if len(options) == 1:
                OpenGL_version = options[0]

            if len(options) == 2:
                size = options[1]

        if len(options) == 3:
            title = options[2]
        try:
            version_major, version_minor = int(OpenGL_version.split('.')[0]), int(OpenGL_version.split('.')[1][0])
            if float(OpenGL_version) > 4.5:
                print('[OPENGL ERROR]: This version does not exist yet, reverting to OpenGL 3.3 instead\n')
        except ValueError:
            print('[OPENGL ERROR]: Invalid OpenGL version, reverting to 3.3 instead\n')
            version_major, version_minor = 3, 3

        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, version_major)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, version_minor)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(self.size[0], self.size[1], title, None, None)

        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.window_resize_callback)
        sys.stdout.write("Done\n")
        sys.stdout.flush()

    def refresh(self, step, *options):
        color = (0.2, 0.3, 0.3, 1.0)
        if options:
            color = options[0]
        if step == 0:
            #glClearColor(color[0], color[1], color[2], color[3])
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if step == 1:
            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def check_if_closed(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.terminate()

    def window_resize_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        self.size = [width, height]
