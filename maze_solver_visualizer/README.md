# Recursive Maze Solver & Visualizer

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/pygame-2.6+-green.svg)](https://pygame.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python application that generates random mazes and solves them using various pathfinding algorithms with real-time visualization using Pygame.

![Maze Solver Demo](docs/demo.gif)

## 🎯 Overview

This project demonstrates fundamental computer science algorithms through an interactive maze-solving visualizer. Watch as different pathfinding algorithms explore mazes in **real-time with live step-by-step visualization**, allowing you to see exactly how each algorithm thinks, explores, and makes decisions as it searches for the solution.

## Features

- **Maze Generation**: Random maze generation using recursive backtracking algorithm
- **Multiple Solving Algorithms**:
  - Depth-First Search (DFS) - Recursive implementation
  - Breadth-First Search (BFS) - Guaranteed shortest path
  - Dijkstra's Algorithm - Optimal pathfinding
- **Real-time Visualization**: See algorithms explore the maze live as they make decisions, with adjustable animation speed
- **Interactive Controls**: Control animation speed, switch algorithms, and generate new mazes

## Requirements

- Python 3.12+
- Pygame 2.6+

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/maze-solver-visualizer.git
   cd maze-solver-visualizer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Quick Start
Run the main application:
```bash
python main.py
```

### Demo Mode
See algorithms in action without GUI:
```bash
python demo.py
```

### Run Tests
Verify everything works:
```bash
python test_components.py
```

## 📸 Screenshots

### Main Interface
![Main Interface](docs/main_interface.png)

### Algorithm Comparison
| Depth-First Search | Breadth-First Search | Dijkstra's Algorithm |
|-------------------|---------------------|---------------------|
| ![DFS](docs/dfs_demo.png) | ![BFS](docs/bfs_demo.png) | ![Dijkstra](docs/dijkstra_demo.png) |

### Console Demo
![Console Demo](docs/console_demo.png)

### Controls

- **G** - Generate a new random maze
- **S** - Solve the current maze using selected algorithm (animated)
- **R** - Reset/stop current solving animation
- **+** - Increase animation speed (faster)
- **-** - Decrease animation speed (slower)
- **1** - Switch to Depth-First Search (DFS)
- **2** - Switch to Breadth-First Search (BFS)
- **3** - Switch to Dijkstra's Algorithm
- **Q** - Quit the application

### Visual Elements

- **Black**: Walls
- **White**: Open paths
- **Green**: Start position (top-left)
- **Red**: End position (bottom-right)
- **Light Blue**: Visited cells during pathfinding
- **Orange**: Currently exploring cell (real-time indicator)
- **Yellow**: Solution path

## Project Structure

```
maze-solver-visualizer/
├── algorithms/              # Modular pathfinding algorithm implementations
│   ├── __init__.py          # Package initialization with exports
│   ├── base_algorithm.py    # Abstract base class for algorithms
│   ├── depth_first_search.py   # DFS implementation
│   ├── breadth_first_search.py # BFS implementation
│   └── dijkstra.py          # Dijkstra's algorithm implementation
├── main.py                  # Main application entry point
├── maze_generator.py        # Maze generation using recursive backtracking
├── maze_solver.py           # Algorithm coordinator and solver interface
├── maze_visualizer.py       # Pygame visualization and user interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Algorithms

### Depth-First Search (DFS)
- **Type**: Recursive backtracking
- **Properties**: May not find shortest path, but uses less memory
- **Use case**: Good for exploring all possible paths

### Breadth-First Search (BFS)
- **Type**: Queue-based level traversal
- **Properties**: Guarantees shortest path in unweighted graphs
- **Use case**: Optimal for finding shortest path

### Dijkstra's Algorithm
- **Type**: Priority queue-based shortest path
- **Properties**: Finds optimal path with weighted edges
- **Use case**: Best for weighted graphs (treats all edges as weight 1 here)

## 🧪 Testing

This project includes a comprehensive test suite with over 100 tests covering all components:

### Running Tests

**Using the test runner script (recommended):**
```bash
# Run all tests
python run_tests.py --all

# Run specific test categories
python run_tests.py --unit          # Unit tests only
python run_tests.py --integration   # Integration tests only
python run_tests.py --performance   # Performance tests only

# Run with coverage
python run_tests.py --coverage
```

**Using pytest directly:**
```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_maze_generator.py -v
pytest tests/test_dfs.py tests/test_bfs.py tests/test_dijkstra.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

**⚠️ Important:** Do not run test files directly with `python tests/test_*.py` as this will cause import errors. Always use `pytest` or the test runner script.

### Test Structure

- **Unit Tests**: Test individual components in isolation
  - `test_maze_generator.py` - Maze generation validation
  - `test_maze_solver.py` - Solver coordination logic  
  - `test_dfs.py` - Depth-First Search algorithm
  - `test_bfs.py` - Breadth-First Search algorithm
  - `test_dijkstra.py` - Dijkstra's algorithm
- **Integration Tests**: Test component interactions
- **Performance Tests**: Benchmark and stress testing

### Test Coverage

The test suite covers:
- Algorithm correctness and optimality
- Maze generation and structure validation
- Edge cases and error handling
- Performance characteristics
- Component integration

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation
- ⭐ Add new algorithms

## 📋 Roadmap

- [ ] A* pathfinding algorithm
- [ ] Animated step-by-step solving
- [ ] Maze saving/loading
- [ ] Different maze generation algorithms
- [ ] Performance benchmarking
- [ ] Web-based version

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pygame](https://pygame.org) for graphics and interaction
- Inspired by classic maze-solving algorithms
- Created for educational purposes

## 📞 Support

If you have questions or need help:
- 📫 Open an [issue](https://github.com/yourusername/maze-solver-visualizer/issues)
- 💬 Start a [discussion](https://github.com/yourusername/maze-solver-visualizer/discussions)
- ⭐ Star this repository if you find it helpful!

---

**Author:** CS5001 Final Project  
**Date:** November 23, 2025  
**Version:** 1.0.0