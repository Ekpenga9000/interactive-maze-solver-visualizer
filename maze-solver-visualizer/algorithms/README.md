# Algorithms Package

This package contains modular implementations of pathfinding algorithms for the Maze Solver & Visualizer.

## Architecture

The algorithms package follows a modular design with the following components:

### Base Algorithm Class

- **`BaseAlgorithm`**: Abstract base class defining the interface for all pathfinding algorithms
- Provides common functionality like neighbor detection and path reconstruction
- Ensures consistent interface across all algorithm implementations

### Algorithm Implementations

- **`DepthFirstSearch`**: Recursive depth-first exploration with backtracking
- **`BreadthFirstSearch`**: Level-by-level exploration guaranteeing shortest path
- **`Dijkstra`**: Priority-based exploration for weighted pathfinding

## Features

### Dual Solving Modes

Each algorithm supports two solving modes:

1. **Standard Solving** (`solve` method):

   - Returns final path and visited cells
   - Optimized for performance
   - Used for quick algorithm comparison

2. **Animated Solving** (`solve_animated` method):
   - Yields step-by-step state information
   - Perfect for real-time visualization
   - Provides detailed algorithm behavior

### Animation State

The animated solving methods yield dictionaries containing:

- `current`: Currently exploring cell
- `visited`: Set of visited cells
- `action`: Current action ('exploring', 'visited', 'found', etc.)
- Algorithm-specific data (stack for DFS, queue for BFS, distances for Dijkstra)

## Usage

### Basic Usage

```python
from algorithms import DepthFirstSearch, BreadthFirstSearch, Dijkstra

# Create algorithm instance
dfs = DepthFirstSearch(maze)

# Solve maze
path, visited = dfs.solve(start, end)

# Animated solving
for state in dfs.solve_animated(start, end):
    print(f"Exploring: {state['current']}")
    if state['action'] == 'found':
        print(f"Solution: {state['path']}")
        break
```

### Integration with MazeSolver

```python
from maze_solver import MazeSolver, Algorithm

solver = MazeSolver(maze)
path, visited = solver.solve(start, end, Algorithm.DFS)
```

## Algorithm Details

### Depth-First Search (DFS)

- **Strategy**: Explore as deep as possible before backtracking
- **Data Structure**: Stack (implemented recursively)
- **Animation States**:
  - `exploring`: Currently examining a cell
  - `visited`: Cell marked as visited
  - `backtrack`: Returning to previous cell
  - `found`: Solution discovered

### Breadth-First Search (BFS)

- **Strategy**: Explore level by level from start
- **Data Structure**: Queue (FIFO)
- **Animation States**:
  - `exploring`: Processing current cell from queue
  - `neighbor_added`: New cell added to exploration queue
  - `found`: Solution discovered

### Dijkstra's Algorithm

- **Strategy**: Always explore the lowest-cost unvisited cell
- **Data Structure**: Priority queue (min-heap)
- **Animation States**:
  - `exploring`: Processing cell with lowest distance
  - `visited`: Cell permanently processed
  - `distance_updated`: Shorter path to neighbor found
  - `found`: Solution discovered

## Extending the Package

To add a new algorithm:

1. Create a new file in the `algorithms/` directory
2. Implement a class inheriting from `BaseAlgorithm`
3. Implement both `solve` and `solve_animated` methods
4. Add the new algorithm to `__init__.py`
5. Update `Algorithm` enum in `maze_solver.py`

### Example Template

```python
from .base_algorithm import BaseAlgorithm

class NewAlgorithm(BaseAlgorithm):
    def solve(self, start, end):
        # Implement standard solving
        pass

    def solve_animated(self, start, end):
        # Implement animated solving
        for step in algorithm_steps:
            yield {
                'current': current_cell,
                'visited': visited_set,
                'action': 'exploring'
            }
```

## Performance Considerations

- **Memory**: Each algorithm instance stores the maze reference
- **CPU**: Animated solving has overhead for state tracking
- **Scalability**: Algorithm complexity remains unchanged

## Testing

The package includes comprehensive tests covering:

- Basic functionality of each algorithm
- Path correctness (start/end validation)
- Visited cell tracking
- Animation state consistency

Run tests with:

```bash
python test_components.py
```
