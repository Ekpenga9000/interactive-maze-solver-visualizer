"""
Demo script showing maze generation and solving algorithms
Runs without GUI to demonstrate the core functionality
"""

from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm

def print_maze(maze, path=None, visited=None, start=None, end=None):
    """Print maze to console with optional path visualization"""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            pos = (x, y)
            if start and pos == start:
                print('S', end='')  # Start
            elif end and pos == end:
                print('E', end='')  # End
            elif path and pos in path:
                print('*', end='')  # Path
            elif visited and pos in visited:
                print('.', end='')  # Visited
            elif cell == 1:
                print('█', end='')  # Wall
            else:
                print(' ', end='')  # Open space
        print()  # New line

def demo_algorithm(solver, start, end, algorithm, maze):
    """Demonstrate a specific algorithm"""
    print(f"\n{algorithm.value}")
    print("=" * len(algorithm.value))
    
    path, visited = solver.solve(start, end, algorithm)
    
    if path:
        print(f"Path found! Length: {len(path)} steps")
        print(f"Cells explored: {len(visited)}")
        print("\nMaze with solution:")
        print_maze(maze, path=path, visited=visited, start=start, end=end)
    else:
        print("No path found!")
    
    return len(path) if path else 0, len(visited)

def main():
    """Main demo function"""
    print("Maze Solver & Visualizer - Algorithm Demo")
    print("=" * 50)
    
    # Create a smaller maze for console display
    print("Generating maze...")
    generator = MazeGenerator(25, 15)
    maze_graph = generator.generate()  # This returns an ExplicitGraph
    legacy_maze = generator.generate_legacy_maze()  # This returns 2D array for display
    start = generator.get_start_position()
    end = generator.get_end_position()
    
    print(f"Maze size: {len(legacy_maze[0])} x {len(legacy_maze)}")
    print(f"Start: {start}, End: {end}")
    
    print("\nOriginal maze:")
    print_maze(legacy_maze, start=start, end=end)
    
    # Create solver
    solver = MazeSolver(maze_graph)
    
    # Test all algorithms
    algorithms = [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]
    results = {}
    
    for algorithm in algorithms:
        path_length, cells_explored = demo_algorithm(solver, start, end, algorithm, legacy_maze)
        results[algorithm.value] = {
            'path_length': path_length,
            'cells_explored': cells_explored
        }
    
    # Summary
    print("\n" + "=" * 50)
    print("ALGORITHM COMPARISON")
    print("=" * 50)
    print(f"{'Algorithm':<20} {'Path Length':<12} {'Cells Explored':<15}")
    print("-" * 50)
    
    for alg_name, result in results.items():
        print(f"{alg_name:<20} {result['path_length']:<12} {result['cells_explored']:<15}")
    
    print("\nLegend:")
    print("S = Start, E = End, * = Solution path, . = Explored cells, █ = Wall")

if __name__ == "__main__":
    main()