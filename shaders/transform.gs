#version 330 core

layout (points) in;
layout (points, max_vertices = 6) out;

uniform sampler3D texture0;

void main() {

    vec3 coords = gl_in[0].gl_Position.xyz;

    int blocktype = int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z), 0).w);

    int neighbours[6] = int[6](int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z+1), 0).w),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y, coords.z-1), 0).w),
                               int(texelFetch(texture0, ivec3(coords.x+1, coords.y, coords.z), 0).w),
                               int(texelFetch(texture0, ivec3(coords.x-1, coords.y, coords.z), 0).w),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y+1, coords.z), 0).w),
                               int(texelFetch(texture0, ivec3(coords.x, coords.y-1, coords.z), 0).w));

    for (int i=0;i<6;i++){

    if (neighbours[i] == 0) {
    gl_Position = vec4(coords, blocktype);
    } else {
    gl_Position = vec4(coords, 0);
    }
    EmitVertex();
    EndPrimitive();
    }

}