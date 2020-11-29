#version 330 core

layout (location = 0) in float blocktype;

uniform mat4 view;
uniform mat4 projection;
uniform vec3 corner;

void main() {
    
    gl_Position = vec4(block);

}
