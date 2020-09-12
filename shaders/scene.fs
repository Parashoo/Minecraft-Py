#version 330 core

in vec2 TexCoord;
flat in int texLayer;
out vec4 FragColor;

uniform sampler2DArray texture0;

void main()
{
	FragColor = texture(texture0, vec3(TexCoord, texLayer));
}
