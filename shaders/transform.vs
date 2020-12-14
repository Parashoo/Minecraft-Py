#version 330 core

void main() {

    float n = gl_VertexID;
    float x = floor(n / (64 * 16.0)) + 1;
    n = mod(n, 64 * 16.0);
    float y = floor(n / (16.0));
    float z = mod(n, 16.0) + 1;
    
    gl_Position = vec4(x, y, z, 0.0);

}