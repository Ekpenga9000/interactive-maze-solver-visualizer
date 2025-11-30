"""
Demo script showing the new explicit graph features:
- Weighted pathfinding with different terrain costs
- Performance improvements with precomputed adjacency
- Randomized end node locations
"""

import time
from graph import ExplicitGraph, TerrainType
from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm

def demo_weighted_pathfinding():
    """Demonstrate weighted pathfinding with different terrain costs"""
    print("=== Weighted Pathfinding Demo ===")
    
    # Create a maze with explicit graph
    generator = MazeGenerator(21, 21)
    
    # Define terrain probabilities for varied terrain
    terrain_probs = {
        TerrainType.PATH: 0.4,   # Normal paths
        TerrainType.MUD: 0.3,    # Slow terrain (cost 3)
        TerrainType.WATER: 0.2,  # Very slow terrain (cost 5)
        TerrainType.SAND: 0.1    # Slightly slow terrain (cost 2)
    }
    
    graph, start, end = generator.generate_with_positions(
        randomize_end=True, 
        terrain_probabilities=terrain_probs
    )
    
    print(f"Generated maze with start: {start}, end: {end}")
    print(f"Total passable positions: {len(graph.get_all_passable_positions())}")
    
    # Create solver
    solver = MazeSolver(graph)
    
    # Compare algorithms
    algorithms_to_test = [Algorithm.BFS, Algorithm.DIJKSTRA]
    results = {}
    
    for algorithm in algorithms_to_test:
        print(f"\n--- Testing {algorithm.value} ---")
        
        # Measure performance
        start_time = time.time()
        path, visited = solver.solve(start, end, algorithm)
        end_time = time.time()
        
        results[algorithm] = {
            'path_length': len(path),
            'visited_count': len(visited),
            'execution_time': end_time - start_time,
            'path': path
        }
        
        # Calculate path cost for weighted algorithms
        if algorithm == Algorithm.DIJKSTRA and path:
            path_cost = 0
            for i in range(len(path) - 1):
                current_pos = path[i]
                next_pos = path[i + 1]
                edge_cost = graph.get_edge_weight(current_pos, next_pos)
                path_cost += edge_cost
            results[algorithm]['path_cost'] = path_cost
        
        print(f"Path found: {'Yes' if path else 'No'}")
        if path:
            print(f"Path length: {len(path)} steps")
            if 'path_cost' in results[algorithm]:
                print(f"Path cost: {results[algorithm]['path_cost']:.2f}")
        print(f"Cells visited: {len(visited)}")
        print(f"Execution time: {end_time - start_time:.4f} seconds")
    
    # Compare results
    print(f"\n=== Algorithm Comparison ===")
    if results[Algorithm.BFS]['path_length'] > 0 and results[Algorithm.DIJKSTRA]['path_length'] > 0:
        bfs_path = results[Algorithm.BFS]['path']
        dijkstra_path = results[Algorithm.DIJKSTRA]['path']
        
        print(f"BFS path length: {len(bfs_path)} steps")
        print(f"Dijkstra path length: {len(dijkstra_path)} steps")
        
        if 'path_cost' in results[Algorithm.DIJKSTRA]:
            # Calculate BFS path cost for comparison
            bfs_cost = 0
            for i in range(len(bfs_path) - 1):
                current_pos = bfs_path[i]
                next_pos = bfs_path[i + 1]
                edge_cost = graph.get_edge_weight(current_pos, next_pos)
                bfs_cost += edge_cost
            
            dijkstra_cost = results[Algorithm.DIJKSTRA]['path_cost']
            
            print(f"BFS path cost: {bfs_cost:.2f}")
            print(f"Dijkstra path cost: {dijkstra_cost:.2f}")
            print(f"Cost savings with Dijkstra: {bfs_cost - dijkstra_cost:.2f}")
    
    return graph, solver, results

def demo_randomized_end_positions():
    """Demonstrate randomized end node locations"""
    print("\n=== Randomized End Positions Demo ===")
    
    generator = MazeGenerator(15, 15)
    graph, start, _ = generator.generate_with_positions()
    solver = MazeSolver(graph)
    
    print(f"Fixed start position: {start}")
    
    # Generate multiple random end positions
    for i in range(5):
        random_end = solver.get_random_end_position(start)
        print(f"Random end #{i+1}: {random_end}")
        
        # Solve to this random end
        path, visited = solver.solve(start, random_end, Algorithm.BFS)
        print(f"  -> Path length: {len(path)} steps, Visited: {len(visited)} cells")

def demo_terrain_analysis():
    """Demonstrate terrain analysis and visualization"""
    print("\n=== Terrain Analysis Demo ===")
    
    generator = MazeGenerator(11, 11)
    
    # Create terrain with high diversity
    terrain_probs = {
        TerrainType.PATH: 0.25,
        TerrainType.MUD: 0.25,
        TerrainType.WATER: 0.25,
        TerrainType.SAND: 0.25
    }
    
    graph, start, end = generator.generate_with_positions(
        terrain_probabilities=terrain_probs
    )
    
    solver = MazeSolver(graph)
    
    # Analyze terrain distribution
    terrain_counts = {}
    for position in graph.get_all_passable_positions():
        terrain_info = solver.get_terrain_info(position)
        terrain_type = terrain_info['terrain']
        terrain_counts[terrain_type] = terrain_counts.get(terrain_type, 0) + 1
    
    print("Terrain distribution:")
    for terrain, count in terrain_counts.items():
        print(f"  {terrain}: {count} cells")
    
    # Show terrain costs
    print("\nTerrain movement costs:")
    for terrain_type in TerrainType:
        if terrain_type != TerrainType.WALL:
            print(f"  {terrain_type.name}: {terrain_type.value}")
    
    # Demonstrate terrain-aware pathfinding
    path, visited = solver.solve(start, end, Algorithm.DIJKSTRA)
    if path:
        print(f"\nPath analysis:")
        print(f"Path length: {len(path)} steps")
        
        # Analyze path terrain
        path_terrain_counts = {}
        total_cost = 0
        
        for i, position in enumerate(path):
            terrain_info = solver.get_terrain_info(position)
            terrain_type = terrain_info['terrain']
            cost = terrain_info['cost']
            
            path_terrain_counts[terrain_type] = path_terrain_counts.get(terrain_type, 0) + 1
            if i > 0:  # Don't count start position cost
                total_cost += cost
        
        print(f"Total path cost: {total_cost}")
        print("Path terrain breakdown:")
        for terrain, count in path_terrain_counts.items():
            print(f"  {terrain}: {count} steps")

def performance_comparison():
    """Compare performance between implicit and explicit graph approaches"""
    print("\n=== Performance Comparison ===")
    print("Note: This shows the explicit graph performance.")
    print("For implicit comparison, you would need to run the old implementation.")
    
    # Test with different maze sizes
    sizes = [(11, 11), (21, 21), (41, 41)]
    
    for width, height in sizes:
        print(f"\nTesting {width}x{height} maze:")
        
        generator = MazeGenerator(width, height)
        
        # Measure graph creation time
        start_time = time.time()
        graph, start, end = generator.generate_with_positions(randomize_end=True)
        creation_time = time.time() - start_time
        
        solver = MazeSolver(graph)
        
        # Measure pathfinding time
        start_time = time.time()
        path, visited = solver.solve(start, end, Algorithm.DIJKSTRA)
        solving_time = time.time() - start_time
        
        print(f"  Graph creation: {creation_time:.4f} seconds")
        print(f"  Pathfinding: {solving_time:.4f} seconds")
        print(f"  Path length: {len(path)} steps")
        print(f"  Cells visited: {len(visited)}")
        print(f"  Total passable cells: {len(graph.get_all_passable_positions())}")

if __name__ == "__main__":
    print("Explicit Graph Maze Solver Demo")
    print("=" * 40)
    
    # Run all demonstrations
    demo_weighted_pathfinding()
    demo_randomized_end_positions()
    demo_terrain_analysis()
    performance_comparison()
    
    print("\n" + "=" * 40)
    print("Demo completed! The explicit graph implementation provides:")
    print("• Weighted pathfinding with terrain costs")
    print("• Performance improvements through precomputed adjacency")
    print("• Randomized end node placement")
    print("• Rich terrain analysis capabilities")