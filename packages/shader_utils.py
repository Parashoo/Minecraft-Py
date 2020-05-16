import glm
import OpenGL
from OpenGL.GL import *

class shader:

    def __init__(self, vertexShaderPath, fragmentShaderPath, version_string):

        with open(vertexShaderPath, 'r') as file:
            self.vertexShaderData = file.read() % version_string

        with open(fragmentShaderPath, 'r') as file:
            self.fragmentShaderData = file.read() % version_string

    def compile(self):

        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, self.vertexShaderData)
        glCompileShader(vertexShader)

        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not success:
            infoLog = glGetShaderInfoLog(vertexShader)
            print('Error: Vertex shader compilation failed\n', infoLog)

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, self.fragmentShaderData)
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

    def get_ID(self):
        return self.program

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

