#version 330 core

layout (points) in;
layout (points, max_vertices = 6) out;

uniform sampler3D chunk_data;

out uint type;

void main() {

    vec3 coords = gl_in[0].gl_Position.xyz;

    int blocktype = int(texelFetch(chunk_data, ivec3(1, 1, 1), 0).x);

    if (blocktype > 0) {

    int neighbours[6] = int[6](int(texelFetch(chunk_data, ivec3(coords.x, coords.y, coords.z+1), 0).x),
                               int(texelFetch(chunk_data, ivec3(coords.x, coords.y, coords.z-1), 0).x),
                               int(texelFetch(chunk_data, ivec3(coords.x+1, coords.y, coords.z), 0).x),
                               int(texelFetch(chunk_data, ivec3(coords.x-1, coords.y, coords.z), 0).x),
                               int(texelFetch(chunk_data, ivec3(coords.x, coords.y+1, coords.z), 0).x),
                               int(texelFetch(chunk_data, ivec3(coords.x, coords.y-1, coords.z), 0).x));
    for (int i=0;i<6;i++){

    if (neighbours[i] == 0) {
    type = uint(1);
    } else {
    type = uint(0);
    }

    type = uint(blocktype);
    EmitVertex();
    EndPrimitive();
    }

    }

}