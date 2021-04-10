#version 330 core

layout (location = 0) in float asdf;

void main() {
    gl_Position = vec4(asdf);
}