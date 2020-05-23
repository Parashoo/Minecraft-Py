import glfw
import glm

class camera:

    def __init__(self, position, front, window_size):
        self.pos = glm.vec3(position[0], position[1], position[2])
        self.front = glm.vec3(front[0], front[1], front[2])
        self.up = glm.vec3(0, 1, 0)
        self.move = glm.vec3(front[0], 0, front[2])

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

        if self.pitch > 89:
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89

        direction = glm.vec3(
          glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
          glm.sin(glm.radians(self.pitch)),
          glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(direction)
        self.move.x = direction.x / glm.cos(glm.radians(self.pitch))
        self.move.z = direction.z / glm.cos(glm.radians(self.pitch))

    def process_input(self, parent, time):
        camera_speed = [4.13 * time, 4.13 * time]

        if glfw.get_key(parent.window, glfw.KEY_W) == glfw.PRESS:
            self.pos += camera_speed[0] * self.move
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

    def testing_commands(self, parent):
        if glfw.get_key(parent.window, glfw.KEY_H) == glfw.PRESS:
            self.pos = glm.vec3(0, 0, -3)

    def return_vectors(self):
        return self.pos, self.pos + self.front, self.up

    def set_sensitivity(self, new_sensitivity):
        self.sensitivity = new_sensitivity
