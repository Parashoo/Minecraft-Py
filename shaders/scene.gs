#version 330 core

layout (triangles) in;
layout (triangle_strip, max_vertices=3) out;

in vec2 tex_coord[];
in float tex_layer[];

out vec2 texture_coord;
out float texture_layer;

void main() {
    if (tex_layer[0] != 0){
        for (int i = 0; i < 3; i++) {
            gl_Position = gl_in[i].gl_Position;
            texture_coord = tex_coord[i];
            texture_layer = tex_layer[i];
            EmitVertex();
        }
        EndPrimitive();
    }
}