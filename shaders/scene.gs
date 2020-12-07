#version 330 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

flat in int tex_index[];

uniform mat4 view;
uniform mat4 projection;

mat4 model = mat4(1.0);

out vec2 texCoord;
flat out int texLayer;

vec3 vertices[8] = vec3[8](vec3(0.0, 0.0, 0.0), 
                           vec3(0.0, 1.0, 0.0), 
                           vec3(1.0, 0.0, 0.0), 
                           vec3(1.0, 1.0, 0.0), 
                           vec3(1.0, 0.0, 1.0), 
                           vec3(1.0, 1.0, 1.0), 
                           vec3(0.0, 0.0, 1.0), 
                           vec3(0.0, 1.0, 1.0));

int faces[24] = int[24](4, 5, 6, 7,
                        0, 1, 2, 3,
                        2, 3, 4, 5,
                        6, 7, 0, 1,
                        1, 7, 3, 5,
                        6, 0, 4, 2);

void main() {

    texLayer = tex_index[0];
    int face_index = int(gl_in[0].gl_Position.w * 4.0);

    if (texLayer > 0) {

    model[3] = vec4(gl_in[0].gl_Position.xyz + vertices[faces[face_index]], 1.0);
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    texCoord = vec2(0.0, 0.0);
    EmitVertex();

    model[3] = vec4(gl_in[0].gl_Position.xyz + vertices[faces[face_index + 1]], 1.0);
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    texCoord = vec2(0.0, 1.0);
    EmitVertex();

    model[3] = vec4(gl_in[0].gl_Position.xyz + vertices[faces[face_index + 2]], 1.0);
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    texCoord = vec2(1.0, 0.0);
    EmitVertex();

    model[3] = vec4(gl_in[0].gl_Position.xyz + vertices[faces[face_index + 3]], 1.0);
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    texCoord = vec2(1.0, 1.0);
    EmitVertex();

    EndPrimitive();
    
    }
    
}