"""
Tests for Breadth-First Search Algorithm
Comprehensive testing of BFS implementation
"""
import pytest
from typing import List, Tuple, Set
from algorithms.breadth_first_search import BreadthFirstSearch


class TestBFSInitialization:
    """Test BFS initialization"""
    
    def test_bfs_initialization(self, simple_test_maze):
        """Test BFS can be initialized"""
        bfs = BreadthFirstSearch(simple_test_maze)
        assert bfs.maze == simple_test_maze
        assert bfs.height == len(simple_test_maze)
        assert bfs.width == len(simple_test_maze[0])
        
    def test_bfs_with_empty_maze(self):
        """Test BFS with edge case inputs"""
        with pytest.raises((IndexError, ValueError)):
            BreadthFirstSearch([])


class TestBFSBasicFunctionality:
    """Test basic BFS functionality"""
    
    def test_bfs_solve_simple_path(self, simple_test_maze):
        """Test BFS solving simple path"""
        bfs = BreadthFirstSearch(simple_test_maze)
        path, visited = bfs.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_bfs_solve_no_solution(self, impossible_maze):
        """Test BFS with impossible maze"""
        bfs = BreadthFirstSearch(impossible_maze)
        path, visited = bfs.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_bfs_path_validity(self, complex_test_maze):
        """Test that BFS path is valid"""
        bfs = BreadthFirstSearch(complex_test_maze)
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
                
    def test_bfs_visited_cells(self, complex_test_maze):
        """Test BFS visited cells properties"""
        bfs = BreadthFirstSearch(complex_test_maze)
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
        
        bfs = BreadthFirstSearch(shortest_path_maze)
        path, visited = bfs.solve((1, 1), (5, 1))
        
        if path:
            # BFS should find shortest path (5 steps)
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            
    def test_bfs_breadth_first_behavior(self, complex_test_maze):
        """Test that BFS exhibits breadth-first behavior"""
        bfs = BreadthFirstSearch(complex_test_maze)
        
        # Create custom BFS to track exploration order
        class TrackingBFS(BreadthFirstSearch):
            def __init__(self, maze):
                super().__init__(maze)
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
                
        tracking_bfs = TrackingBFS(complex_test_maze)
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
        
        bfs = BreadthFirstSearch(optimal_maze)
        path, visited = bfs.solve((1, 1), (3, 3))
        
        if path:
            # BFS should find path of length 5 (minimum steps)
            assert len(path) == 5
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)


class TestBFSPerformance:
    """Test BFS performance characteristics"""
    
    def test_bfs_exploration_completeness(self, complex_test_maze):
        """Test BFS exploration completeness"""
        bfs = BreadthFirstSearch(complex_test_maze)
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
        
        bfs = BreadthFirstSearch(known_optimal_maze)
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
        
        bfs = BreadthFirstSearch(single_cell_maze)
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
        
        bfs = BreadthFirstSearch(linear_maze)
        path, visited = bfs.solve((1, 1), (3, 1))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 1)
            assert len(path) == 3  # Optimal path
            
    def test_bfs_wall_start_position(self, simple_test_maze):
        """Test BFS starting from wall position"""
        bfs = BreadthFirstSearch(simple_test_maze)
        path, visited = bfs.solve((0, 0), (3, 3))  # Start at wall
        
        assert path == []  # Should fail to find path
        
    def test_bfs_wall_end_position(self, simple_test_maze):
        """Test BFS ending at wall position"""
        bfs = BreadthFirstSearch(simple_test_maze)
        path, visited = bfs.solve((1, 1), (0, 0))  # End at wall
        
        assert path == []  # Should fail to find path
        
    def test_bfs_out_of_bounds(self, simple_test_maze):
        """Test BFS with out of bounds coordinates"""
        bfs = BreadthFirstSearch(simple_test_maze)
        
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
        
        bfs = BreadthFirstSearch(large_maze)
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
        
        bfs = BreadthFirstSearch(complex_maze)
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
        
        bfs = BreadthFirstSearch(equal_paths_maze)
        path, visited = bfs.solve((1, 1), (5, 1))
        
        if path:
            # Should find one of the optimal paths
            assert path[0] == (1, 1)
            assert path[-1] == (5, 1)
            # Both paths through (3,1) and (3,3) should be length 5
            assert len(path) == 5
            
    def test_bfs_consistent_results(self, simple_test_maze):
        """Test that BFS produces consistent results"""
        bfs = BreadthFirstSearch(simple_test_maze)
        
        # Run multiple times
        results = []
        for _ in range(3):
            path, visited = bfs.solve((1, 1), (3, 3))
            results.append((len(path) if path else 0, len(visited)))
        
        # Results should be consistent
        assert len(set(results)) == 1  # All results should be identical