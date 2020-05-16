import glfw
from OpenGL.GL import *

window_width, window_height = 800, 600

help_string = '''
window() takes following optional arguments, in following order:
	-OpenGL_version: a string containing the version to be used. Defaults to '3.3'.
	-size: a tuple containing the window's dimensions. Defaults to (800, 600)
	-title: a string containing the window's title. Defaults to "__DELETEME__".
'''

class window:

	def __init__(self, *options, **even_more_options):

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

		if even_more_options:
			if even_more_options['-h'] == True:
				print(help_string)

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

		self.window = glfw.create_window(window_width, window_height, title, None, None)

		glfw.make_context_current(self.window)
		glfw.set_framebuffer_size_callback(self.window, resize_callback)

	def refresh(self, step, *options):

		color = (0.2, 0.3, 0.3, 1.0)

		if options:
			color = options[0]

		if step == 0:
			glClearColor(color[0], color[1], color[2], color[3])
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			self.size[0], self.size[1] = window_width, window_height

		if step == 1:
			glfw.swap_buffers(self.window)
			glfw.poll_events()

	def check_if_closed(self):
		return glfw.window_should_close(self.window)

	def close(self):
		glfw.terminate()

	def pause(self):
		if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
			glfw.set_cursor_pos_callback(self.window, None)

def resize_callback(window, width, height):
	global window_width, window_height
	glViewport(0, 0, width, height)
	window_width, window_height = width, height
