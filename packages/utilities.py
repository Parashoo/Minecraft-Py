import glfw
import numpy as np
import glm
import time
import sys, os

from OpenGL.GL import *
from PIL import Image
from pathlib import Path

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
            self.pos = glm.vec3(0, 0, 0)
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
            print(self.pitch)
    def return_vectors(self):
        return self.pos, self.pos + self.front, self.up

    def set_sensitivity(self, new_sensitivity):
        self.sensitivity = new_sensitivity

class window:
    def __init__(self, *options, **even_more_options):
        sys.stdout.write("Creating window... ")
        sys.stdout.flush()

        self.size = [800, 600]

        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(self.size[0], self.size[1], "__DELETEME__", None, None)

        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.window_resize_callback)
        sys.stdout.write("Done\n")
        sys.stdout.flush()

    def refresh(self, step, context, *options):
        color = (0.2, 0.3, 0.3, 1.0)
        if options:
            color = options[0]
        if step == 0:
            context.clear()
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
