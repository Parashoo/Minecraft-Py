import numpy as np
from PIL import Image
from OpenGL.GL import *

class texture:
	def __init__(self, source, flip):
		self.source = source
		self.flip = flip

	def source_open(self):
		try:
			self.tex_file = Image.open(self.source)
		except FileNotFoundError:
			print('[TEXTURE ERROR]: Given file does not exist')
		if self.flip:
			self.tex_file = self.tex_file.rotate(180)

	def source_open_zone(self, zone):
		self.tex_file = Image.open(self.source).crop(zone)
		if self.flip:
			self.tex_file = self.tex_file.rotate(180)

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
