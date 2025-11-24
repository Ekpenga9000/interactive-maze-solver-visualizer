# Contributing to Maze Solver & Visualizer

Thank you for your interest in contributing to the Maze Solver & Visualizer project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/yourusername/maze-solver-visualizer/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, Pygame version)

### Suggesting Features

1. Check existing issues for similar feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Include docstrings for new functions/classes
4. **Test your changes**:
   - Run `python test_components.py`
   - Test the GUI application
   - Ensure all algorithms work correctly
5. **Commit your changes**: `git commit -m "Add your feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Submit a Pull Request**

## Code Style Guidelines

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Add type hints where appropriate

## Algorithm Contributions

If you want to add new pathfinding algorithms:

1. Add the new algorithm to the `Algorithm` enum in `maze_solver.py`
2. Implement the algorithm method in the `MazeSolver` class
3. Follow the same return format: `(path, visited_cells)`
4. Add the algorithm to the visualizer controls
5. Update documentation and tests

## Testing

Before submitting a pull request:

1. Run the component tests: `python test_components.py`
2. Test the main application: `python main.py`
3. Run the demo: `python demo.py`
4. Verify all algorithms work correctly
5. Test on different maze sizes

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Reach out to the maintainers

Thank you for contributing!