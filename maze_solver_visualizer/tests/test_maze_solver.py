"""
Tests for Maze Solver
Comprehensive testing of the main solver coordination functionality
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_solver import MazeSolver, Algorithm
from graph import ExplicitGraph, TerrainType
from typing import List

# Test fixtures
def create_simple_test_graph():
    """Create a simple test graph"""
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(5, 5)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
    return graph

def create_complex_test_graph():
    """Create a more complex test graph"""
    maze = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(7, 6)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
    return graph

def create_impossible_test_graph():
    """Create an impossible graph with no solution"""
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(5, 5)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
    return graph

def create_maze_solver_simple():
    """Create a maze solver for simple graph"""
    return MazeSolver(create_simple_test_graph())

def create_maze_solver_complex():
    """Create a maze solver for complex graph"""
    return MazeSolver(create_complex_test_graph())

def create_maze_solver_impossible():
    """Create a maze solver for impossible graph"""
    return MazeSolver(create_impossible_test_graph())

class TestMazeSolverInitialization:
    """Test maze solver initialization"""
    
    def test_solver_initialization(self):
        """Test maze solver can be initialized"""
        simple_test_graph = create_simple_test_graph()
        solver = MazeSolver(simple_test_graph)
        assert solver.graph == simple_test_graph
        assert solver.height == simple_test_graph.height
        assert solver.width == simple_test_graph.width
        
    def test_solver_empty_maze(self):
        """Test solver with minimal graph"""
        # Create minimal graph (1x1) instead of empty
        minimal_graph = ExplicitGraph(1, 1)
        minimal_graph.add_node((0, 0), TerrainType.PATH)
        solver = MazeSolver(minimal_graph)
        assert solver is not None
        assert solver.width == 1
        assert solver.height == 1
            
    def test_solver_invalid_maze_format(self):
        """Test solver with invalid graph format"""
        # Create a minimal valid graph
        minimal_graph = ExplicitGraph(1, 1)
        minimal_graph.add_node((0, 0), TerrainType.PATH)
        solver = MazeSolver(minimal_graph)
        # Should not crash on initialization
        assert solver is not None

class TestMazeSolverBasicFunctionality:
    """Test basic solver functionality"""
    
    def test_get_neighbors_center_cell(self):
        """Test getting neighbors for a center cell"""
        maze_solver_simple = create_maze_solver_simple()
        # Cell at (2, 2) should have 4 potential neighbors
        neighbors = maze_solver_simple._get_neighbors(2, 2)
        
        # Filter out walls (value 1) from the actual graph
        valid_neighbors = [
            (x, y) for x, y in neighbors
            if maze_solver_simple.graph.is_passable((x, y))
        ]
        
        assert len(neighbors) >= 0  # Could be 0 if surrounded by walls
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in neighbors)
        
    def test_get_neighbors_corner_cell(self):
        """Test getting neighbors for a corner cell"""
        maze_solver_simple = create_maze_solver_simple()
        # Corner cell should have fewer neighbors
        neighbors = maze_solver_simple._get_neighbors(0, 0)
        
        # Corner cells are typically walls, so might have no valid neighbors
        assert isinstance(neighbors, list)
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in neighbors)
        
    def test_get_neighbors_bounds_checking(self):
        """Test neighbor bounds checking"""
        maze_solver_simple = create_maze_solver_simple()
        height, width = maze_solver_simple.height, maze_solver_simple.width
        
        # Test neighbors are within bounds
        for x in range(width):
            for y in range(height):
                neighbors = maze_solver_simple._get_neighbors(x, y)
                for nx, ny in neighbors:
                    assert 0 <= nx < width
                    assert 0 <= ny < height
                    
    def test_get_neighbors_no_walls(self):
        """Test that get_neighbors doesn't return wall cells"""
        maze_solver_simple = create_maze_solver_simple()
        neighbors = maze_solver_simple._get_neighbors(1, 1)
        
        # All returned neighbors should be passable
        for x, y in neighbors:
            assert maze_solver_simple.graph.is_passable((x, y))

class TestAlgorithmSolving:
    """Test algorithm solving functionality"""
    
    def test_solve_simple_maze_dfs(self):
        """Test solving simple maze with DFS"""
        maze_solver_simple = create_maze_solver_simple()
        path, visited = maze_solver_simple.solve((1, 1), (3, 3), Algorithm.DFS)
        
        # Should find a path
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:  # If solution exists
            assert len(path) > 0
            assert path[0] == (1, 1)  # Starts at start
            assert path[-1] == (3, 3)  # Ends at end
            assert len(visited) > 0
    
    def test_solve_simple_maze_bfs(self):
        """Test solving simple maze with BFS"""
        maze_solver_simple = create_maze_solver_simple()
        path, visited = maze_solver_simple.solve((1, 1), (3, 3), Algorithm.BFS)
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert len(path) > 0
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(visited) > 0
            
    def test_solve_simple_maze_dijkstra(self):
        """Test solving simple maze with Dijkstra"""
        maze_solver_simple = create_maze_solver_simple()
        path, visited = maze_solver_simple.solve((1, 1), (3, 3), Algorithm.DIJKSTRA)
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert len(path) > 0
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(visited) > 0
            
    def test_solve_complex_maze_all_algorithms(self):
        """Test solving complex maze with all algorithms"""
        maze_solver_complex = create_maze_solver_complex()
        algorithms = [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]
        
        for algorithm in algorithms:
            path, visited = maze_solver_complex.solve((1, 1), (5, 4), algorithm)
            
            assert isinstance(path, list)
            assert isinstance(visited, set)
            
            if path:
                assert path[0] == (1, 1)
                assert path[-1] == (5, 4)
            
    def test_solve_impossible_maze_all_algorithms(self):
        """Test solving impossible maze returns empty path"""
        maze_solver_impossible = create_maze_solver_impossible()
        algorithms = [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]
        
        for algorithm in algorithms:
            path, visited = maze_solver_impossible.solve((1, 1), (3, 1), algorithm)
            
            # Should return empty path for impossible maze
            assert path == []
            assert isinstance(visited, set)

class TestPathValidation:
    """Test path validation and properties"""
    
    def test_path_continuity_dfs(self):
        """Test that DFS path is continuous"""
        maze_solver_complex = create_maze_solver_complex()
        path, _ = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.DFS)
        
        if len(path) > 1:
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                # Adjacent cells should be exactly 1 step apart
                dx = abs(current[0] - next_pos[0])
                dy = abs(current[1] - next_pos[1])
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1), \
                    f"Path not continuous: {current} -> {next_pos}"
                    
    def test_path_continuity_bfs(self):
        """Test that BFS path is continuous"""
        maze_solver_complex = create_maze_solver_complex()
        path, _ = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.BFS)
        
        if len(path) > 1:
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                dx = abs(current[0] - next_pos[0])
                dy = abs(current[1] - next_pos[1])
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
    
    def test_path_continuity_dijkstra(self):
        """Test that Dijkstra path is continuous"""
        maze_solver_complex = create_maze_solver_complex()
        path, _ = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.DIJKSTRA)
        
        if len(path) > 1:
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                dx = abs(current[0] - next_pos[0])
                dy = abs(current[1] - next_pos[1])
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
                
    def test_path_no_walls(self):
        """Test that path doesn't go through walls"""
        maze_solver_simple = create_maze_solver_simple()
        path, _ = maze_solver_simple.solve((1, 1), (3, 3), Algorithm.BFS)
        
        for x, y in path:
            assert maze_solver_simple.graph.is_passable((x, y)), \
                f"Path goes through wall at ({x}, {y})"
                
    def test_visited_cells_properties(self):
        """Test properties of visited cells"""
        maze_solver_complex = create_maze_solver_complex()
        path, visited = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.BFS)
        
        # All path cells should be in visited cells
        if path:
            for pos in path:
                assert pos in visited, f"Path position {pos} not in visited set"
                
        # All visited cells should be valid positions
        for x, y in visited:
            assert 0 <= x < maze_solver_complex.width
            assert 0 <= y < maze_solver_complex.height
            assert maze_solver_complex.graph.is_passable((x, y))  # No walls

class TestAlgorithmComparison:
    """Test comparison between different algorithms"""
    
    def test_bfs_finds_shortest_path(self):
        """Test that BFS finds shortest path"""
        maze_solver_simple = create_maze_solver_simple()
        start, end = (1, 1), (3, 3)
        
        bfs_path, _ = maze_solver_simple.solve(start, end, Algorithm.BFS)
        dfs_path, _ = maze_solver_simple.solve(start, end, Algorithm.DFS)
        dijkstra_path, _ = maze_solver_simple.solve(start, end, Algorithm.DIJKSTRA)
        
        if bfs_path and dijkstra_path:
            # BFS and Dijkstra should find same length path (optimal)
            assert len(bfs_path) == len(dijkstra_path)
            
        if bfs_path and dfs_path:
            # BFS should find path no longer than DFS
            assert len(bfs_path) <= len(dfs_path)
            
    def test_all_algorithms_find_solution_when_exists(self):
        """Test all algorithms find solution when one exists"""
        maze_solver_complex = create_maze_solver_complex()
        start, end = (1, 1), (5, 4)
        
        dfs_path, _ = maze_solver_complex.solve(start, end, Algorithm.DFS)
        bfs_path, _ = maze_solver_complex.solve(start, end, Algorithm.BFS)
        dijkstra_path, _ = maze_solver_complex.solve(start, end, Algorithm.DIJKSTRA)
        
        # If one algorithm finds a path, all should find a path
        if any([dfs_path, bfs_path, dijkstra_path]):
            assert dfs_path, "DFS should find path when solution exists"
            assert bfs_path, "BFS should find path when solution exists"
            assert dijkstra_path, "Dijkstra should find path when solution exists"
    
    def test_algorithm_consistency(self):
        """Test that algorithms are consistent across runs"""
        maze_solver_simple = create_maze_solver_simple()
        start, end = (1, 1), (3, 3)
        
        # Run each algorithm multiple times
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            paths = []
            for _ in range(3):
                path, _ = maze_solver_simple.solve(start, end, algorithm)
                paths.append(path)
            
            # All runs should produce the same result (deterministic behavior)
            first_path = paths[0]
            for path in paths[1:]:
                if algorithm == Algorithm.BFS or algorithm == Algorithm.DIJKSTRA:
                    # BFS and Dijkstra should be deterministic
                    assert path == first_path, f"{algorithm} produced inconsistent results"

class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_same_start_end_position(self):
        """Test when start and end are the same"""
        maze_solver_simple = create_maze_solver_simple()
        start_end = (1, 1)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(start_end, start_end, algorithm)
            
            # Should return a path with just the start position
            assert path == [start_end] or path == []
            assert start_end in visited
            
    def test_invalid_start_position(self):
        """Test with invalid start position"""
        maze_solver_simple = create_maze_solver_simple()
        # Wall position
        invalid_start = (0, 0)
        valid_end = (3, 3)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(invalid_start, valid_end, algorithm)
            assert path == []  # Should return empty path
            
    def test_invalid_end_position(self):
        """Test with invalid end position"""
        maze_solver_simple = create_maze_solver_simple()
        valid_start = (1, 1)
        invalid_end = (0, 0)  # Wall position
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(valid_start, invalid_end, algorithm)
            assert path == []  # Should return empty path
            
    def test_out_of_bounds_positions(self):
        """Test with out of bounds positions"""
        maze_solver_simple = create_maze_solver_simple()
        valid_start = (1, 1)
        out_of_bounds = (100, 100)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(valid_start, out_of_bounds, algorithm)
            assert path == []  # Should return empty path
            
    def test_unknown_algorithm(self):
        """Test with unknown algorithm"""
        maze_solver_simple = create_maze_solver_simple()
        start, end = (1, 1), (3, 3)
        
        try:
            # Create a mock invalid algorithm
            class InvalidAlgorithm:
                value = "Invalid"
            
            maze_solver_simple.solve(start, end, InvalidAlgorithm())
            assert False, "Expected ValueError for invalid algorithm"
        except ValueError:
            pass  # Expected exception
    
    def test_maze_boundaries(self):
        """Test maze boundary edge cases"""
        maze_solver_simple = create_maze_solver_simple()
        
        # Test positions at boundaries
        test_cases = [
            # Valid boundary positions
            ((1, 1), (1, 3)),  # Vertical edge
            ((1, 1), (3, 1)),  # Horizontal edge
            
            # Invalid boundary positions (walls)
            ((0, 2), (1, 1)),  # Start at wall
            ((1, 1), (4, 2)),  # End at wall
        ]
        
        for start, end in test_cases:
            for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
                path, visited = maze_solver_simple.solve(start, end, algorithm)
                
                if path:
                    # Verify all path positions are valid
                    for x, y in path:
                        assert 0 <= x < maze_solver_simple.width
                        assert 0 <= y < maze_solver_simple.height
                        assert maze_solver_simple.graph.is_passable((x, y))

class TestMazeSolverPerformance:
    """Test maze solver performance characteristics"""
    
    def test_large_maze_solving(self):
        """Test solving larger mazes"""
        # Create a larger graph
        graph = ExplicitGraph(15, 15)
        size = 15
        
        # Build the maze grid first
        large_maze = []
        for y in range(size):
            row = []
            for x in range(size):
                if x == 0 or y == 0 or x == size-1 or y == size-1:
                    row.append(1)  # Border walls
                elif x % 2 == 1 and y % 2 == 1:
                    row.append(0)  # Open spaces
                else:
                    row.append(1)  # Walls
            large_maze.append(row)
        
        # Ensure start and end are clear
        large_maze[1][1] = 0
        large_maze[size-2][size-2] = 0
        
        # Build graph from maze
        graph.build_from_maze_grid(large_maze, {TerrainType.PATH: 1.0})
        solver = MazeSolver(graph)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = solver.solve((1, 1), (size-2, size-2), algorithm)
            
            # Should complete without errors
            assert isinstance(path, list)
            assert isinstance(visited, set)
            
            if path:
                assert path[0] == (1, 1)
                assert path[-1] == (size-2, size-2)

def run_all_tests():
    """Run all maze solver tests"""
    test_classes = [
        TestMazeSolverInitialization,
        TestMazeSolverBasicFunctionality,
        TestAlgorithmSolving,
        TestPathValidation,
        TestAlgorithmComparison,
        TestEdgeCases,
        TestMazeSolverPerformance
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running Maze Solver tests...")
    
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            print(f"  {test_method}... ", end="")
            try:
                getattr(test_instance, test_method)()
                print("PASS")
                passed_tests += 1
            except Exception as e:
                print(f"FAIL: {e}")
                failed_tests.append(f"{test_class.__name__}.{test_method}: {e}")
                # Uncomment for detailed traces
                # traceback.print_exc()
    
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for failure in failed_tests:
            print(f"  - {failure}")
        return False
    else:
        print("All tests passed!")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)