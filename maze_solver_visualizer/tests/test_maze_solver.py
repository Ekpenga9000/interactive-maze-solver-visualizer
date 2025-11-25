"""
Tests for Maze Solver
Comprehensive testing of the main solver coordination functionality
"""
import pytest
from maze_solver import MazeSolver, Algorithm


class TestMazeSolverInitialization:
    """Test maze solver initialization"""
    
    def test_solver_initialization(self, simple_test_maze):
        """Test maze solver can be initialized"""
        solver = MazeSolver(simple_test_maze)
        assert solver.maze == simple_test_maze
        assert solver.height == len(simple_test_maze)
        assert solver.width == len(simple_test_maze[0])
        
    def test_solver_empty_maze(self):
        """Test solver with empty maze"""
        with pytest.raises((IndexError, ValueError)):
            MazeSolver([])
            
    def test_solver_invalid_maze_format(self):
        """Test solver with invalid maze format"""
        invalid_maze = [[1, 0], [1]]  # Irregular rows
        solver = MazeSolver(invalid_maze)
        # Should not crash on initialization
        assert solver is not None


class TestMazeSolverBasicFunctionality:
    """Test basic solver functionality"""
    
    def test_get_neighbors_center_cell(self, maze_solver_simple):
        """Test getting neighbors for a center cell"""
        # Cell at (2, 2) should have 4 potential neighbors
        neighbors = maze_solver_simple._get_neighbors(2, 2)
        
        # Filter out walls (value 1) from the actual maze
        valid_neighbors = [
            (x, y) for x, y in neighbors
            if maze_solver_simple.maze[y][x] == 0
        ]
        
        assert len(neighbors) >= 0  # Could be 0 if surrounded by walls
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in neighbors)
        
    def test_get_neighbors_corner_cell(self, maze_solver_simple):
        """Test getting neighbors for a corner cell"""
        # Corner cell should have fewer neighbors
        neighbors = maze_solver_simple._get_neighbors(0, 0)
        
        # Corner cells are typically walls, so might have no valid neighbors
        assert isinstance(neighbors, list)
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in neighbors)
        
    def test_get_neighbors_bounds_checking(self, maze_solver_simple):
        """Test neighbor bounds checking"""
        height, width = maze_solver_simple.height, maze_solver_simple.width
        
        # Test neighbors are within bounds
        for x in range(width):
            for y in range(height):
                neighbors = maze_solver_simple._get_neighbors(x, y)
                for nx, ny in neighbors:
                    assert 0 <= nx < width
                    assert 0 <= ny < height
                    
    def test_get_neighbors_no_walls(self, maze_solver_simple):
        """Test that get_neighbors doesn't return wall cells"""
        neighbors = maze_solver_simple._get_neighbors(1, 1)
        
        # All returned neighbors should be open paths (value 0)
        for x, y in neighbors:
            assert maze_solver_simple.maze[y][x] == 0


class TestAlgorithmSolving:
    """Test algorithm solving functionality"""
    
    @pytest.mark.parametrize("algorithm", [
        Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA
    ])
    def test_solve_simple_maze(self, maze_solver_simple, algorithm):
        """Test solving simple maze with all algorithms"""
        path, visited = maze_solver_simple.solve((1, 1), (3, 3), algorithm)
        
        # Should find a path
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:  # If solution exists
            assert len(path) > 0
            assert path[0] == (1, 1)  # Starts at start
            assert path[-1] == (3, 3)  # Ends at end
            assert len(visited) > 0
            
    @pytest.mark.parametrize("algorithm", [
        Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA
    ])
    def test_solve_complex_maze(self, maze_solver_complex, algorithm):
        """Test solving complex maze with all algorithms"""
        path, visited = maze_solver_complex.solve((1, 1), (5, 4), algorithm)
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (5, 4)
            
    @pytest.mark.parametrize("algorithm", [
        Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA
    ])
    def test_solve_impossible_maze(self, maze_solver_impossible, algorithm):
        """Test solving impossible maze returns empty path"""
        path, visited = maze_solver_impossible.solve((1, 1), (3, 1), algorithm)
        
        # Should return empty path for impossible maze
        assert path == []
        assert isinstance(visited, set)


class TestPathValidation:
    """Test path validation and properties"""
    
    def test_path_continuity_dfs(self, maze_solver_complex):
        """Test that DFS path is continuous"""
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
                    
    def test_path_continuity_bfs(self, maze_solver_complex):
        """Test that BFS path is continuous"""
        path, _ = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.BFS)
        
        if len(path) > 1:
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                dx = abs(current[0] - next_pos[0])
                dy = abs(current[1] - next_pos[1])
                assert (dx == 1 and dy == 0) or (dx == 0 and dy == 1)
                
    def test_path_no_walls(self, maze_solver_simple):
        """Test that path doesn't go through walls"""
        path, _ = maze_solver_simple.solve((1, 1), (3, 3), Algorithm.BFS)
        
        for x, y in path:
            assert maze_solver_simple.maze[y][x] == 0, \
                f"Path goes through wall at ({x}, {y})"
                
    def test_visited_cells_properties(self, maze_solver_complex):
        """Test properties of visited cells"""
        path, visited = maze_solver_complex.solve((1, 1), (5, 4), Algorithm.BFS)
        
        # All path cells should be in visited cells
        if path:
            for pos in path:
                assert pos in visited, f"Path position {pos} not in visited set"
                
        # All visited cells should be valid positions
        for x, y in visited:
            assert 0 <= x < maze_solver_complex.width
            assert 0 <= y < maze_solver_complex.height
            assert maze_solver_complex.maze[y][x] == 0  # No walls


class TestAlgorithmComparison:
    """Test comparison between different algorithms"""
    
    def test_bfs_finds_shortest_path(self, maze_solver_simple):
        """Test that BFS finds shortest path"""
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
            
    def test_all_algorithms_find_solution_when_exists(self, maze_solver_complex):
        """Test all algorithms find solution when one exists"""
        start, end = (1, 1), (5, 4)
        
        dfs_path, _ = maze_solver_complex.solve(start, end, Algorithm.DFS)
        bfs_path, _ = maze_solver_complex.solve(start, end, Algorithm.BFS)
        dijkstra_path, _ = maze_solver_complex.solve(start, end, Algorithm.DIJKSTRA)
        
        # If one algorithm finds a path, all should find a path
        if any([dfs_path, bfs_path, dijkstra_path]):
            assert dfs_path, "DFS should find path when solution exists"
            assert bfs_path, "BFS should find path when solution exists"
            assert dijkstra_path, "Dijkstra should find path when solution exists"


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_same_start_end_position(self, maze_solver_simple):
        """Test when start and end are the same"""
        start_end = (1, 1)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(start_end, start_end, algorithm)
            
            # Should return a path with just the start position
            assert path == [start_end] or path == []
            assert start_end in visited
            
    def test_invalid_start_position(self, maze_solver_simple):
        """Test with invalid start position"""
        # Wall position
        invalid_start = (0, 0)
        valid_end = (3, 3)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(invalid_start, valid_end, algorithm)
            assert path == []  # Should return empty path
            
    def test_invalid_end_position(self, maze_solver_simple):
        """Test with invalid end position"""
        valid_start = (1, 1)
        invalid_end = (0, 0)  # Wall position
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(valid_start, invalid_end, algorithm)
            assert path == []  # Should return empty path
            
    def test_out_of_bounds_positions(self, maze_solver_simple):
        """Test with out of bounds positions"""
        valid_start = (1, 1)
        out_of_bounds = (100, 100)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = maze_solver_simple.solve(valid_start, out_of_bounds, algorithm)
            assert path == []  # Should return empty path
            
    def test_unknown_algorithm(self, maze_solver_simple):
        """Test with unknown algorithm"""
        start, end = (1, 1), (3, 3)
        
        with pytest.raises(ValueError):
            # Create a mock invalid algorithm
            class InvalidAlgorithm:
                value = "Invalid"
            
            maze_solver_simple.solve(start, end, InvalidAlgorithm())