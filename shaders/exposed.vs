#version 330 core

layout(location=0) in int dummy;

void main() {

    float n = gl_VertexID;
    float x = floor(n / (256.0 * 16.0 ));
    n = mod(n, 256.0 * 16.0);
    float y = floor(n / (16.0));
    float z = mod(n, 16.0);

    gl_Position 

}