import glm, glfw

class camera:
    def __init__(self, parent):
        self.parent = parent
        self.position = glm.vec3(0)
        self.looking = glm.vec3(1, 0, 0)

        self.pitch, self.yaw = 0, 0
        self.last_x, self.last_y = glfw.get_window_size(self.parent.window)
        
        self.last_x /= 2
        self.last_y /= 2

        glfw.set_input_mode(self.parent.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos_callback(self.parent.window, self.mouse_callback)

    def mouse_callback(self, parent, x, y):

        x_offset, y_offset = x - self.last_x, y - self.last_y
        self.last_x, self.last_y = x, y

        x_offset *= 0.2
        y_offset *= 0.2

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