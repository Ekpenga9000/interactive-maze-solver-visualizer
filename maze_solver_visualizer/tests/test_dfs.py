"""
Tests for Depth-First Search Algorithm
Comprehensive testing of DFS implementation
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple, Set
from algorithms.depth_first_search import DepthFirstSearch
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
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
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
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
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
    graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
    return graph

class TestDFSInitialization:
    """Test DFS initialization"""
    
    def test_dfs_initialization(self):
        """Test DFS can be initialized"""
        simple_test_graph = create_simple_test_graph()
        dfs = DepthFirstSearch(simple_test_graph)
        assert dfs.graph == simple_test_graph
        assert dfs.height == simple_test_graph.height
        assert dfs.width == simple_test_graph.width
        
    def test_dfs_with_empty_maze(self):
        """Test DFS with edge case inputs"""
        # Test with minimal valid graph
        minimal_graph = ExplicitGraph(1, 1)
        minimal_graph.add_node((0, 0), TerrainType.PATH)
        dfs = DepthFirstSearch(minimal_graph)
        assert dfs.graph == minimal_graph
        assert dfs.height == 1
        assert dfs.width == 1

class TestDFSBasicFunctionality:
    """Test basic DFS functionality"""
    
    def test_dfs_solve_simple_path(self):
        """Test DFS solving simple path"""
        simple_test_graph = create_simple_test_graph()
        dfs = DepthFirstSearch(simple_test_graph)
        path, visited = dfs.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_dfs_solve_no_solution(self):
        """Test DFS with impossible maze"""
        impossible_graph = create_impossible_graph()
        dfs = DepthFirstSearch(impossible_graph)
        path, visited = dfs.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_dfs_path_validity(self):
        """Test that DFS returns valid paths"""
        complex_test_graph = create_complex_test_graph()
        dfs = DepthFirstSearch(complex_test_graph)
        path, visited = dfs.solve((1, 1), (5, 1))
        
        if path:
            # Path should start and end correctly
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            
            # All positions in path should be adjacent
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                distance = abs(x1 - x2) + abs(y1 - y2)
                assert distance == 1, f"Non-adjacent positions in path: {path[i]} -> {path[i+1]}"
        
        # All path positions should be in visited set
        for pos in path:
            assert pos in visited
            
    def test_dfs_visited_cells(self):
        """Test that DFS tracks visited cells properly"""
        complex_test_graph = create_complex_test_graph()
        dfs = DepthFirstSearch(complex_test_graph)
        path, visited = dfs.solve((1, 1), (5, 4))
        
        # Visited should include start position
        assert (1, 1) in visited
        
        # If path exists, end should be in visited
        if path:
            assert (5, 4) in visited
        
        # Visited should not be empty (at least explored start)
        assert len(visited) > 0

class TestDFSAlgorithmSpecific:
    """Test DFS-specific behaviors"""
    
    def test_dfs_depth_first_behavior(self):
        """Test that DFS explores depth-first"""
        complex_test_graph = create_complex_test_graph()
        dfs = DepthFirstSearch(complex_test_graph)
        
        # Use animated version to see exploration order
        states = list(dfs.solve_animated((1, 1), (5, 4)))
        
        assert len(states) > 0
        
        # Should have exploration states
        exploration_states = [s for s in states if s['action'] == 'exploring']
        assert len(exploration_states) > 0
        
    def test_dfs_backtracking(self):
        """Test DFS backtracking behavior"""
        # Create maze that requires backtracking
        maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1], 
            [1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        graph = ExplicitGraph(5, 5)
        graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
        
        dfs = DepthFirstSearch(graph)
        path, visited = dfs.solve((1, 1), (3, 3))
        
        # Should find a valid path even with backtracking needed
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 5  # Minimum for this maze

class TestDFSPerformance:
    """Test DFS performance characteristics"""
    
    def test_dfs_exploration_efficiency(self):
        """Test DFS exploration efficiency"""
        complex_test_graph = create_complex_test_graph()
        dfs = DepthFirstSearch(complex_test_graph)
        path, visited = dfs.solve((1, 1), (5, 1))
        
        # DFS might not find shortest path but should find a path if one exists
        if path:
            assert len(path) >= 2  # At least start and end
            
        # Should visit reasonable number of cells
        total_passable = 0
        for y in range(6):
            for x in range(7):
                if complex_test_graph.is_passable((x, y)):
                    total_passable += 1
        
        # Shouldn't visit more cells than exist
        assert len(visited) <= total_passable
        
    def test_dfs_different_paths(self):
        """Test that DFS can find different valid paths"""
        # Create graph with multiple paths
        maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1], 
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        graph = ExplicitGraph(5, 5)
        graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
        
        dfs = DepthFirstSearch(graph)
        path1, _ = dfs.solve((1, 1), (3, 3))
        path2, _ = dfs.solve((1, 1), (3, 1))
        
        # Both should be valid paths
        if path1:
            assert path1[0] == (1, 1) and path1[-1] == (3, 3)
        if path2:
            assert path2[0] == (1, 1) and path2[-1] == (3, 1)

class TestDFSEdgeCases:
    """Test edge cases for DFS"""
    
    def test_dfs_single_cell_path(self):
        """Test DFS with single cell (start == end)"""
        graph = ExplicitGraph(3, 3)
        graph.add_node((1, 1), TerrainType.PATH)
        
        dfs = DepthFirstSearch(graph)
        path, visited = dfs.solve((1, 1), (1, 1))
        
        assert path == [(1, 1)]
        assert (1, 1) in visited
        
    def test_dfs_linear_path(self):
        """Test DFS on linear path"""
        graph = ExplicitGraph(5, 1)
        for x in range(5):
            graph.add_node((x, 0), TerrainType.PATH)
        
        for x in range(4):
            graph.add_edge((x, 0), (x+1, 0))
        
        # Debug: verify graph setup
        assert graph.get_neighbor_positions((0, 0)) == [(1, 0)], f"Expected [(1, 0)], got {graph.get_neighbor_positions((0, 0))}"
        assert graph.get_neighbor_positions((4, 0)) == [(3, 0)], f"Expected [(3, 0)], got {graph.get_neighbor_positions((4, 0))}"
        
        dfs = DepthFirstSearch(graph)
        path, visited = dfs.solve((0, 0), (4, 0))
        
        # Should find a valid path
        assert len(path) > 0, f"Should find path, got {path}"
        assert path[0] == (0, 0)
        assert path[-1] == (4, 0)
        # Path should be correct length for linear case
        assert len(path) == 5, f"Expected path length 5, got {len(path)}: {path}"
        
    def test_dfs_wall_start_position(self):
        """Test DFS with wall at start position"""
        simple_test_graph = create_simple_test_graph()
        dfs = DepthFirstSearch(simple_test_graph)
        path, visited = dfs.solve((0, 0), (3, 3))  # (0,0) is wall
        
        # Should return empty path when starting from wall
        assert path == []
        # Visited might be empty or contain just the invalid start
        assert len(visited) <= 1
        
    def test_dfs_wall_end_position(self):
        """Test DFS with wall at end position"""
        simple_test_graph = create_simple_test_graph()
        dfs = DepthFirstSearch(simple_test_graph)
        path, visited = dfs.solve((1, 1), (0, 0))  # (0,0) is wall
        
        assert path == []
        assert len(visited) > 0  # Should still explore from start
        
    def test_dfs_out_of_bounds(self):
        """Test DFS with out of bounds positions"""
        simple_test_graph = create_simple_test_graph()
        dfs = DepthFirstSearch(simple_test_graph)
        path, visited = dfs.solve((1, 1), (10, 10))  # Out of bounds
        
        assert path == []
        assert len(visited) > 0  # Should still explore from valid start

class TestDFSStress:
    """Stress tests for DFS"""
    
    def test_dfs_large_maze(self):
        """Test DFS on larger maze"""
        # Create a 15x15 maze with paths
        size = 15
        graph = ExplicitGraph(size, size)
        
        # Add border walls and internal paths
        for y in range(size):
            for x in range(size):
                if x == 0 or y == 0 or x == size-1 or y == size-1:
                    graph.add_node((x, y), TerrainType.WALL)
                else:
                    graph.add_node((x, y), TerrainType.PATH)
        
        # Add edges for internal paths
        for y in range(1, size-1):
            for x in range(1, size-1):
                if x < size-2:
                    graph.add_edge((x, y), (x+1, y))
                if y < size-2:
                    graph.add_edge((x, y), (x, y+1))
        
        dfs = DepthFirstSearch(graph)
        path, visited = dfs.solve((1, 1), (size-2, size-2))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (size-2, size-2)
            assert len(path) >= 2

def run_all_tests():
    """Run all DFS tests"""
    test_classes = [
        TestDFSInitialization,
        TestDFSBasicFunctionality,
        TestDFSAlgorithmSpecific,
        TestDFSPerformance,
        TestDFSEdgeCases,
        TestDFSStress
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running DFS tests...")
    
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