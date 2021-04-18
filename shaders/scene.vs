#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in float blockType;

out vec2 tex_coord;
out float tex_layer;

uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * vec4(aPos, 1.0);
    tex_coord = aTexCoord;
    tex_layer = int(blockType);
}
