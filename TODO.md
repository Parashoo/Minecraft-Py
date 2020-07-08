### Rendering
  - Redo rendering engine
    - Use multiple different buffers of "quadrants", each having bonus space for more blocks,
      allocated on runtime
    - Assemble chunk exposed blocks into larger buffer
  - Allow editing of buffer data
    - Keep track of exposed faces and their memory pointers

### Movement
  - Collisions <-- BIG POINT RIGHT HERE
    - Hitboxes
  - Gravity

### World Generation
  - Heightmap
    - Upper layer: grass
    - 2-3 layers under: dirt
    - Until bottom: stone
    - Bottom: bedrock
  - Trees?

### Models
  - Create new models:
    - Bedrock
    - Oak Logs
    - Oak Leaves
    - Oak Planks
    - Stone
