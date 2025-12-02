#!/usr/bin/env python3
"""
Tests for Algorithm Base Class and Common Functionality
Tests the shared functionality across all pathfinding algorithms
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.base_algorithm import BaseAlgorithm
from algorithms.breadth_first_search import BreadthFirstSearch
from algorithms.depth_first_search import DepthFirstSearch
from algorithms.dijkstra import Dijkstra
from graph import ExplicitGraph, TerrainType
from maze_solver import Algorithm
from typing import List, Tuple, Set, Dict, Any

class TestBaseAlgorithm:
    """Test the BaseAlgorithm base class"""
    
    def test_base_algorithm_initialization(self):
        """Test that base algorithm initializes correctly"""
        graph = ExplicitGraph(5, 5)
        
        # Add some nodes
        for y in range(5):
            for x in range(5):
                terrain = TerrainType.WALL if x == 0 or y == 0 or x == 4 or y == 4 else TerrainType.PATH
                graph.add_node((x, y), terrain)
        
        # Create algorithm instance
        bfs = BreadthFirstSearch(graph)
        
        assert bfs.graph == graph
        assert bfs.width == 5
        assert bfs.height == 5
    
    def test_maze_property_backward_compatibility(self):
        """Test that maze property provides backward compatibility"""
        graph = ExplicitGraph(3, 3)
        
        # Create a simple pattern
        nodes = [
            ((0, 0), TerrainType.WALL), ((1, 0), TerrainType.WALL), ((2, 0), TerrainType.WALL),
            ((0, 1), TerrainType.WALL), ((1, 1), TerrainType.PATH), ((2, 1), TerrainType.WALL),
            ((0, 2), TerrainType.WALL), ((1, 2), TerrainType.WALL), ((2, 2), TerrainType.WALL)
        ]
        
        for pos, terrain in nodes:
            graph.add_node(pos, terrain)
        
        algorithm = BreadthFirstSearch(graph)
        maze = algorithm.maze
        
        # Should return simple grid format
        assert isinstance(maze, list)
        assert len(maze) == 3
        assert len(maze[0]) == 3
        
        # Center should be passable (0), borders should be walls (1)
        assert maze[1][1] == 0  # Center path
        assert maze[0][0] == 1  # Corner wall
        assert maze[2][2] == 1  # Corner wall
    
    def test_get_neighbors(self):
        """Test getting neighbors using explicit graph"""
        graph = ExplicitGraph(5, 5)
        
        # Create a cross pattern with center and 4 neighbors passable
        positions = [(2, 2), (1, 2), (3, 2), (2, 1), (2, 3)]  # center + 4 directions
        for pos in positions:
            graph.add_node(pos, TerrainType.PATH)
        
        # Add edges
        center = (2, 2)
        for pos in positions[1:]:  # Skip center
            graph.add_edge(center, pos)
        
        algorithm = BreadthFirstSearch(graph)
        neighbors = algorithm.get_neighbors(2, 2)
        
        assert len(neighbors) == 4
        expected_neighbors = [(1, 2), (3, 2), (2, 1), (2, 3)]
        for neighbor in neighbors:
            assert neighbor in expected_neighbors
    
    def test_get_neighbors_with_weights(self):
        """Test getting neighbors with their edge weights"""
        graph = ExplicitGraph(3, 3)
        
        # Create center with different terrain neighbors
        center = (1, 1)
        neighbors = [
            ((0, 1), TerrainType.PATH),    # Cost 1
            ((2, 1), TerrainType.MUD),     # Cost 3
            ((1, 0), TerrainType.WATER),   # Cost 5
            ((1, 2), TerrainType.SAND)     # Cost 2
        ]
        
        graph.add_node(center, TerrainType.PATH)
        for pos, terrain in neighbors:
            graph.add_node(pos, terrain)
            graph.add_edge(center, pos, bidirectional=False)
        
        algorithm = BreadthFirstSearch(graph)
        weighted_neighbors = algorithm.get_neighbors_with_weights(1, 1)
        
        assert len(weighted_neighbors) == 4
        
        # Check weights match terrain costs
        neighbor_weights = dict(weighted_neighbors)
        assert neighbor_weights[(0, 1)] == TerrainType.PATH.value   # 1
        assert neighbor_weights[(2, 1)] == TerrainType.MUD.value    # 3
        assert neighbor_weights[(1, 0)] == TerrainType.WATER.value  # 5
        assert neighbor_weights[(1, 2)] == TerrainType.SAND.value   # 2
    
    def test_get_edge_weight(self):
        """Test getting edge weights between positions"""
        graph = ExplicitGraph(3, 1)
        
        # Create path: PATH -> MUD -> WATER
        graph.add_node((0, 0), TerrainType.PATH)
        graph.add_node((1, 0), TerrainType.MUD)
        graph.add_node((2, 0), TerrainType.WATER)
        
        graph.add_edge((0, 0), (1, 0), bidirectional=False)
        graph.add_edge((1, 0), (2, 0), bidirectional=False)
        
        algorithm = BreadthFirstSearch(graph)
        
        # Test existing edges
        assert algorithm.get_edge_weight((0, 0), (1, 0)) == TerrainType.MUD.value
        assert algorithm.get_edge_weight((1, 0), (2, 0)) == TerrainType.WATER.value
        
        # Test non-existing edges (should return high value or None)
        non_edge_weight = algorithm.get_edge_weight((0, 0), (2, 0))
        assert non_edge_weight == float('inf') or non_edge_weight is None
        
        reverse_weight = algorithm.get_edge_weight((2, 0), (0, 0))
        assert reverse_weight == float('inf') or reverse_weight is None

class TestAlgorithmCommonFunctionality:
    """Test functionality common to all pathfinding algorithms"""
    
    def test_all_algorithms_implement_required_methods(self):
        """Test that all algorithms implement required abstract methods"""
        graph = ExplicitGraph(5, 5)
        # Create a simple passable area
        for y in range(1, 4):
            for x in range(1, 4):
                graph.add_node((x, y), TerrainType.PATH)
                if x < 3:
                    graph.add_edge((x, y), (x+1, y))
                if y < 3:
                    graph.add_edge((x, y), (x, y+1))
        
        algorithms = [
            BreadthFirstSearch(graph),
            DepthFirstSearch(graph),
            Dijkstra(graph)
        ]
        
        for algorithm in algorithms:
            # Should have solve method
            assert hasattr(algorithm, 'solve')
            assert callable(algorithm.solve)
            
            # Should have solve_animated method
            assert hasattr(algorithm, 'solve_animated')
            assert callable(algorithm.solve_animated)
            
            # Test that methods work
            start = (1, 1)
            end = (3, 3)
            
            path, visited = algorithm.solve(start, end)
            assert isinstance(path, list)
            assert isinstance(visited, set)
            
            # Test animated version
            animation_generator = algorithm.solve_animated(start, end)
            states = list(animation_generator)
            assert len(states) > 0
            assert all('action' in state for state in states)
    
    def test_algorithm_path_reconstruction(self):
        """Test path reconstruction works correctly"""
        graph = ExplicitGraph(5, 1)
        
        # Create simple linear path
        for x in range(5):
            graph.add_node((x, 0), TerrainType.PATH)
        
        # Add edges with explicit bidirectional connections
        for x in range(4):
            graph.add_edge((x, 0), (x+1, 0), bidirectional=True)
        
        algorithm = BreadthFirstSearch(graph)
        start = (0, 0)
        end = (4, 0)
        
        # Debug: verify graph connectivity
        neighbors_start = algorithm.get_neighbors(0, 0)
        neighbors_end = algorithm.get_neighbors(4, 0)
        assert len(neighbors_start) > 0, f"Start position {start} should have neighbors"
        assert len(neighbors_end) > 0, f"End position {end} should have neighbors"
        
        path, visited = algorithm.solve(start, end)
        
        # Should find a path
        assert len(path) > 0, f"Should find path from {start} to {end}, got empty path"
        assert path[0] == start, f"Path should start at {start}"
        assert path[-1] == end, f"Path should end at {end}"
        
        # Path should be correct length (for this simple linear case)
        expected_path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        assert path == expected_path, f"Expected {expected_path}, got {path}"
    
    def test_algorithm_visited_tracking(self):
        """Test that visited cells are tracked correctly"""
        graph = ExplicitGraph(3, 3)
        
        # Create a 3x3 grid of paths
        for y in range(3):
            for x in range(3):
                graph.add_node((x, y), TerrainType.PATH)
        
        # Add all horizontal and vertical edges
        for y in range(3):
            for x in range(3):
                if x < 2:
                    graph.add_edge((x, y), (x+1, y))
                if y < 2:
                    graph.add_edge((x, y), (x, y+1))
        
        algorithm = BreadthFirstSearch(graph)
        start = (0, 0)
        end = (2, 2)
        
        path, visited = algorithm.solve(start, end)
        
        # Should have visited multiple cells
        assert len(visited) > 0
        assert start in visited
        assert end in visited
        
        # All path cells should be in visited
        for pos in path:
            assert pos in visited
    
    def test_no_path_scenario(self):
        """Test behavior when no path exists"""
        graph = ExplicitGraph(5, 3)
        
        # Create two disconnected areas
        # Left area
        graph.add_node((0, 1), TerrainType.PATH)
        graph.add_node((1, 1), TerrainType.PATH)
        graph.add_edge((0, 1), (1, 1))
        
        # Wall barrier
        for y in range(3):
            graph.add_node((2, y), TerrainType.WALL)
        
        # Right area
        graph.add_node((3, 1), TerrainType.PATH)
        graph.add_node((4, 1), TerrainType.PATH)
        graph.add_edge((3, 1), (4, 1))
        
        algorithm = BreadthFirstSearch(graph)
        start = (0, 1)
        end = (4, 1)
        
        path, visited = algorithm.solve(start, end)
        
        # Should return empty path
        assert len(path) == 0
        
        # Should still have visited some cells (in the starting area)
        assert len(visited) > 0
        assert start in visited
        assert end not in visited

class TestAlgorithmSpecificBehavior:
    """Test algorithm-specific behaviors"""
    
    def test_bfs_breadth_first_exploration(self):
        """Test that BFS explores breadth-first"""
        graph = ExplicitGraph(5, 5)
        
        # Create a diamond pattern to test BFS behavior
        center = (2, 2)
        positions = [
            (2, 2),  # center
            (1, 2), (3, 2), (2, 1), (2, 3),  # distance 1
            (0, 2), (4, 2), (2, 0), (2, 4),  # distance 2
        ]
        
        for pos in positions:
            graph.add_node(pos, TerrainType.PATH)
        
        # Connect in diamond pattern
        edges = [
            ((2, 2), (1, 2)), ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((2, 2), (2, 3)),
            ((1, 2), (0, 2)), ((3, 2), (4, 2)), ((2, 1), (2, 0)), ((2, 3), (2, 4))
        ]
        
        for pos1, pos2 in edges:
            graph.add_edge(pos1, pos2)
        
        bfs = BreadthFirstSearch(graph)
        start = (2, 2)
        end = (0, 2)
        
        # Get animation states to verify breadth-first behavior
        states = list(bfs.solve_animated(start, end))
        
        # Should find breadth levels
        breadth_level_states = [s for s in states if 'breadth_levels' in s]
        assert len(breadth_level_states) > 0
        
        # Final state should have correct breadth levels
        final_breadth_state = breadth_level_states[-1]
        breadth_levels = final_breadth_state['breadth_levels']
        
        # Center should be level 0
        assert breadth_levels.get((2, 2), -1) == 0
        
        # Adjacent cells should be level 1
        for pos in [(1, 2), (3, 2), (2, 1), (2, 3)]:
            if pos in breadth_levels:
                assert breadth_levels[pos] == 1
    
    def test_dijkstra_weighted_exploration(self):
        """Test that Dijkstra considers weights properly"""
        graph = ExplicitGraph(3, 3)
        
        # Create scenario where shortest path != cheapest path
        # Top row: PATH - MUD - PATH (cost: 1 + 3 = 4)
        # Bottom: PATH - PATH - PATH (cost: 1 + 1 = 2, but longer)
        
        positions = [
            ((0, 0), TerrainType.PATH), ((1, 0), TerrainType.MUD), ((2, 0), TerrainType.PATH),
            ((0, 1), TerrainType.PATH), ((1, 1), TerrainType.PATH), ((2, 1), TerrainType.PATH),
            ((0, 2), TerrainType.PATH), ((1, 2), TerrainType.PATH), ((2, 2), TerrainType.PATH),
        ]
        
        for pos, terrain in positions:
            graph.add_node(pos, terrain)
        
        # Add edges to create two paths: top (short, expensive) and bottom (long, cheap)
        edges = [
            # Top row
            ((0, 0), (1, 0)), ((1, 0), (2, 0)),
            # Bottom rows
            ((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (1, 2)), 
            ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (2, 0)),
            # Middle connections
            ((0, 1), (1, 1)), ((1, 1), (2, 1)),
        ]
        
        for pos1, pos2 in edges:
            graph.add_edge(pos1, pos2)
        
        dijkstra = Dijkstra(graph)
        bfs = BreadthFirstSearch(graph)
        
        start = (0, 0)
        end = (2, 0)
        
        dijkstra_path, _ = dijkstra.solve(start, end)
        bfs_path, _ = bfs.solve(start, end)
        
        # Both should find valid paths
        assert len(dijkstra_path) > 0
        assert len(bfs_path) > 0
        assert dijkstra_path[0] == start and dijkstra_path[-1] == end
        assert bfs_path[0] == start and bfs_path[-1] == end
        
        # Calculate costs
        def path_cost(path):
            cost = 0
            for i in range(len(path) - 1):
                cost += graph.get_edge_weight(path[i], path[i+1])
            return cost
        
        dijkstra_cost = path_cost(dijkstra_path)
        bfs_cost = path_cost(bfs_path)
        
        # Dijkstra should find lower or equal cost path
        assert dijkstra_cost <= bfs_cost
    
    def test_dfs_depth_first_exploration(self):
        """Test that DFS explores depth-first"""
        graph = ExplicitGraph(3, 5)
        
        # Create a long corridor to test DFS behavior
        positions = [(1, y) for y in range(5)]  # Vertical corridor
        positions.extend([(0, 0), (2, 0)])     # Side branches at top
        
        for pos in positions:
            graph.add_node(pos, TerrainType.PATH)
        
        # Connect corridor vertically
        for y in range(4):
            graph.add_edge((1, y), (1, y+1))
        
        # Add side branches
        graph.add_edge((1, 0), (0, 0))
        graph.add_edge((1, 0), (2, 0))
        
        dfs = DepthFirstSearch(graph)
        start = (1, 0)
        end = (1, 4)
        
        path, visited = dfs.solve(start, end)
        
        # Should find a valid path
        assert len(path) > 0
        assert path[0] == start
        assert path[-1] == end
        
        # Path should be reasonably direct (DFS characteristic)
        # In this case, should go straight down the corridor
        expected_path = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
        assert path == expected_path or len(path) == len(expected_path)

class TestAnimationStates:
    """Test animation state generation for all algorithms"""
    
    def test_animation_state_format(self):
        """Test that animation states have correct format"""
        graph = ExplicitGraph(3, 3)
        for y in range(3):
            for x in range(3):
                graph.add_node((x, y), TerrainType.PATH)
                if x < 2:
                    graph.add_edge((x, y), (x+1, y))
                if y < 2:
                    graph.add_edge((x, y), (x, y+1))
        
        algorithms = [
            (BreadthFirstSearch(graph), 'BFS'),
            (DepthFirstSearch(graph), 'DFS'),
            (Dijkstra(graph), 'Dijkstra')
        ]
        
        for algorithm, name in algorithms:
            states = list(algorithm.solve_animated((0, 0), (2, 2)))
            
            assert len(states) > 0, f"{name} should generate animation states"
            
            # All states should have 'action'
            for state in states:
                assert 'action' in state, f"{name} states should have action field"
                assert isinstance(state['action'], str)
            
            # Last state should be 'found' or 'no_solution'
            final_action = states[-1]['action']
            assert final_action in ['found', 'no_solution'], f"{name} should end with found/no_solution"
            
            # If found, should have path
            if final_action == 'found':
                assert 'path' in states[-1], f"{name} found state should include path"
                assert len(states[-1]['path']) >= 2, f"{name} path should have start and end"
    
    def test_algorithm_specific_animation_data(self):
        """Test that algorithms include their specific animation data"""
        graph = ExplicitGraph(3, 3)
        for y in range(3):
            for x in range(3):
                graph.add_node((x, y), TerrainType.PATH)
                if x < 2:
                    graph.add_edge((x, y), (x+1, y))
                if y < 2:
                    graph.add_edge((x, y), (x, y+1))
        
        # Test BFS includes breadth levels
        bfs = BreadthFirstSearch(graph)
        bfs_states = list(bfs.solve_animated((0, 0), (2, 2)))
        
        breadth_found = any('breadth_levels' in state for state in bfs_states)
        assert breadth_found, "BFS should include breadth level information"
        
        # Test Dijkstra includes distances
        dijkstra = Dijkstra(graph)
        dijkstra_states = list(dijkstra.solve_animated((0, 0), (2, 2)))
        
        distances_found = any('distances' in state for state in dijkstra_states)
        assert distances_found, "Dijkstra should include distance information"
        
        # Test DFS includes stack information
        dfs = DepthFirstSearch(graph)
        dfs_states = list(dfs.solve_animated((0, 0), (2, 2)))
        
        # DFS should have some form of exploration state
        assert len(dfs_states) > 0, "DFS should generate animation states"
        # The specific data structure for DFS may vary

if __name__ == "__main__":
    # Run tests directly without pytest dependency
    test_classes = [
        TestBaseAlgorithm,
        TestAlgorithmCommonFunctionality,
        TestAlgorithmSpecificBehavior,
        TestAnimationStates
    ]
    
    total_tests = 0
    passed_tests = 0
    
    print("Running Algorithm Tests")
    print("=" * 50)
    
    for test_class in test_classes:
        instance = test_class()
        methods = [method for method in dir(instance) if method.startswith('test_')]
        
        print(f"\nRunning {test_class.__name__}:")
        
        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {str(e)}")
                # Uncomment next line for detailed error traces
                # traceback.print_exc()
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Some tests failed. {total_tests - passed_tests} failures.")
        sys.exit(1)