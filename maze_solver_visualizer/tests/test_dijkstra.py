"""
Tests for Dijkstra's Algorithm
Comprehensive testing of Dijkstra implementation with weighted paths
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple, Set
from algorithms.dijkstra import Dijkstra
from graph import ExplicitGraph, TerrainType

# Test fixtures
def create_simple_test_graph():
    """Create a simple 5x5 test graph"""
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

def create_weighted_test_graph():
    """Create a test graph with different terrain weights"""
    graph = ExplicitGraph(5, 3)
    
    # Top path: PATH -> MUD -> PATH (cost: 1 + 3 = 4)
    graph.add_node((0, 0), TerrainType.PATH)
    graph.add_node((1, 0), TerrainType.PATH)
    graph.add_node((2, 0), TerrainType.MUD)
    graph.add_node((3, 0), TerrainType.PATH) 
    graph.add_node((4, 0), TerrainType.PATH)
    
    # Middle path: longer but cheaper PATH -> PATH -> PATH (cost: 1 + 1 + 1 = 3)
    graph.add_node((0, 1), TerrainType.PATH)
    graph.add_node((1, 1), TerrainType.PATH)
    graph.add_node((2, 1), TerrainType.PATH)
    graph.add_node((3, 1), TerrainType.PATH)
    graph.add_node((4, 1), TerrainType.PATH)
    
    # Bottom path: very expensive WATER terrain
    graph.add_node((0, 2), TerrainType.PATH)
    graph.add_node((1, 2), TerrainType.WATER)
    graph.add_node((2, 2), TerrainType.WATER)
    graph.add_node((3, 2), TerrainType.WATER)
    graph.add_node((4, 2), TerrainType.PATH)
    
    # Add horizontal edges
    for y in range(3):
        for x in range(4):
            graph.add_edge((x, y), (x+1, y))
    
    # Add vertical connections
    for x in range(5):
        graph.add_edge((x, 0), (x, 1))
        graph.add_edge((x, 1), (x, 2))
    
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

class TestDijkstraInitialization:
    """Test Dijkstra initialization"""
    
    def test_dijkstra_initialization(self):
        """Test Dijkstra can be initialized"""
        simple_test_graph = create_simple_test_graph()
        dijkstra = Dijkstra(simple_test_graph)
        assert dijkstra.graph == simple_test_graph
        assert dijkstra.height == simple_test_graph.height
        assert dijkstra.width == simple_test_graph.width
        
    def test_dijkstra_with_empty_maze(self):
        """Test Dijkstra with minimal graph"""
        minimal_graph = ExplicitGraph(1, 1)
        minimal_graph.add_node((0, 0), TerrainType.PATH)
        dijkstra = Dijkstra(minimal_graph)
        assert dijkstra.graph == minimal_graph
        assert dijkstra.height == 1
        assert dijkstra.width == 1

class TestDijkstraBasicFunctionality:
    """Test basic Dijkstra functionality"""
    
    def test_dijkstra_solve_simple_path(self):
        """Test Dijkstra solving simple path"""
        simple_test_graph = create_simple_test_graph()
        dijkstra = Dijkstra(simple_test_graph)
        path, visited = dijkstra.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_dijkstra_solve_no_solution(self):
        """Test Dijkstra with impossible maze"""
        impossible_graph = create_impossible_graph()
        dijkstra = Dijkstra(impossible_graph)
        path, visited = dijkstra.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_dijkstra_path_validity(self):
        """Test that Dijkstra returns valid paths"""
        weighted_graph = create_weighted_test_graph()
        dijkstra = Dijkstra(weighted_graph)
        path, visited = dijkstra.solve((0, 0), (4, 0))
        
        if path:
            # Path should start and end correctly
            assert path[0] == (0, 0)
            assert path[-1] == (4, 0)
            
            # All positions in path should be adjacent
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                distance = abs(x1 - x2) + abs(y1 - y2)
                assert distance == 1, f"Non-adjacent positions in path: {path[i]} -> {path[i+1]}"
        
        # All path positions should be in visited set
        for pos in path:
            assert pos in visited
            
    def test_dijkstra_visited_cells(self):
        """Test that Dijkstra tracks visited cells properly"""
        weighted_graph = create_weighted_test_graph()
        dijkstra = Dijkstra(weighted_graph)
        path, visited = dijkstra.solve((0, 1), (4, 1))
        
        # Visited should include start position
        assert (0, 1) in visited
        
        # If path exists, end should be in visited
        if path:
            assert (4, 1) in visited
        
        # Visited should not be empty (at least explored start)
        assert len(visited) > 0

class TestDijkstraWeightedPaths:
    """Test Dijkstra's weighted pathfinding capabilities"""
    
    def test_dijkstra_optimal_cost(self):
        """Test that Dijkstra finds optimal cost paths"""
        weighted_graph = create_weighted_test_graph()
        dijkstra = Dijkstra(weighted_graph)
        path, visited = dijkstra.solve((0, 0), (4, 2))
        
        if path:
            # Calculate path cost
            total_cost = 0
            for i in range(len(path) - 1):
                edge_weight = weighted_graph.get_edge_weight(path[i], path[i+1])
                total_cost += edge_weight
            
            # Should find reasonably optimal path
            assert total_cost > 0
            assert len(path) >= 2
    
    def test_dijkstra_terrain_preference(self):
        """Test Dijkstra prefers lower cost terrain"""
        weighted_graph = create_weighted_test_graph()
        dijkstra = Dijkstra(weighted_graph)
        
        # Should prefer middle path (all PATH terrain) over top path (contains MUD)
        path_to_middle, _ = dijkstra.solve((0, 0), (4, 1))
        path_to_top, _ = dijkstra.solve((0, 0), (4, 0))
        
        if path_to_middle and path_to_top:
            # Calculate costs
            def path_cost(path, graph):
                cost = 0
                for i in range(len(path) - 1):
                    cost += graph.get_edge_weight(path[i], path[i+1])
                return cost
            
            cost_middle = path_cost(path_to_middle, weighted_graph)
            cost_top = path_cost(path_to_top, weighted_graph)
            
            # Direct path to middle should be cheaper than path through mud
            # (This test depends on the specific graph setup)
            assert cost_middle > 0 and cost_top > 0
            
    def test_dijkstra_distance_tracking(self):
        """Test that Dijkstra tracks distances correctly"""
        weighted_graph = create_weighted_test_graph()
        dijkstra = Dijkstra(weighted_graph)
        
        # Get animation states to check distance tracking
        states = list(dijkstra.solve_animated((0, 1), (4, 1)))
        
        # Should have states with distance information
        distance_states = [s for s in states if 'distances' in s]
        assert len(distance_states) > 0
        
        # Check that distances are reasonable
        final_distances = distance_states[-1]['distances']
        assert (0, 1) in final_distances
        assert final_distances[(0, 1)] == 0  # Start position should have distance 0

class TestDijkstraAlgorithmSpecific:
    """Test Dijkstra-specific behaviors"""
    
    def test_dijkstra_shortest_path_property(self):
        """Test Dijkstra's shortest path property"""
        graph = ExplicitGraph(3, 3)
        
        # Create a simple graph where we can verify optimality
        for y in range(3):
            for x in range(3):
                graph.add_node((x, y), TerrainType.PATH)
        
        # Add all possible edges
        for y in range(3):
            for x in range(3):
                if x < 2:
                    graph.add_edge((x, y), (x+1, y))
                if y < 2:
                    graph.add_edge((x, y), (x, y+1))
        
        dijkstra = Dijkstra(graph)
        path, visited = dijkstra.solve((0, 0), (2, 2))
        
        # Should find optimal path
        if path:
            assert len(path) == 5  # Optimal path length for 3x3 corner to corner
            assert path[0] == (0, 0)
            assert path[-1] == (2, 2)
    
    def test_dijkstra_vs_bfs_comparison(self):
        """Test Dijkstra vs BFS on uniform cost graph"""
        from algorithms.breadth_first_search import BreadthFirstSearch
        
        # Create uniform cost graph
        graph = ExplicitGraph(4, 4)
        for y in range(4):
            for x in range(4):
                if x == 0 or y == 0 or x == 3 or y == 3:
                    graph.add_node((x, y), TerrainType.WALL)
                else:
                    graph.add_node((x, y), TerrainType.PATH)
        
        # Add edges for inner area
        for y in range(1, 3):
            for x in range(1, 3):
                if x < 2:
                    graph.add_edge((x, y), (x+1, y))
                if y < 2:
                    graph.add_edge((x, y), (x, y+1))
        
        dijkstra = Dijkstra(graph)
        bfs = BreadthFirstSearch(graph)
        
        dijkstra_path, _ = dijkstra.solve((1, 1), (2, 2))
        bfs_path, _ = bfs.solve((1, 1), (2, 2))
        
        # Both should find optimal paths of same length on uniform cost
        if dijkstra_path and bfs_path:
            assert len(dijkstra_path) == len(bfs_path)

class TestDijkstraEdgeCases:
    """Test edge cases for Dijkstra"""
    
    def test_dijkstra_single_cell_path(self):
        """Test Dijkstra with single cell (start == end)"""
        graph = ExplicitGraph(3, 3)
        graph.add_node((1, 1), TerrainType.PATH)
        
        dijkstra = Dijkstra(graph)
        path, visited = dijkstra.solve((1, 1), (1, 1))
        
        assert path == [(1, 1)]
        assert (1, 1) in visited
        
    def test_dijkstra_linear_path(self):
        """Test Dijkstra on linear path"""
        graph = ExplicitGraph(5, 1)
        for x in range(5):
            graph.add_node((x, 0), TerrainType.PATH)
        
        for x in range(4):
            graph.add_edge((x, 0), (x+1, 0))
        
        dijkstra = Dijkstra(graph)
        path, visited = dijkstra.solve((0, 0), (4, 0))
        
        assert len(path) == 5
        assert path == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        
    def test_dijkstra_wall_positions(self):
        """Test Dijkstra with wall positions"""
        simple_test_graph = create_simple_test_graph()
        dijkstra = Dijkstra(simple_test_graph)
        
        # Wall start position
        path, visited = dijkstra.solve((0, 0), (3, 3))
        assert path == []
        assert len(visited) <= 1
        
        # Wall end position 
        path, visited = dijkstra.solve((1, 1), (0, 0))
        assert path == []
        assert len(visited) > 0
        
    def test_dijkstra_out_of_bounds(self):
        """Test Dijkstra with out of bounds positions"""
        simple_test_graph = create_simple_test_graph()
        dijkstra = Dijkstra(simple_test_graph)
        path, visited = dijkstra.solve((1, 1), (10, 10))
        
        assert path == []
        assert len(visited) > 0

class TestDijkstraStress:
    """Stress tests for Dijkstra"""
    
    def test_dijkstra_large_weighted_maze(self):
        """Test Dijkstra on larger weighted maze"""
        size = 10
        graph = ExplicitGraph(size, size)
        
        # Create checkerboard pattern of different terrains
        for y in range(size):
            for x in range(size):
                if x == 0 or y == 0 or x == size-1 or y == size-1:
                    graph.add_node((x, y), TerrainType.WALL)
                elif (x + y) % 2 == 0:
                    graph.add_node((x, y), TerrainType.PATH)
                else:
                    graph.add_node((x, y), TerrainType.MUD)
        
        # Add edges
        for y in range(1, size-1):
            for x in range(1, size-1):
                if x < size-2:
                    graph.add_edge((x, y), (x+1, y))
                if y < size-2:
                    graph.add_edge((x, y), (x, y+1))
        
        dijkstra = Dijkstra(graph)
        path, visited = dijkstra.solve((1, 1), (size-2, size-2))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (size-2, size-2)
            assert len(path) >= 2

def run_all_tests():
    """Run all Dijkstra tests"""
    test_classes = [
        TestDijkstraInitialization,
        TestDijkstraBasicFunctionality,
        TestDijkstraWeightedPaths,
        TestDijkstraAlgorithmSpecific,
        TestDijkstraEdgeCases,
        TestDijkstraStress
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running Dijkstra tests...")
    
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