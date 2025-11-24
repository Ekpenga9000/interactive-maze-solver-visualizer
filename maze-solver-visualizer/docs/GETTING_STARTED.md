# Getting Started with Maze Solver & Visualizer

Welcome to the Maze Solver & Visualizer project! This guide will help you get up and running quickly.

## Quick Start (5 minutes)

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/maze-solver-visualizer.git
cd maze-solver-visualizer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Basic Controls
- **G** - Generate new maze
- **S** - Solve current maze  
- **1/2/3** - Switch algorithms
- **Q** - Quit

That's it! You now have a working maze solver.

## Understanding the Application

### What You'll See
When you run the application, you'll see:
- **Black areas**: Walls you cannot pass through
- **White areas**: Open paths you can walk on
- **Green square**: Starting position (top-left)
- **Red square**: Goal position (bottom-right)

### How to Use It
1. **Generate a maze**: Press 'G' to create a new random maze
2. **Choose algorithm**: Press '1' (DFS), '2' (BFS), or '3' (Dijkstra)
3. **Solve the maze**: Press 'S' to watch the algorithm work
4. **Observe the solution**:
   - **Light blue**: Areas the algorithm explored
   - **Yellow**: The final solution path

### Algorithm Comparison
Try the same maze with different algorithms:
1. Generate a maze (G)
2. Solve with DFS (1, then S)
3. Switch to BFS (2, then S)  
4. Switch to Dijkstra (3, then S)

Notice how each algorithm explores the maze differently!

## Console Demo

For a text-based demonstration without graphics:
```bash
python demo.py
```

This shows:
- ASCII art maze representation
- Algorithm comparison statistics
- Performance metrics

## Testing Everything Works

Run the test suite:
```bash
python test_components.py
```

Expected output:
```
✓ Pygame imported successfully
✓ MazeGenerator working correctly  
✓ All solving algorithms working correctly
✓ All tests passed!
```

## Project Structure

```
maze-solver-visualizer/
├── 📁 .github/          # GitHub-specific files
├── 📁 docs/             # Documentation
├── 📄 main.py           # Start here! Main application
├── 📄 maze_generator.py # Creates random mazes
├── 📄 maze_solver.py    # Pathfinding algorithms
├── 📄 maze_visualizer.py# Graphics and user interface
├── 📄 demo.py           # Console demonstration
├── 📄 test_components.py# Test everything works
└── 📄 requirements.txt  # What to install
```

## Understanding the Code

### For Beginners
Start with these files in order:
1. `main.py` - See how everything starts
2. `maze_generator.py` - Understand maze creation
3. `maze_solver.py` - Learn the algorithms
4. `demo.py` - See a simple example

### For Advanced Users
- Check `docs/ARCHITECTURE.md` for design decisions
- Read `docs/ALGORITHMS.md` for algorithm details
- Review `test_components.py` for testing approach

## Common Issues

### "No module named pygame"
```bash
pip install pygame
```

### "Permission denied" or "Cannot find python"
Make sure you've activated your virtual environment:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Application window doesn't open
Try running the console demo instead:
```bash
python demo.py
```

### Maze appears all black
This usually means the maze generation failed. Try:
1. Restart the application
2. Press 'G' to generate a new maze
3. Check the console for error messages

## Next Steps

### Experiment with Different Sizes
Edit `main.py` to try different maze dimensions:
```python
visualizer = MazeVisualizer(
    window_width=1200,    # Bigger window
    window_height=800,
    maze_width=61,        # Larger maze (must be odd)
    maze_height=41
)
```

### Learn the Algorithms
- Read `docs/ALGORITHMS.md` for detailed explanations
- Try to predict which algorithm will be fastest
- Observe the different exploration patterns

### Contribute
- Report bugs or suggest features
- Add new algorithms
- Improve the documentation
- See `CONTRIBUTING.md` for guidelines

## Educational Value

This project teaches:
- **Algorithm Design**: How different strategies solve the same problem
- **Data Structures**: Stacks, queues, priority queues, graphs
- **Software Architecture**: Modular design and separation of concerns  
- **Visualization**: Making algorithms understandable through graphics
- **Testing**: Ensuring code reliability and correctness

## Resources for Learning More

### Algorithms
- [Visualgo](https://visualgo.net/en/dfsbfs) - Interactive algorithm visualizations
- [CS50 Introduction to Computer Science](https://cs50.harvard.edu/x/) - Excellent algorithms course

### Python and Pygame
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Official Python tutorial
- [Pygame Documentation](https://www.pygame.org/docs/) - Learn game development

### Pathfinding
- [Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - Excellent pathfinding tutorials
- [Amit's Game Programming Information](http://theory.stanford.edu/~amitp/GameProgramming/) - Comprehensive game algorithms

## Getting Help

If you need help:
1. 📖 Check this documentation
2. 🐛 Search existing [issues](https://github.com/yourusername/maze-solver-visualizer/issues)
3. ❓ Ask a [question](https://github.com/yourusername/maze-solver-visualizer/discussions)
4. 🚨 Report a [bug](https://github.com/yourusername/maze-solver-visualizer/issues/new)

Happy maze solving! 🎯