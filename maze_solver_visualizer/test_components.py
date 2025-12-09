"""
Test script for the Maze Solver & Visualizer
Tests all components without requiring GUI interaction
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_maze_generator():
    """Test the maze generator"""
    print("Testing Maze Generator...")
    from maze_generator import MazeGenerator
    
    generator = MazeGenerator(21, 15)
    maze_graph = generator.generate()  # This returns ExplicitGraph
    maze = generator.generate_legacy_maze()  # This returns 2D array for testing
    
    assert len(maze) == 15, "Maze height incorrect"
    assert len(maze[0]) == 21, "Maze width incorrect"
    assert maze[1][1] == 0, "Start position not clear"
    assert maze[13][19] == 0, "End position not clear"
    
    print("✓ Maze Generator working correctly")

def test_maze_solver():
    """Test the maze solver algorithms"""
    print("Testing Maze Solver...")
    from maze_generator import MazeGenerator
    from maze_solver import MazeSolver, Algorithm
    
    # Create a simple test maze
    generator = MazeGenerator(21, 15)
    maze_graph = generator.generate()  # ExplicitGraph for solver
    solver = MazeSolver(maze_graph)
    
    start = generator.get_start_position()
    end = generator.get_end_position()
    
    # Test DFS
    path_dfs, visited_dfs = solver.solve(start, end, Algorithm.DFS)
    assert len(path_dfs) > 0, "DFS failed to find path"
    assert path_dfs[0] == start, "DFS path doesn't start correctly"
    assert path_dfs[-1] == end, "DFS path doesn't end correctly"
    
    # Test BFS
    path_bfs, visited_bfs = solver.solve(start, end, Algorithm.BFS)
    assert len(path_bfs) > 0, "BFS failed to find path"
    assert path_bfs[0] == start, "BFS path doesn't start correctly"
    assert path_bfs[-1] == end, "BFS path doesn't end correctly"
    
    # Test Dijkstra
    path_dijkstra, visited_dijkstra = solver.solve(start, end, Algorithm.DIJKSTRA)
    assert len(path_dijkstra) > 0, "Dijkstra failed to find path"
    assert path_dijkstra[0] == start, "Dijkstra path doesn't start correctly"
    assert path_dijkstra[-1] == end, "Dijkstra path doesn't end correctly"
    
    print("✓ All solving algorithms working correctly")
    print(f"  - DFS path length: {len(path_dfs)}")
    print(f"  - BFS path length: {len(path_bfs)}")
    print(f"  - Dijkstra path length: {len(path_dijkstra)}")

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        import pygame
        print(f"✓ Pygame imported successfully (version {pygame.version.ver})")
    except ImportError as e:
        print(f"✗ Failed to import pygame: {e}")
        return False
    
    try:
        from maze_generator import MazeGenerator
        print("✓ MazeGenerator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MazeGenerator: {e}")
        return False
    
    try:
        from maze_solver import MazeSolver, Algorithm
        print("✓ MazeSolver imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MazeSolver: {e}")
        return False
    
    try:
        from maze_visualizer import MazeVisualizer
        print("✓ MazeVisualizer imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MazeVisualizer: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Maze Solver & Visualizer - Component Tests")
    print("=" * 50)
    
    if not test_imports():
        print("\n✗ Import tests failed!")
        return
    
    try:
        test_maze_generator()
        test_maze_solver()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed! The maze solver is ready to use.")
        print("\nTo run the visualizer, execute: python main.py")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()