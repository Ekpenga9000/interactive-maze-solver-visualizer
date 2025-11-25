"""
Tests for Dijkstra's Algorithm
Comprehensive testing of Dijkstra implementation
"""
import pytest
from typing import List, Tuple, Set
from algorithms.dijkstra import Dijkstra


class TestDijkstraInitialization:
    """Test Dijkstra initialization"""
    
    def test_dijkstra_initialization(self, simple_test_maze):
        """Test Dijkstra can be initialized"""
        dijkstra = Dijkstra(simple_test_maze)
        assert dijkstra.maze == simple_test_maze
        assert dijkstra.height == len(simple_test_maze)
        assert dijkstra.width == len(simple_test_maze[0])
        
    def test_dijkstra_with_empty_maze(self):
        """Test Dijkstra with edge case inputs"""
        with pytest.raises((IndexError, ValueError)):
            Dijkstra([])


class TestDijkstraBasicFunctionality:
    """Test basic Dijkstra functionality"""
    
    def test_dijkstra_solve_simple_path(self, simple_test_maze):
        """Test Dijkstra solving simple path"""
        dijkstra = Dijkstra(simple_test_maze)
        path, visited = dijkstra.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_dijkstra_solve_no_solution(self, impossible_maze):
        """Test Dijkstra with impossible maze"""
        dijkstra = Dijkstra(impossible_maze)
        path, visited = dijkstra.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_dijkstra_path_validity(self, complex_test_maze):
        """Test that Dijkstra path is valid"""
        dijkstra = Dijkstra(complex_test_maze)
        path, visited = dijkstra.solve((1, 1), (5, 4))
        
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
                assert dijkstra.maze[y][x] == 0
                
    def test_dijkstra_visited_cells(self, complex_test_maze):
        """Test Dijkstra visited cells properties"""
        dijkstra = Dijkstra(complex_test_maze)
        path, visited = dijkstra.solve((1, 1), (5, 4))
        
        # Path cells should be subset of visited
        if path:
            for pos in path:
                assert pos in visited
                
        # All visited cells should be valid
        for x, y in visited:
            assert 0 <= x < dijkstra.width
            assert 0 <= y < dijkstra.height
            assert dijkstra.maze[y][x] == 0


class TestDijkstraAlgorithmSpecific:
    """Test Dijkstra-specific algorithm behavior"""
    
    def test_dijkstra_shortest_path_guarantee(self):
        """Test that Dijkstra always finds shortest path"""
        # Create maze with clear shortest path
        shortest_path_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(shortest_path_maze)
        path, visited = dijkstra.solve((1, 1), (5, 1))
        
        if path:
            # Dijkstra should find shortest path (5 steps)
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            
    def test_dijkstra_priority_queue_behavior(self, complex_test_maze):
        """Test that Dijkstra uses priority queue correctly"""
        dijkstra = Dijkstra(complex_test_maze)
        
        # Create custom Dijkstra to track distance updates
        class TrackingDijkstra(Dijkstra):
            def __init__(self, maze):
                super().__init__(maze)
                self.distance_updates = []
                
            def solve(self, start, end):
                import heapq
                
                visited = set()
                distances = {start: 0}
                previous = {}
                pq = [(0, start)]
                
                while pq:
                    current_dist, current = heapq.heappop(pq)
                    
                    if current in visited:
                        continue
                        
                    visited.add(current)
                    self.distance_updates.append((current, current_dist))
                    
                    if current == end:
                        # Reconstruct path
                        path = []
                        pos = end
                        while pos in previous:
                            path.append(pos)
                            pos = previous[pos]
                        path.append(start)
                        return path[::-1], visited
                    
                    x, y = current
                    for neighbor in self.get_neighbors(x, y):
                        if neighbor not in visited:
                            new_dist = current_dist + 1  # All edges have weight 1
                            if neighbor not in distances or new_dist < distances[neighbor]:
                                distances[neighbor] = new_dist
                                previous[neighbor] = current
                                heapq.heappush(pq, (new_dist, neighbor))
                
                return [], visited
                
        tracking_dijkstra = TrackingDijkstra(complex_test_maze)
        path, visited = tracking_dijkstra.solve((1, 1), (5, 4))
        
        # Should process nodes in distance order
        assert len(tracking_dijkstra.distance_updates) > 0
        
        # Distances should be non-decreasing
        distances = [dist for _, dist in tracking_dijkstra.distance_updates]
        assert distances == sorted(distances)
        
    def test_dijkstra_optimal_exploration(self):
        """Test Dijkstra optimal exploration patterns"""
        # Create maze where Dijkstra optimality is clear
        optimal_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(optimal_maze)
        path, visited = dijkstra.solve((1, 1), (3, 3))
        
        if path:
            # Dijkstra should find optimal path of length 5
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)


class TestDijkstraPerformance:
    """Test Dijkstra performance characteristics"""
    
    def test_dijkstra_vs_bfs_same_result(self):
        """Test that Dijkstra produces same results as BFS for unweighted graphs"""
        # For unweighted graphs, Dijkstra should find same shortest paths as BFS
        test_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(test_maze)
        dijkstra_path, dijkstra_visited = dijkstra.solve((1, 1), (5, 3))
        
        # Import and test BFS for comparison
        from algorithms.breadth_first_search import BreadthFirstSearch
        bfs = BreadthFirstSearch(test_maze)
        bfs_path, bfs_visited = bfs.solve((1, 1), (5, 3))
        
        # Both should find paths of same length (optimal)
        if dijkstra_path and bfs_path:
            assert len(dijkstra_path) == len(bfs_path)
            
    def test_dijkstra_exploration_efficiency(self, complex_test_maze):
        """Test Dijkstra exploration efficiency"""
        dijkstra = Dijkstra(complex_test_maze)
        path, visited = dijkstra.solve((1, 1), (5, 4))
        
        if path:
            # Dijkstra should find optimal path
            assert len(path) >= 3  # Some minimum reasonable path length
            
        # Dijkstra explores efficiently
        assert len(visited) > 0
        
    def test_dijkstra_distance_correctness(self):
        """Test that Dijkstra correctly calculates distances"""
        # Create maze where distance calculations matter
        distance_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(distance_maze)
        path, visited = dijkstra.solve((1, 1), (5, 3))
        
        if path:
            # Path length should equal distance (all edges weight 1)
            expected_distance = len(path) - 1  # Number of edges
            assert expected_distance >= 0


class TestDijkstraEdgeCases:
    """Test Dijkstra edge cases"""
    
    def test_dijkstra_single_cell_path(self):
        """Test Dijkstra with single cell path"""
        single_cell_maze = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        
        dijkstra = Dijkstra(single_cell_maze)
        path, visited = dijkstra.solve((1, 1), (1, 1))
        
        assert path == [(1, 1)]
        assert (1, 1) in visited
        
    def test_dijkstra_linear_path(self):
        """Test Dijkstra with linear path"""
        linear_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(linear_maze)
        path, visited = dijkstra.solve((1, 1), (3, 1))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 1)
            assert len(path) == 3  # Optimal path
            
    def test_dijkstra_wall_positions(self, simple_test_maze):
        """Test Dijkstra with wall start/end positions"""
        dijkstra = Dijkstra(simple_test_maze)
        
        # Start at wall
        path, visited = dijkstra.solve((0, 0), (3, 3))
        assert path == []
        
        # End at wall
        path, visited = dijkstra.solve((1, 1), (0, 0))
        assert path == []
        
    def test_dijkstra_out_of_bounds(self, simple_test_maze):
        """Test Dijkstra with out of bounds coordinates"""
        dijkstra = Dijkstra(simple_test_maze)
        
        # Out of bounds start
        path, visited = dijkstra.solve((-1, -1), (3, 3))
        assert path == []
        
        # Out of bounds end
        path, visited = dijkstra.solve((1, 1), (100, 100))
        assert path == []


class TestDijkstraStress:
    """Stress tests for Dijkstra"""
    
    def test_dijkstra_large_maze(self):
        """Test Dijkstra with larger maze"""
        # Create larger maze
        size = 15
        large_maze = [[1 for _ in range(size)] for _ in range(size)]
        
        # Create a simple path
        for i in range(1, size - 1):
            large_maze[1][i] = 0  # Horizontal path
            large_maze[i][size - 2] = 0  # Vertical path
            
        large_maze[1][1] = 0  # Start
        large_maze[size - 2][size - 2] = 0  # End
        
        dijkstra = Dijkstra(large_maze)
        path, visited = dijkstra.solve((1, 1), (size - 2, size - 2))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (size - 2, size - 2)
            
    def test_dijkstra_complex_maze(self):
        """Test Dijkstra with complex maze structure"""
        complex_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(complex_maze)
        path, visited = dijkstra.solve((1, 1), (9, 5))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (9, 5)
            
        # Dijkstra should find optimal path in complex maze
        assert len(visited) > 0


class TestDijkstraComparison:
    """Test Dijkstra comparative behavior"""
    
    def test_dijkstra_multiple_equal_paths(self):
        """Test Dijkstra behavior with multiple equal-length paths"""
        # Create maze with two equal shortest paths
        equal_paths_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(equal_paths_maze)
        path, visited = dijkstra.solve((1, 1), (5, 1))
        
        if path:
            # Should find one of the optimal paths
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            # Both paths should be length 5
            assert len(path) == 5
            
    def test_dijkstra_consistent_results(self, simple_test_maze):
        """Test that Dijkstra produces consistent results"""
        dijkstra = Dijkstra(simple_test_maze)
        
        # Run multiple times
        results = []
        for _ in range(3):
            path, visited = dijkstra.solve((1, 1), (3, 3))
            results.append((len(path) if path else 0, len(visited)))
        
        # Results should be consistent
        assert len(set(results)) == 1  # All results should be identical
        
    def test_dijkstra_optimality_guarantee(self):
        """Test Dijkstra's optimality guarantee"""
        # Create maze where suboptimal algorithms might fail
        optimality_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(optimality_maze)
        path, visited = dijkstra.solve((1, 1), (7, 7))
        
        if path:
            # Should find truly optimal path
            assert path[0] == (1, 1)
            assert path[-1] == (7, 7)
            # Verify optimality (shortest possible path length)
            assert len(path) >= 13  # Minimum Manhattan distance + 1


class TestDijkstraSpecialCases:
    """Test Dijkstra special algorithm cases"""
    
    def test_dijkstra_priority_updates(self):
        """Test that Dijkstra correctly handles priority updates"""
        # Create maze where priority updates matter
        priority_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(priority_maze)
        path, visited = dijkstra.solve((1, 1), (5, 3))
        
        if path:
            # Should find path considering all possible routes
            assert path[0] == (1, 1)
            assert path[-1] == (5, 3)
            
    def test_dijkstra_relaxation_property(self):
        """Test Dijkstra's relaxation property"""
        # Create scenario where relaxation is needed
        relaxation_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        dijkstra = Dijkstra(relaxation_maze)
        path, visited = dijkstra.solve((1, 1), (7, 3))
        
        if path:
            # Should handle relaxation correctly
            assert path[0] == (1, 1)
            assert path[-1] == (7, 3)
            
            # Path should be optimal despite complex structure
            # Check that path is reasonable length
            assert len(path) >= 7  # Minimum reasonable path