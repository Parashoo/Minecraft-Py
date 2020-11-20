#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in float blockType;

out vec2 TexCoord;
flat out int texLayer;

uniform mat4 view;
uniform mat4 projection;

mat4 model = mat4(1.0);

vec3 faces[24] = vec3[24](vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), 
                          vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0),
                          vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0),
                          vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0),
                          vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0),
                          vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0), vec3(1.0 ,0.0, 1.0));


void main() {
    model[3] = vec4(aPos, 1.0);
    gl_Position = projection * view * model * vec4(0.0, 0.0, 0.0, 1.0);
    TexCoord = aTexCoord;
    texLayer = int(blockType);
}
