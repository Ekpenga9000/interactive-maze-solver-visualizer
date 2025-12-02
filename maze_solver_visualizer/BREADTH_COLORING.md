# Enhanced Maze Visualizer - Breadth Split Visualization

## New Feature: Two-Color Breadth Splitting Visualization

The maze visualizer now uses two alternating colors to show how BFS and Dijkstra algorithms split and explore different breadths, making it easy to visualize the wave-like expansion pattern.

## How It Works

### Breadth-First Search (BFS) - Algorithm 2
- **Even levels (0, 2, 4...)**: Light Blue (original color)
- **Odd levels (1, 3, 5...)**: Light Red/Pink
- **Result**: Clear alternating pattern showing each breadth level as the algorithm expands outward in waves

### Dijkstra's Algorithm - Algorithm 3  
- **Closer distances**: Light Blue
- **Farther distances**: Light Red/Pink
- **Result**: Visual distinction between cells that are closer vs farther from the start

### Depth-First Search (DFS) - Algorithm 1
- Uses the standard **light blue** color
- No breadth splitting since DFS explores depth-first, not breadth-first

## Visual Benefits

1. **See the Wave Pattern**: Watch BFS create alternating rings of blue and red as it explores each breadth level
2. **Understand Splitting**: Clearly see how the algorithm splits into multiple paths at each breadth level
3. **Simple but Effective**: Just two colors make the pattern easy to follow without visual overload
4. **Educational Value**: Perfect for understanding the systematic expansion of breadth-first algorithms

## Usage

1. **Generate a new maze**: Press `G`
2. **Select BFS or Dijkstra**: Press `2` or `3`  
3. **Start solving**: Press `S`
4. **Watch the alternating colors**: See the blue and red pattern showing breadth splitting!

## Color Pattern Examples

**BFS Example**: 
- Start position: Light blue (level 0)
- First ring around start: Light red (level 1) 
- Second ring: Light blue (level 2)
- Third ring: Light red (level 3)
- And so on...

**Dijkstra Example**: Cells are colored based on whether they're in the closer half (blue) or farther half (red) of the distance range.

This simplified visualization makes it much easier to see the breadth-first exploration pattern without being distracted by too many colors!