#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in float blockType;

out vec2 TexCoord;
flat out int texLayer;

uniform mat4 view;
uniform mat4 projection;

uniform vec3 corner;

void main() {
    
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    TexCoord = aTexCoord;
    texLayer = int(blockType);
}
