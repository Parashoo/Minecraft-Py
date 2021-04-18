#version 330 core

layout (location = 0) in vec3 aPos;

out vec3 skyColor;

uniform float orientation;

void main() {
    gl_Position = vec4(aPos, 1.0);
    skyColor = mix(vec3(0.9, 0.9, 1.0), vec3(0.4, 0.5, 0.7), sin(orientation+aPos.y));
    if (all(lessThanEqual(skyColor, vec3(0.4, 0.5, 0.7)))){
    skyColor = vec3(0.4, 0.5, 0.7);
    }
}
