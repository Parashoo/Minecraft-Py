#version 330 core

in vec3 skyColor;

out vec4 FragColor;

void main() {
    FragColor = vec4(skyColor, 1.0);
}
