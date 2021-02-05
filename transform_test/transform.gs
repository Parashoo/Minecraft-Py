#version 330 core

layout (points) in;
layout (points, max_vertices = 1) out;

out float type;

uniform sampler3D data;

void main() {

    uint x = uint(gl_in[0].gl_Position.x - int(gl_in[0].gl_Position.x/16)*16);
    uint y = uint(gl_in[0].gl_Position.x/16);

    type = uint(texelFetch(data, ivec3(5, 5, 5), 0).x);

    EmitVertex();
    EndPrimitive();

}