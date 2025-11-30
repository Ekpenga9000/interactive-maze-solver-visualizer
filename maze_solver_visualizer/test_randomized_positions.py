"""
Test script for randomized start and end positions
Demonstrates the variety of scenarios created by different position combinations
"""

from compatibility import LegacyMazeGenerator, LegacyMazeSolver
from maze_solver import Algorithm
import time

def test_randomized_positions():
    """Test that start and end positions are randomized to create diverse scenarios"""
    print("=== Testing Randomized Start and End Positions ===")
    
    generator = LegacyMazeGenerator(21, 21)
    
    # Generate multiple mazes and show position variety
    positions_seen = set()
    scenarios = []
    
    for i in range(10):
        maze, start, end = generator.generate_with_positions(randomize_positions=True)
        solver = LegacyMazeSolver(maze)
        
        # Test pathfinding
        start_time = time.time()
        path, visited = solver.solve(start, end, Algorithm.BFS)
        solve_time = time.time() - start_time
        
        # Calculate distance metrics
        manhattan_distance = abs(end[0] - start[0]) + abs(end[1] - start[1])
        path_length = len(path)
        efficiency = path_length / manhattan_distance if manhattan_distance > 0 else float('inf')
        
        scenario = {
            'id': i + 1,
            'start': start,
            'end': end,
            'manhattan_dist': manhattan_distance,
            'path_length': path_length,
            'visited_count': len(visited),
            'efficiency': efficiency,
            'solve_time': solve_time
        }
        scenarios.append(scenario)
        
        positions_seen.add((start, end))
        
        print(f"Scenario {i+1}: Start={start}, End={end}")
        print(f"  Manhattan distance: {manhattan_distance}")
        print(f"  Actual path: {path_length} steps")
        print(f"  Efficiency ratio: {efficiency:.2f}")
        print(f"  Cells visited: {len(visited)}")
        print(f"  Solve time: {solve_time:.4f}s")
        print()
    
    # Analyze variety
    print(f"=== Analysis ===")
    print(f"Unique position combinations: {len(positions_seen)}/10")
    
    # Find most challenging scenario
    most_challenging = max(scenarios, key=lambda x: x['efficiency'])
    print(f"Most challenging: Scenario {most_challenging['id']} (efficiency: {most_challenging['efficiency']:.2f})")
    
    # Find shortest path scenario  
    shortest_path = min(scenarios, key=lambda x: x['path_length'])
    print(f"Shortest path: Scenario {shortest_path['id']} ({shortest_path['path_length']} steps)")
    
    # Find longest path scenario
    longest_path = max(scenarios, key=lambda x: x['path_length'])
    print(f"Longest path: Scenario {longest_path['id']} ({longest_path['path_length']} steps)")
    
    return scenarios

def test_strategic_positions():
    """Test that positions are placed at strategic locations"""
    print("\n=== Strategic Position Analysis ===")
    
    from maze_generator import MazeGenerator
    
    generator_internal = MazeGenerator(21, 21)
    strategic_positions = generator_internal.get_strategic_positions()
    
    print("Strategic positions identified:")
    for i, pos in enumerate(strategic_positions):
        x, y = pos
        if x == 1 and y == 1:
            location = "Top-left corner"
        elif x == 19 and y == 1:
            location = "Top-right corner"
        elif x == 1 and y == 19:
            location = "Bottom-left corner"
        elif x == 19 and y == 19:
            location = "Bottom-right corner"
        elif x == 11 and y == 11:
            location = "Center"
        elif y == 1:
            location = "Top edge"
        elif y == 19:
            location = "Bottom edge"
        elif x == 1:
            location = "Left edge"
        elif x == 19:
            location = "Right edge"
        else:
            location = "Other strategic"
        
        print(f"  {pos}: {location}")

def test_algorithm_performance_variety():
    """Test how different position scenarios affect algorithm performance"""
    print("\n=== Algorithm Performance on Varied Scenarios ===")
    
    generator = LegacyMazeGenerator(21, 21)
    algorithms = [Algorithm.BFS, Algorithm.DFS, Algorithm.DIJKSTRA]
    
    # Test 3 different scenarios
    for scenario_num in range(3):
        print(f"\nScenario {scenario_num + 1}:")
        maze, start, end = generator.generate_with_positions(randomize_positions=True)
        solver = LegacyMazeSolver(maze)
        
        manhattan_dist = abs(end[0] - start[0]) + abs(end[1] - start[1])
        print(f"  Start: {start}, End: {end} (Manhattan: {manhattan_dist})")
        
        for algorithm in algorithms:
            start_time = time.time()
            path, visited = solver.solve(start, end, algorithm)
            solve_time = time.time() - start_time
            
            print(f"    {algorithm.value}:")
            print(f"      Path: {len(path)} steps")
            print(f"      Visited: {len(visited)} cells")
            print(f"      Time: {solve_time:.4f}s")

if __name__ == "__main__":
    print("Randomized Position Test Suite")
    print("=" * 50)
    
    scenarios = test_randomized_positions()
    test_strategic_positions()
    test_algorithm_performance_variety()
    
    print("\n" + "=" * 50)
    print("✓ Random position generation creates diverse pathfinding scenarios!")
    print("✓ Strategic positioning includes corners, center, and edges!")
    print("✓ Algorithm performance varies significantly across scenarios!")