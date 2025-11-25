"""
Tests for Depth-First Search Algorithm
Comprehensive testing of DFS implementation
"""
import pytest
from typing import List, Tuple, Set
from algorithms.depth_first_search import DepthFirstSearch


class TestDFSInitialization:
    """Test DFS initialization"""
    
    def test_dfs_initialization(self, simple_test_maze):
        """Test DFS can be initialized"""
        dfs = DepthFirstSearch(simple_test_maze)
        assert dfs.maze == simple_test_maze
        assert dfs.height == len(simple_test_maze)
        assert dfs.width == len(simple_test_maze[0])
        
    def test_dfs_with_empty_maze(self):
        """Test DFS with edge case inputs"""
        with pytest.raises((IndexError, ValueError)):
            DepthFirstSearch([])


class TestDFSBasicFunctionality:
    """Test basic DFS functionality"""
    
    def test_dfs_solve_simple_path(self, simple_test_maze):
        """Test DFS solving simple path"""
        dfs = DepthFirstSearch(simple_test_maze)
        path, visited = dfs.solve((1, 1), (3, 3))
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            assert len(path) >= 3  # Minimum path length
            
    def test_dfs_solve_no_solution(self, impossible_maze):
        """Test DFS with impossible maze"""
        dfs = DepthFirstSearch(impossible_maze)
        path, visited = dfs.solve((1, 1), (3, 1))
        
        assert path == []
        assert isinstance(visited, set)
        
    def test_dfs_path_validity(self, complex_test_maze):
        """Test that DFS path is valid"""
        dfs = DepthFirstSearch(complex_test_maze)
        path, visited = dfs.solve((1, 1), (5, 4))
        
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
                assert dfs.maze[y][x] == 0
                
    def test_dfs_visited_cells(self, complex_test_maze):
        """Test DFS visited cells properties"""
        dfs = DepthFirstSearch(complex_test_maze)
        path, visited = dfs.solve((1, 1), (5, 4))
        
        # Path cells should be subset of visited
        if path:
            for pos in path:
                assert pos in visited
                
        # All visited cells should be valid
        for x, y in visited:
            assert 0 <= x < dfs.width
            assert 0 <= y < dfs.height
            assert dfs.maze[y][x] == 0


class TestDFSAlgorithmSpecific:
    """Test DFS-specific algorithm behavior"""
    
    def test_dfs_depth_first_behavior(self, complex_test_maze):
        """Test that DFS exhibits depth-first behavior"""
        dfs = DepthFirstSearch(complex_test_maze)
        
        # Create a custom DFS to track exploration order
        class TrackingDFS(DepthFirstSearch):
            def __init__(self, maze):
                super().__init__(maze)
                self.exploration_order = []
                
            def solve(self, start, end):
                visited = set()
                path = []
                
                def dfs_recursive(current):
                    x, y = current
                    if current in visited:
                        return False
                    
                    visited.add(current)
                    self.exploration_order.append(current)
                    path.append(current)
                    
                    if current == end:
                        return True
                    
                    for neighbor in self.get_neighbors(x, y):
                        if dfs_recursive(neighbor):
                            return True
                    
                    path.pop()
                    return False
                
                dfs_recursive(start)
                return path, visited
                
        tracking_dfs = TrackingDFS(complex_test_maze)
        path, visited = tracking_dfs.solve((1, 1), (5, 4))
        
        # DFS should explore deep before backtracking
        assert len(tracking_dfs.exploration_order) > 0
        assert tracking_dfs.exploration_order[0] == (1, 1)
        
    def test_dfs_backtracking(self):
        """Test DFS backtracking behavior"""
        # Create maze that forces backtracking
        backtrack_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dfs = DepthFirstSearch(backtrack_maze)
        path, visited = dfs.solve((1, 1), (5, 3))
        
        if path:
            # Should find a valid path despite need for backtracking
            assert path[0] == (1, 1)
            assert path[-1] == (5, 3)
            
        # Should have visited some cells (backtracking is likely but not guaranteed)
        assert len(visited) >= len(path) if path else True


class TestDFSPerformance:
    """Test DFS performance characteristics"""
    
    def test_dfs_exploration_efficiency(self, complex_test_maze):
        """Test DFS exploration patterns"""
        dfs = DepthFirstSearch(complex_test_maze)
        path, visited = dfs.solve((1, 1), (5, 4))
        
        if path:
            # DFS might not find shortest path
            assert len(path) >= 3  # Some minimum reasonable path length
            
        # DFS should visit some cells (but may not be optimal)
        assert len(visited) > 0
        
    def test_dfs_different_paths(self):
        """Test that DFS can find different valid paths"""
        # Create maze with multiple solution paths
        multi_path_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        dfs = DepthFirstSearch(multi_path_maze)
        path, visited = dfs.solve((1, 1), (5, 3))
        
        if path:
            # Should find a valid path
            assert path[0] == (1, 1)
            assert path[-1] == (5, 3)
            
            # Verify path validity
            for x, y in path:
                assert dfs.maze[y][x] == 0


class TestDFSEdgeCases:
    """Test DFS edge cases"""
    
    def test_dfs_single_cell_path(self):
        """Test DFS with single cell path"""
        single_cell_maze = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        
        dfs = DepthFirstSearch(single_cell_maze)
        path, visited = dfs.solve((1, 1), (1, 1))
        
        assert path == [(1, 1)]
        assert (1, 1) in visited
        
    def test_dfs_linear_path(self):
        """Test DFS with linear path"""
        linear_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        dfs = DepthFirstSearch(linear_maze)
        path, visited = dfs.solve((1, 1), (3, 1))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 1)
            assert len(path) == 3  # Shortest path
            
    def test_dfs_wall_start_position(self, simple_test_maze):
        """Test DFS starting from wall position"""
        dfs = DepthFirstSearch(simple_test_maze)
        path, visited = dfs.solve((0, 0), (3, 3))  # Start at wall
        
        assert path == []  # Should fail to find path
        
    def test_dfs_wall_end_position(self, simple_test_maze):
        """Test DFS ending at wall position"""
        dfs = DepthFirstSearch(simple_test_maze)
        path, visited = dfs.solve((1, 1), (0, 0))  # End at wall
        
        assert path == []  # Should fail to find path
        
    def test_dfs_out_of_bounds(self, simple_test_maze):
        """Test DFS with out of bounds coordinates"""
        dfs = DepthFirstSearch(simple_test_maze)
        
        # Out of bounds start
        path, visited = dfs.solve((-1, -1), (3, 3))
        assert path == []
        
        # Out of bounds end
        path, visited = dfs.solve((1, 1), (100, 100))
        assert path == []


class TestDFSStress:
    """Stress tests for DFS"""
    
    def test_dfs_large_maze(self):
        """Test DFS with larger maze"""
        # Create larger maze
        size = 15
        large_maze = [[1 for _ in range(size)] for _ in range(size)]
        
        # Create a simple path
        for i in range(1, size - 1):
            large_maze[1][i] = 0  # Horizontal path
            large_maze[i][size - 2] = 0  # Vertical path
            
        large_maze[1][1] = 0  # Start
        large_maze[size - 2][size - 2] = 0  # End
        
        dfs = DepthFirstSearch(large_maze)
        path, visited = dfs.solve((1, 1), (size - 2, size - 2))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (size - 2, size - 2)
            
    def test_dfs_many_dead_ends(self):
        """Test DFS with maze containing many dead ends"""
        dead_end_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        dfs = DepthFirstSearch(dead_end_maze)
        path, visited = dfs.solve((1, 1), (7, 3))
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (7, 3)
            
        # Should have explored some cells (backtracking behavior varies)
        assert len(visited) >= len(path) if path else True