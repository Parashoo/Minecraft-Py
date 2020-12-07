#version 330 core

layout (location = 0) in int blocktype;

uniform vec2 corner;

flat out int tex_index;

void main() {

    float n = gl_VertexID;
    float x = floor(n / (256.0 * 16.0 * 6.0));
    n = mod(n, 256.0 * 16.0 * 6.0);
    float y = floor(n / (16.0 * 6.0));
    n = mod(n, 16.0 * 6.0);
    float z = floor(n / 6.0);
    float f = mod(n, 6.0);
    
    gl_Position = vec4(x + corner.x * 16, y, z + corner.y * 16, f);
    tex_index = blocktype;

}
