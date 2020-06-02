#version %s core

layout (location = 0) in vec3 aPos;

out vec3 skyColor;

uniform float orientation;

void main() {
     gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
     skyColor = mix(vec3(0.8, 0.8, 0.85), vec3(0.5, 0.5, 0.65), (sin(orientation)+1)/2 + aPos.y);
}
