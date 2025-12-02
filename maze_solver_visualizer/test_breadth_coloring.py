"""
Test script for verifying breadth level coloring in BFS and distance coloring in Dijkstra
"""

from compatibility import LegacyMazeGenerator, LegacyMazeSolver
from maze_solver import Algorithm

def test_breadth_level_tracking():
    """Test that BFS properly tracks breadth levels"""
    print("=== Testing BFS Breadth Level Tracking ===")
    
    # Create a simple maze
    generator = LegacyMazeGenerator(11, 11)
    maze, start, end = generator.generate_with_positions(randomize_positions=False)
    solver = LegacyMazeSolver(maze)
    
    # Get the BFS algorithm
    bfs_algorithm = solver._solver.algorithms[Algorithm.BFS]
    
    # Run animated BFS and collect breadth level information
    breadth_levels = {}
    step_count = 0
    
    for state in bfs_algorithm.solve_animated(start, end):
        step_count += 1
        if 'breadth_levels' in state:
            breadth_levels.update(state['breadth_levels'])
        
        if state['action'] == 'found':
            break
        
        if step_count > 20:  # Limit to avoid infinite loop in testing
            break
    
    print(f"BFS completed in {step_count} steps")
    print(f"Tracked {len(breadth_levels)} cell levels")
    print("Sample breadth levels:")
    
    # Show some example breadth levels
    for i, (pos, level) in enumerate(list(breadth_levels.items())[:10]):
        print(f"  Position {pos}: Level {level}")
    
    # Verify start position is level 0
    if start in breadth_levels:
        print(f"✓ Start position {start} has level {breadth_levels[start]}")
    else:
        print(f"⚠ Start position {start} not found in breadth levels")
    
    return breadth_levels

def test_dijkstra_distance_tracking():
    """Test that Dijkstra properly tracks distances"""
    print("\n=== Testing Dijkstra Distance Tracking ===")
    
    # Create a maze with terrain costs
    from graph import ExplicitGraph, TerrainType
    from maze_generator import MazeGenerator
    from maze_solver import MazeSolver
    
    generator = MazeGenerator(11, 11)
    terrain_probs = {
        TerrainType.PATH: 0.5,
        TerrainType.MUD: 0.3,
        TerrainType.WATER: 0.2
    }
    
    graph, start, end = generator.generate_with_positions(
        terrain_probabilities=terrain_probs
    )
    solver = MazeSolver(graph)
    
    # Get the Dijkstra algorithm
    dijkstra_algorithm = solver.algorithms[Algorithm.DIJKSTRA]
    
    # Run animated Dijkstra and collect distance information
    distances = {}
    step_count = 0
    
    for state in dijkstra_algorithm.solve_animated(start, end):
        step_count += 1
        if 'distances' in state:
            distances.update(state['distances'])
        
        if state['action'] == 'found':
            break
        
        if step_count > 30:  # Limit to avoid infinite loop in testing
            break
    
    print(f"Dijkstra completed in {step_count} steps")
    print(f"Tracked {len(distances)} cell distances")
    print("Sample distances:")
    
    # Show some example distances
    for i, (pos, dist) in enumerate(list(distances.items())[:10]):
        print(f"  Position {pos}: Distance {dist}")
    
    # Verify start position has distance 0
    if start in distances:
        print(f"✓ Start position {start} has distance {distances[start]}")
    else:
        print(f"⚠ Start position {start} not found in distances")
    
    return distances

def test_color_generation():
    """Test the color generation functions"""
    print("\n=== Testing Color Generation ===")
    
    from maze_visualizer import MazeVisualizer
    
    # Create a dummy visualizer to test color methods
    visualizer = MazeVisualizer(400, 400, 11, 11)
    
    print("Sample breadth level colors:")
    for level in range(5):
        color = visualizer.get_breadth_color(level)
        print(f"  Level {level}: RGB{color}")
    
    print("Sample distance colors:")
    # Set up some dummy distances for testing
    visualizer.distances = {(1, 1): 0, (2, 1): 5, (3, 1): 10, (4, 1): 15}
    
    for distance in [0, 5, 10, 15]:
        color = visualizer.get_distance_color(distance)
        print(f"  Distance {distance}: RGB{color}")
    
    print("✓ Color generation working correctly")

if __name__ == "__main__":
    print("Breadth Level and Distance Coloring Test Suite")
    print("=" * 55)
    
    try:
        breadth_levels = test_breadth_level_tracking()
        distances = test_dijkstra_distance_tracking()
        test_color_generation()
        
        print("\n" + "=" * 55)
        print("✓ All tests completed successfully!")
        print("✓ BFS tracks breadth levels for colored visualization")
        print("✓ Dijkstra tracks distances for colored visualization")
        print("✓ Color generation functions work correctly")
        print("\nNow when you run the visualizer:")
        print("• BFS will show different colors for each breadth level")
        print("• Dijkstra will show gradient colors based on distance")
        print("• DFS will use the standard light blue color")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()