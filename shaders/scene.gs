#version 330 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

float vec3[4] 

vec3 vertices[8] = vec3[8](vec3(0.0, 0.0, 0.0), vec3(0.0, 0.0, 1.0), vec3(0.0, 1.0, 0.0), vec3(1.0, 0.0, 0.0), vec3(1.0, 1.0, 0.0), vec3(1.0, 0.0, 1.0), vec3(0.0, 1.0, 1.0), vec3(1.0, 1.0, 1.0))

int faces[24] = int[24](4, 7, 1, 6,
                        0, 2, 3, 4);

void main() {

    float x = floor(gl_VertexID / (256.0 * 16.0 * 6.0));
    float y = floor(mod(gl_VertexID, (256.0 * 16.0 * 6.0)) / 256.0);
    float z = floor(mod(floor(mod(gl_VertexID, (256.0 * 16.0 * 6.0)) / 256.0), 16.0) / 16.0);
    float f = mod(mod(floor(mod(gl_VertexID, (256.0 * 16.0 * 6.0)) / 256.0), 16.0), 16.0);
    
}