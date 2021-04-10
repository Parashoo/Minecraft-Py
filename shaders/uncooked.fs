#version 330 core

in vec3 texture_info;
out vec4 FragColor;

uniform sampler2DArray texture0;

void main() {
    FragColor = texture(texture0, texture_info);
}