#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texture_coords;
layout (location = 2) in float texture_ID;

out vec3 texture_info:

uniform mat4 view;
uniform mat4 projection;

void main() {

    if (texture_ID != 0.0) {
        gl_Position = projection * view * vec4(position, 1.0);
        texture_info = vec3(texture_coords, texture_ID);
    }

}