#version 330 core

out vec4 FragColor;

uniform sampler2D texture0; 

void main() {
    FragColor = texture(texture0, gl_PointCoord);
}

