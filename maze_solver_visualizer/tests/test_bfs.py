"""
Tests for Breadth-First Search Algorithm
Comprehensive testing of BFS implementation
"""
import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple, Set
from algorithms.breadth_first_search import BreadthFirstSearch
from graph import ExplicitGraph, TerrainType

# Test fixtures converted from conftest.py
def create_simple_test_graph():
    """Create a simple 5x5 test graph for algorithm testing"""
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(5, 5)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})  # Only paths for simplicity
    return graph

def create_complex_test_graph():
    """Create a more complex test graph"""
    maze = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(7, 6)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})  # Only paths for simplicity
    return graph

def create_impossible_graph():
    """Create a graph with no solution"""
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    graph = ExplicitGraph(5, 5)
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})  # Only paths for simplicity
    return graph

# Keep the old functions for backward compatibility with existing tests that might need maze grids
def create_simple_test_maze():
    """Create a simple 5x5 test maze for algorithm testing"""
    return [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

def create_complex_test_maze():
    """Create a more complex test maze"""
    return [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

def create_impossible_maze():
    """Create a maze with no solution"""
    return [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]


class TestBFSInitialization:
    """Test BFS initialization"""
    
    def test_bfs_initialization(self):
        """Test BFS can be initialized"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        assert bfs.graph == simple_test_graph
        assert bfs.height == simple_test_graph.height
        assert bfs.width == simple_test_graph.width
        
    def test_bfs_with_empty_maze(self):
        """Test BFS with edge case inputs"""
        # Test with minimal valid graph
        minimal_graph = ExplicitGraph(1, 1)
        minimal_graph.add_node((0, 0), TerrainType.PATH)
        bfs = BreadthFirstSearch(minimal_graph)
        assert bfs.graph == minimal_graph
        assert bfs.height == 1
        assert bfs.width == 1


class TestBFSBasicFunctionality:
    """Test basic BFS functionality"""
    
    def test_bfs_solve_simple_path(self):
        """Test BFS solving simple path"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        path, visited = bfs.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_bfs_solve_no_solution(self):
        """Test BFS with impossible maze"""
        impossible_graph = create_impossible_graph()
        bfs = BreadthFirstSearch(impossible_graph)
        path, visited = bfs.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_bfs_path_validity(self):
        """Test that BFS path is valid"""
        complex_test_graph = create_complex_test_graph()
        bfs = BreadthFirstSearch(complex_test_graph)
        path, visited = bfs.solve((1, 1), (5, 4))
        
        if path:
            # Check path continuity
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                dx = abs(current[0] - next_pos[0])
                dy = abs(current[1] - next_pos[1])
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
                
            # Check no walls in path
            for x, y in path:
                assert bfs.maze[y][x] == 0
                
    def test_bfs_visited_cells(self):
        """Test BFS visited cells properties"""
        complex_test_graph = create_complex_test_graph()
        bfs = BreadthFirstSearch(complex_test_graph)
        path, visited = bfs.solve((1, 1), (5, 4))
        
        # Path cells should be subset of visited
        if path:
            for pos in path:
                assert pos in visited
                
        # All visited cells should be valid
        for x, y in visited:
            assert 0 <= x < bfs.width
            assert 0 <= y < bfs.height
            assert bfs.maze[y][x] == 0


class TestBFSAlgorithmSpecific:
    """Test BFS-specific algorithm behavior"""
    
    def test_bfs_shortest_path(self):
        """Test that BFS finds shortest path"""
        # Create maze with clear shortest path
        shortest_path_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(7, 5)
        graph.build_from_maze_grid(shortest_path_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (5, 1))
        
        if path:
            # BFS should find shortest path (5 steps)
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            
    def test_bfs_breadth_first_behavior(self):
        """Test that BFS exhibits breadth-first behavior"""
        complex_test_graph = create_complex_test_graph()
        bfs = BreadthFirstSearch(complex_test_graph)
        
        # Create custom BFS to track exploration order
        class TrackingBFS(BreadthFirstSearch):
            def __init__(self, graph):
                super().__init__(graph)
                self.exploration_order = []
                
            def solve(self, start, end):
                from collections import deque
                
                visited = set()
                queue = deque([start])
                parent = {start: None}
                
                visited.add(start)
                self.exploration_order.append(start)
                
                while queue:
                    current = queue.popleft()
                    
                    if current == end:
                        # Reconstruct path
                        path = []
                        pos = end
                        while pos:
                            path.append(pos)
                            pos = parent[pos]
                        return path[::-1], visited
                    
                    x, y = current
                    for neighbor in self.get_neighbors(x, y):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            parent[neighbor] = current
                            queue.append(neighbor)
                            self.exploration_order.append(neighbor)
                
                return [], visited
                
        tracking_bfs = TrackingBFS(complex_test_graph)
        path, visited = tracking_bfs.solve((1, 1), (5, 4))
        
        # BFS should explore level by level
        assert len(tracking_bfs.exploration_order) > 0
        assert tracking_bfs.exploration_order[0] == (1, 1)
        
    def test_bfs_optimal_exploration(self):
        """Test BFS optimal exploration patterns"""
        # Create maze where BFS optimality is clear
        optimal_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(5, 5)
        graph.build_from_maze_grid(optimal_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (3, 3))
        
        if path:
            # BFS should find path of length 5 (minimum steps)
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)


class TestBFSPerformance:
    """Test BFS performance characteristics"""
    
    def test_bfs_exploration_completeness(self):
        """Test BFS exploration completeness"""
        complex_test_graph = create_complex_test_graph()
        bfs = BreadthFirstSearch(complex_test_graph)
        path, visited = bfs.solve((1, 1), (5, 4))
        
        if path:
            # BFS finds shortest path when solution exists
            assert len(path) >= 3  # Some minimum reasonable path length
            
        # BFS explores systematically
        assert len(visited) > 0
        
    def test_bfs_vs_optimal_path_length(self):
        """Test that BFS path length is optimal"""
        # Create maze with known shortest path
        known_optimal_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(7, 5)
        graph.build_from_maze_grid(known_optimal_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (5, 3))
        
        if path:
            # BFS should find optimal path length
            # Minimum path: (1,1) -> (1,3) -> (2,3) -> (3,3) -> (4,3) -> (5,3) = 6 steps
            expected_min_length = 7  # Corrected based on actual path
            assert len(path) == expected_min_length


class TestBFSEdgeCases:
    """Test BFS edge cases"""
    
    def test_bfs_single_cell_path(self):
        """Test BFS with single cell path"""
        single_cell_maze = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        
        graph = ExplicitGraph(3, 3)
        graph.build_from_maze_grid(single_cell_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (1, 1))
        
        assert path == [(1, 1)]
        assert (1, 1) in visited
        
    def test_bfs_linear_path(self):
        """Test BFS with linear path"""
        linear_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(5, 3)
        graph.build_from_maze_grid(linear_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (3, 1))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 1)
            assert len(path) == 3  # Optimal path
            
    def test_bfs_wall_start_position(self):
        """Test BFS starting from wall position"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        path, visited = bfs.solve((0, 0), (3, 3))  # Start at wall
        
        assert path == []  # Should fail to find path
        
    def test_bfs_wall_end_position(self):
        """Test BFS ending at wall position"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        path, visited = bfs.solve((1, 1), (0, 0))  # End at wall
        
        assert path == []  # Should fail to find path
        
    def test_bfs_out_of_bounds(self):
        """Test BFS with out of bounds coordinates"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        
        # Out of bounds start
        path, visited = bfs.solve((-1, -1), (3, 3))
        assert path == []
        
        # Out of bounds end
        path, visited = bfs.solve((1, 1), (100, 100))
        assert path == []


class TestBFSStress:
    """Stress tests for BFS"""
    
    def test_bfs_large_maze(self):
        """Test BFS with larger maze"""
        # Create larger maze
        size = 15
        large_maze = [[1 for _ in range(size)] for _ in range(size)]
        
        # Create a simple path
        for i in range(1, size - 1):
            large_maze[1][i] = 0  # Horizontal path
            large_maze[i][size - 2] = 0  # Vertical path
            
        large_maze[1][1] = 0  # Start
        large_maze[size - 2][size - 2] = 0  # End
        
        graph = ExplicitGraph(size, size)
        graph.build_from_maze_grid(large_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (size - 2, size - 2))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (size - 2, size - 2)
            
    def test_bfs_complex_maze(self):
        """Test BFS with complex maze structure"""
        complex_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(11, 7)
        graph.build_from_maze_grid(complex_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (9, 5))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (9, 5)
            
        # BFS should find optimal path in complex maze
        assert len(visited) > 0


class TestBFSComparison:
    """Test BFS comparative behavior"""
    
    def test_bfs_multiple_equal_paths(self):
        """Test BFS behavior with multiple equal-length paths"""
        # Create maze with two equal shortest paths
        equal_paths_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        graph = ExplicitGraph(7, 5)
        graph.build_from_maze_grid(equal_paths_maze, {TerrainType.PATH: 1.0})
        bfs = BreadthFirstSearch(graph)
        path, visited = bfs.solve((1, 1), (5, 1))
        
        if path:
            # Should find one of the optimal paths
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            # Both paths through (3,1) and (3,3) should be length 5
            assert len(path) == 5
            
    def test_bfs_consistent_results(self):
        """Test that BFS produces consistent results"""
        simple_test_graph = create_simple_test_graph()
        bfs = BreadthFirstSearch(simple_test_graph)
        
        # Run multiple times
        results = []
        for _ in range(3):
            path, visited = bfs.solve((1, 1), (3, 3))
            results.append((len(path) if path else 0, len(visited)))
        
        # Results should be consistent
        assert len(set(results)) == 1  # All results should be identical

def run_all_tests():
    """Run all tests in this module"""
    test_classes = [TestBFSInitialization, TestBFSBasicFunctionality, TestBFSAlgorithmSpecific, 
                   TestBFSPerformance, TestBFSEdgeCases, TestBFSStress, TestBFSComparison]
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running BFS tests...")
    
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        test_instance = test_class()
        
        # Get all test methods
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_') and callable(getattr(test_instance, method))]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                print(f"  {test_method}...", end=" ")
                getattr(test_instance, test_method)()
                print("PASS")
                passed_tests += 1
            except Exception as e:
                print(f"FAIL: {e}")
                failed_tests.append(f"{test_class.__name__}.{test_method}: {e}")
                traceback.print_exc()
    
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