# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-23

### Added
- Initial release of Maze Solver & Visualizer
- Maze generation using recursive backtracking algorithm
- Three pathfinding algorithms:
  - Depth-First Search (DFS) with recursive implementation
  - Breadth-First Search (BFS) for shortest path
  - Dijkstra's Algorithm for optimal pathfinding
- Interactive Pygame-based visualization
- Real-time algorithm visualization with color-coded cells
- Keyboard controls for algorithm switching and maze generation
- Console-based algorithm demonstration (`demo.py`)
- Comprehensive test suite (`test_components.py`)
- Complete documentation and README
- MIT License
- Contributing guidelines

### Features
- **Interactive Controls:**
  - G: Generate new maze
  - S: Solve current maze
  - 1/2/3: Switch between algorithms
  - Q: Quit application
- **Visual Elements:**
  - Green start position
  - Red end position
  - Yellow solution path
  - Light blue explored cells
  - Black walls, white paths
- **Algorithm Statistics:**
  - Path length display
  - Performance comparison
  - Exploration efficiency metrics

### Technical Details
- Python 3.12+ support
- Pygame 2.6+ compatibility
- Modular architecture with separate components
- Type hints and comprehensive docstrings
- Cross-platform compatibility (Linux, Windows, macOS)

## [Unreleased]

### Planned
- A* pathfinding algorithm
- Animated step-by-step solving
- Maze saving/loading functionality
- Different maze generation algorithms
- Performance benchmarking tools
- GUI improvements and themes