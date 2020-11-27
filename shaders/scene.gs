#version 330 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

vec3 vertices[8] = vec3[8](vec3(0.0, 0.0, 0.0), 
                           vec3(0.0, 1.0, 0.0), 
                           vec3(1.0, 0.0, 0.0), 
                           vec3(1.0, 1.0, 0.0), 
                           vec3(1.0, 0.0, 1.0), 
                           vec3(1.0, 1.0, 1.0), 
                           vec3(0.0, 0.0, 1.0), 
                           vec3(0.0, 1.0, 1.0));

vec2 tex_coords[4] = vec2[4](vec2(0.0, 0.0),
                             vec2(0.0, 1.0),
                             vec2(1.0, 0.0),
                             vec2(1.0, 1.0));

int faces[24] = int[24](4, 5, 6, 7,
                        0, 1, 2, 3,
                        2, 3, 5, 4,
                        6, 7, 0, 1,
                        1, 7, 3, 5,
                        6, 0, 4, 2);

void main() {

    float n = gl_VertexID;
    float x = floor(n / (256.0 * 16.0 * 6.0));
    n = mod(n, 256.0 * 16.0 * 6.0);
    float y = floor(n / (16.0 * 6.0));
    n = mod(n, 16.0 * 6.0);
    float z = floor(n / 6.0);
    float f = mod(n, 6.0);

    mat4 model = mat4(1.0);


    vec3 worldpos = vec3(x, y, z) + corner;

    model[3] = vec4(vertices[faces[f]], 1.0);
    
    model[3] = vec4(vertices[faces[f+1]], 1.0);
    
    model[3] = vec4(vertices[faces[f+2]], 1.0);
    
    model[3] = vec4(vertices[faces[f+3]], 1.0);
    

}