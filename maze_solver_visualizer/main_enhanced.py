"""
Enhanced Maze Solver & Visualizer
A program that generates random mazes and solves them using various algorithms with terrain costs:
- Depth-First Search (DFS) 
- Breadth-First Search (BFS)
- Dijkstra's Algorithm (with weighted terrain)

Features:
- Weighted pathfinding with different terrain costs
- Randomized end node placement  
- Performance-optimized explicit graph representation
- Rich terrain analysis

Author: Your Name
Date: November 30, 2025
"""

import sys
import time
from typing import Dict, Any
from graph import TerrainType
from compatibility import EnhancedMazeGenerator, EnhancedMazeSolver, LegacyMazeGenerator, LegacyMazeSolver
from maze_solver import Algorithm

def demonstrate_legacy_compatibility():
    """Show that the old interface still works"""
    print("=== Legacy Compatibility Test ===")
    
    # Use old interface
    generator = LegacyMazeGenerator(21, 21)
    maze_grid, start, end = generator.generate_with_positions()
    
    solver = LegacyMazeSolver(maze_grid)
    path, visited = solver.solve(start, end, Algorithm.BFS)
    
    print(f"Legacy maze solved: {len(path)} steps, {len(visited)} visited")
    print("✓ Legacy compatibility maintained!")

def demonstrate_enhanced_features():
    """Show the new enhanced features"""
    print("\n=== Enhanced Features Demo ===")
    
    # Create enhanced maze with terrain costs
    generator = EnhancedMazeGenerator(21, 21)
    
    terrain_probs = {
        TerrainType.PATH: 0.4,    # Fast paths
        TerrainType.MUD: 0.3,     # Slow terrain (cost 3)
        TerrainType.WATER: 0.2,   # Very slow (cost 5) 
        TerrainType.SAND: 0.1     # Moderately slow (cost 2)
    }
    
    graph, start, end = generator.generate_with_terrain(
        terrain_probabilities=terrain_probs,
        randomize_end=True
    )
    
    solver = EnhancedMazeSolver(graph)
    
    print(f"Enhanced maze: start={start}, end={end}")
    
    # Compare algorithms
    algorithms = [Algorithm.BFS, Algorithm.DIJKSTRA]
    
    for algorithm in algorithms:
        print(f"\n--- {algorithm.value} ---")
        
        start_time = time.time()
        result = solver.solve_weighted(start, end, algorithm)
        end_time = time.time()
        
        print(f"Path length: {result['path_length']} steps")
        print(f"Cells visited: {result['visited_count']}")
        print(f"Execution time: {end_time - start_time:.4f}s")
        
        if 'total_cost' in result:
            print(f"Total path cost: {result['total_cost']}")
            print("Terrain breakdown:")
            for terrain, count in result['terrain_breakdown'].items():
                print(f"  {terrain}: {count} steps")

def demonstrate_randomized_endpoints():
    """Show randomized end node placement"""
    print("\n=== Randomized End Points Demo ===")
    
    generator = EnhancedMazeGenerator(15, 15)
    graph, start, _ = generator.generate_simple()
    solver = EnhancedMazeSolver(graph)
    
    print(f"Fixed start: {start}")
    print("Random end points:")
    
    for i in range(3):
        random_end = solver.get_random_end(start)
        result = solver.solve_weighted(start, random_end, Algorithm.BFS)
        print(f"  End #{i+1}: {random_end} -> {result['path_length']} steps")

def analyze_terrain_costs():
    """Analyze how terrain costs affect pathfinding"""
    print("\n=== Terrain Cost Analysis ===")
    
    generator = EnhancedMazeGenerator(15, 15)
    
    # Create maze with mixed terrain
    terrain_probs = {
        TerrainType.PATH: 0.25,   # Cost 1
        TerrainType.SAND: 0.25,   # Cost 2  
        TerrainType.MUD: 0.25,    # Cost 3
        TerrainType.WATER: 0.25   # Cost 5
    }
    
    graph, start, end = generator.generate_with_terrain(terrain_probs)
    solver = EnhancedMazeSolver(graph)
    
    # Compare BFS (unweighted) vs Dijkstra (weighted)
    bfs_result = solver.solve_weighted(start, end, Algorithm.BFS)
    dijkstra_result = solver.solve_weighted(start, end, Algorithm.DIJKSTRA)
    
    print("BFS (ignores terrain costs):")
    print(f"  Path length: {bfs_result['path_length']} steps")
    
    print("Dijkstra (considers terrain costs):")  
    print(f"  Path length: {dijkstra_result['path_length']} steps")
    if 'total_cost' in dijkstra_result:
        print(f"  Total cost: {dijkstra_result['total_cost']}")
    
    # Calculate BFS path cost for comparison
    if bfs_result['path']:
        bfs_cost = 0
        for i, pos in enumerate(bfs_result['path']):
            if i > 0:  # Skip start position
                terrain_info = solver.analyze_terrain(pos)
                bfs_cost += terrain_info['cost']
        
        if 'total_cost' in dijkstra_result:
            savings = bfs_cost - dijkstra_result['total_cost']
            print(f"  BFS path would cost: {bfs_cost}")
            print(f"  Cost savings: {savings}")

def performance_benchmark():
    """Benchmark performance with different maze sizes"""
    print("\n=== Performance Benchmark ===")
    
    sizes = [(11, 11), (21, 21), (31, 31)]
    
    for width, height in sizes:
        print(f"\n{width}x{height} maze:")
        
        generator = EnhancedMazeGenerator(width, height)
        
        # Measure graph creation
        start_time = time.time()
        graph, start, end = generator.generate_with_terrain(randomize_end=True)
        creation_time = time.time() - start_time
        
        solver = EnhancedMazeSolver(graph)
        
        # Measure solving
        start_time = time.time()
        result = solver.solve_weighted(start, end, Algorithm.DIJKSTRA)
        solving_time = time.time() - start_time
        
        print(f"  Graph creation: {creation_time:.4f}s")
        print(f"  Pathfinding: {solving_time:.4f}s") 
        print(f"  Path found: {result['path_length']} steps")
        print(f"  Efficiency: {len(graph.get_all_passable_positions())} total / {result['visited_count']} visited")

def main():
    """Main function demonstrating all features"""
    print("Enhanced Maze Solver with Explicit Graph")
    print("=" * 50)
    
    try:
        # Test legacy compatibility
        demonstrate_legacy_compatibility()
        
        # Show new features
        demonstrate_enhanced_features()
        demonstrate_randomized_endpoints()
        analyze_terrain_costs()
        performance_benchmark()
        
        print("\n" + "=" * 50)
        print("✓ All demonstrations completed successfully!")
        print("\nKey improvements:")
        print("• Weighted pathfinding with terrain costs")
        print("• Randomized end node placement") 
        print("• Performance-optimized explicit graph")
        print("• Backward compatibility maintained")
        print("• Rich terrain and cost analysis")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()