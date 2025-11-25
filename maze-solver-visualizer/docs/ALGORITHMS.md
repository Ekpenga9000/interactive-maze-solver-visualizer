# Algorithm Documentation

This document provides detailed explanations of the pathfinding algorithms implemented in the Maze Solver & Visualizer.

## Overview

The project implements three classic pathfinding algorithms, each with different characteristics and use cases:

1. **Depth-First Search (DFS)** - Explores deep paths first
2. **Breadth-First Search (BFS)** - Explores level by level
3. **Dijkstra's Algorithm** - Finds optimal paths with weights

## Depth-First Search (DFS)

### Algorithm Description

DFS explores as far as possible along each branch before backtracking. It uses a recursive approach to dive deep into the maze structure.

### Implementation Details

```python
def _solve_dfs(self, start, end):
    visited = set()
    path = []

    def dfs_recursive(current):
        if current in visited:
            return False

        visited.add(current)
        path.append(current)

        if current == end:
            return True

        # Try all neighbors
        for neighbor in self._get_neighbors(*current):
            if dfs_recursive(neighbor):
                return True

        # Backtrack
        path.pop()
        return False

    dfs_recursive(start)
    return path, visited
```

### Characteristics

- **Time Complexity**: O(V + E) where V = vertices, E = edges
- **Space Complexity**: O(V) for recursion stack and visited set
- **Completeness**: Yes (will find a solution if one exists)
- **Optimality**: No (may not find the shortest path)

### Pros and Cons

✅ **Pros:**

- Memory efficient for long paths
- Simple to implement and understand
- Good for exploring all possible paths

❌ **Cons:**

- May find very long paths
- Can get stuck in infinite loops without visited tracking
- May not find optimal solution

### Best Use Cases

- When memory is limited
- When any solution is acceptable
- For maze generation (recursive backtracking)
- When exploring all possibilities is needed

## Breadth-First Search (BFS)

### Algorithm Description

BFS explores all nodes at the current depth before moving to nodes at the next depth level. It guarantees the shortest path in unweighted graphs.

### Implementation Details

```python
def _solve_bfs(self, start, end):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visited

        for neighbor in self._get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return [], visited
```

### Characteristics

- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V) for queue and parent tracking
- **Completeness**: Yes
- **Optimality**: Yes (shortest path in unweighted graphs)

### Pros and Cons

✅ **Pros:**

- Guarantees shortest path
- Systematic exploration
- Good for finding minimum steps

❌ **Cons:**

- Higher memory usage for wide graphs
- May explore many irrelevant nodes
- Queue can become large

### Best Use Cases

- When shortest path is required
- For unweighted graphs (like our maze)
- When solution quality matters more than speed
- For level-based exploration

## Dijkstra's Algorithm

### Algorithm Description

Dijkstra's algorithm finds the shortest path in weighted graphs by always exploring the node with the lowest cost first. In our implementation, all edges have weight 1.

### Implementation Details

```python
def _solve_dijkstra(self, start, end):
    pq = [(0, start)]  # (distance, position)
    distances = {start: 0}
    parent = {start: None}
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visited

        for neighbor in self._get_neighbors(*current):
            if neighbor not in visited:
                new_distance = current_dist + 1

                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_distance, neighbor))

    return [], visited
```

### Characteristics

- **Time Complexity**: O((V + E) log V) with binary heap
- **Space Complexity**: O(V) for distances and priority queue
- **Completeness**: Yes
- **Optimality**: Yes (optimal for weighted graphs)

### Pros and Cons

✅ **Pros:**

- Optimal for weighted graphs
- Handles complex cost functions
- Well-studied and proven
- Extensible to different edge weights

❌ **Cons:**

- Overkill for unweighted graphs
- Higher computational overhead
- More complex implementation
- Priority queue overhead

### Best Use Cases

- Weighted graphs with varying edge costs
- When optimality is critical
- Complex pathfinding with multiple constraints
- Real-world navigation systems

## Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Optimal | Best For          |
| --------- | --------------- | ---------------- | ------- | ----------------- |
| DFS       | O(V + E)        | O(V)             | No      | Memory efficiency |
| BFS       | O(V + E)        | O(V)             | Yes\*   | Shortest path     |
| Dijkstra  | O((V+E) log V)  | O(V)             | Yes     | Weighted graphs   |

\*Optimal for unweighted graphs only

## Visual Differences

When running the visualizer, you can observe different exploration patterns:

### DFS Pattern

- **Color**: Explores in snake-like patterns
- **Behavior**: Goes deep before backtracking
- **Visited Area**: Often concentrated in specific regions

### BFS Pattern

- **Color**: Explores in expanding circles/waves
- **Behavior**: Systematic level-by-level expansion
- **Visited Area**: Even spread from start point

### Dijkstra Pattern

- **Color**: Similar to BFS for unweighted mazes
- **Behavior**: Priority-based exploration
- **Visited Area**: Efficient expansion toward target

## Performance Analysis

### Typical Results (25x15 maze)

```
Algorithm            Path Length  Cells Explored
--------------------------------------------------
Depth-First Search   107          115
Breadth-First Search 107          159
Dijkstra's Algorithm 107          159
```

### Analysis

- **DFS**: Found solution with minimal exploration
- **BFS**: Guaranteed optimal but explored more cells
- **Dijkstra**: Same as BFS for unweighted maze

## Implementation Notes

### Neighbor Selection

All algorithms use the same `_get_neighbors()` method:

```python
def _get_neighbors(self, x, y):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < self.width and
            0 <= new_y < self.height and
            self.maze[new_y][new_x] == 0):
            neighbors.append((new_x, new_y))

    return neighbors
```

### Path Reconstruction

BFS and Dijkstra use parent tracking for path reconstruction:

```python
# Reconstruct path from end to start
path = []
while current is not None:
    path.append(current)
    current = parent[current]
path.reverse()
```

DFS builds the path during exploration and backtracks when needed.

## Extensions and Improvements

### Possible Enhancements

1. **A\* Algorithm**: Add heuristic-guided search
2. **Bidirectional Search**: Search from both ends
3. **Jump Point Search**: Optimize for grid-based pathfinding
4. **Dynamic Pathfinding**: Handle changing obstacles

### Algorithm Variants

1. **Iterative DFS**: Stack-based instead of recursive
2. **Best-First Search**: Heuristic-guided exploration
3. **Uniform Cost Search**: Dijkstra variant
4. **Greedy Search**: Fast but not optimal

### Performance Optimizations

1. **Early Termination**: Stop when target is found
2. **Path Smoothing**: Remove unnecessary turns
3. **Hierarchical Pathfinding**: Multi-level maze solving
4. **Parallel Search**: Multiple algorithm instances

## References

1. Cormen, T. H., et al. "Introduction to Algorithms" (CLRS)
2. Russell, S., & Norvig, P. "Artificial Intelligence: A Modern Approach"
3. Sedgewick, R., & Wayne, K. "Algorithms" (4th Edition)
4. Wikipedia articles on pathfinding algorithms
