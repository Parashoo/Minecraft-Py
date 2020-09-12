#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 cube_coord;
layout (location = 3) in float blockType;

out vec2 TexCoord;
flat out int texLayer;

uniform mat4 view;
uniform mat4 projection;

mat4 model = mat4(1.0);

void main() {
    model[3] = vec4(cube_coord.xyz, 1.0);
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
    texLayer = int(blockType);
}
