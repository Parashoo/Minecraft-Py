#version 330 core

in vec2 texture_coord;
in float texture_layer;
out vec4 FragColor;

uniform sampler2DArray texture0;

void main()
{
	FragColor = texture(texture0, vec3(texture_coord, 1));
}
