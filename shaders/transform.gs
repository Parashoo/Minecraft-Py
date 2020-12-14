#version 330 core

layout (points) in;
layout (points, max_vertices = 6) out;

uniform sampler3D texture0;

out uint type;

void main() {

    vec3 coords = gl_in[0].gl_Position.xyz;

    int blocktype = int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z), 0).r);

    if (blocktype > 0) {

    int neighbours[6] = int[6](int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z+1), 0).r),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z-1), 0).r),
                               int(texelFetch(texture0, ivec3(coords.x+1, coords.y, coords.z), 0).r),
                               int(texelFetch(texture0, ivec3(coords.x-1, coords.y, coords.z), 0).r),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y+1, coords.z), 0).r),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y-1, coords.z), 0).r));
    for (int i=0;i<6;i++){

    if (neighbours[i] == 0) {
    type = uint(1);
    } else {
    type = uint(0);
    }
    EmitVertex();
    EndPrimitive();
    }

    }

}