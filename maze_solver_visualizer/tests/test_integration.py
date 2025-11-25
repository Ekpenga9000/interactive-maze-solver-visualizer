"""
Integration Tests for Maze Solver Visualizer
Testing component interactions and end-to-end workflows
"""
import pytest
from typing import List, Tuple, Set
from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm
from maze_visualizer import MazeVisualizer
from algorithms.depth_first_search import DepthFirstSearch
from algorithms.breadth_first_search import BreadthFirstSearch
from algorithms.dijkstra import Dijkstra


class TestMazeGeneratorSolverIntegration:
    """Test integration between maze generator and solver"""
    
    def test_generated_maze_always_solvable(self):
        """Test that all generated mazes are solvable"""
        generator = MazeGenerator(15, 15)
        
        # Test multiple generated mazes
        for _ in range(5):
            maze, start, end = generator.generate_with_positions()
            
            # Test with all algorithms
            solver = MazeSolver(maze)
            for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
                path, visited = solver.solve(start, end, algorithm)
                
                # Generated maze should always be solvable
                assert path is not None
                assert len(path) > 0
                assert path[0] == start
                assert path[-1] == end
                
    def test_maze_structure_consistency(self):
        """Test that generated maze structure is consistent with solver expectations"""
        generator = MazeGenerator(11, 11)
        maze, start, end = generator.generate_with_positions()
        
        # Test maze structure
        height = len(maze)
        width = len(maze[0])
        
        # Start and end should be valid positions
        start_x, start_y = start
        end_x, end_y = end
        
        assert 0 <= start_x < width
        assert 0 <= start_y < height
        assert 0 <= end_x < width
        assert 0 <= end_y < height
        
        # Start and end should be open cells
        assert maze[start_y][start_x] == 0
        assert maze[end_y][end_x] == 0
        
        # Test solving
        solver = MazeSolver(maze)
        path, visited = solver.solve(start, end, Algorithm.BFS)
        
        assert path is not None
        assert len(path) >= 2  # At least start and end


class TestAlgorithmComparison:
    """Test comparison between different algorithms"""
    
    def test_all_algorithms_find_solution(self, complex_test_maze):
        """Test that all algorithms find solution when one exists"""
        solver = MazeSolver(complex_test_maze)
        start = (1, 1)
        end = (5, 4)
        
        results = {}
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = solver.solve(start, end, algorithm)
            results[algorithm] = (path, visited)
            
        # All algorithms should find a solution
        for algorithm, (path, visited) in results.items():
            assert path is not None, f"{algorithm} should find a solution"
            assert len(path) > 0, f"{algorithm} should find non-empty path"
            assert path[0] == start, f"{algorithm} path should start correctly"
            assert path[-1] == end, f"{algorithm} path should end correctly"
            
    def test_bfs_dijkstra_optimal_paths(self):
        """Test that BFS and Dijkstra find optimal paths"""
        # Create maze with clear optimal path
        optimal_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        solver = MazeSolver(optimal_maze)
        start = (1, 1)
        end = (5, 3)
        
        # BFS and Dijkstra should find same length paths
        bfs_path, _ = solver.solve(start, end, Algorithm.BFS)
        dijkstra_path, _ = solver.solve(start, end, Algorithm.DIJKSTRA)
        
        assert bfs_path is not None
        assert dijkstra_path is not None
        assert len(bfs_path) == len(dijkstra_path)  # Both should be optimal
        
    def test_algorithm_visited_cells_patterns(self, complex_test_maze):
        """Test different exploration patterns of algorithms"""
        solver = MazeSolver(complex_test_maze)
        start = (1, 1)
        end = (5, 4)
        
        dfs_path, dfs_visited = solver.solve(start, end, Algorithm.DFS)
        bfs_path, bfs_visited = solver.solve(start, end, Algorithm.BFS)
        dijkstra_path, dijkstra_visited = solver.solve(start, end, Algorithm.DIJKSTRA)
        
        # All should find solutions
        assert dfs_path and bfs_path and dijkstra_path
        
        # BFS and Dijkstra should visit similar patterns (both optimal)
        # DFS might visit different patterns
        
        # All visited sets should contain the path
        for path, visited in [(dfs_path, dfs_visited), (bfs_path, bfs_visited), (dijkstra_path, dijkstra_visited)]:
            for pos in path:
                assert pos in visited


class TestVisualizerIntegration:
    """Test integration with visualizer component"""
    
    def test_visualizer_initialization(self):
        """Test that visualizer initializes with proper components"""
        # Note: This test doesn't actually create pygame window
        # but tests the integration logic
        
        generator = MazeGenerator(15, 15)
        maze, start, end = generator.generate_with_positions()
        
        # Test that we can create solver and algorithm instances
        solver = MazeSolver(maze)
        
        # Test algorithm instantiation
        dfs = DepthFirstSearch(maze)
        bfs = BreadthFirstSearch(maze)
        dijkstra = Dijkstra(maze)
        
        assert dfs.maze == maze
        assert bfs.maze == maze
        assert dijkstra.maze == maze
        
    def test_real_time_solving_data_flow(self):
        """Test data flow for real-time solving visualization"""
        generator = MazeGenerator(11, 11)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Test that solve_animated returns generator
        real_time_generator = solver.solve_animated(maze, start, end, Algorithm.BFS)
        
        # Test that generator produces steps
        steps = list(real_time_generator)
        assert len(steps) > 0
        
        # Each step should have proper structure
        for step in steps:
            assert 'current' in step
            assert 'visited' in step
            assert 'path' in step
            
            current = step['current']
            visited = step['visited']
            path = step['path']
            
            assert isinstance(current, (tuple, type(None)))
            assert isinstance(visited, set)
            assert isinstance(path, list)


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows"""
    
    def test_complete_maze_solving_workflow(self):
        """Test complete workflow from generation to solving"""
        # Generate maze
        generator = MazeGenerator(13, 13)
        maze, start, end = generator.generate_with_positions()
        
        # Solve with each algorithm
        solver = MazeSolver(maze)
        algorithms = [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]
        
        results = {}
        for algorithm in algorithms:
            path, visited = solver.solve(start, end, algorithm)
            results[algorithm] = (path, visited)
            
            # Verify solution
            assert path is not None
            assert len(path) >= 2
            assert path[0] == start
            assert path[-1] == end
            
            # Verify path validity
            for x, y in path:
                assert 0 <= x < len(maze[0])
                assert 0 <= y < len(maze)
                assert maze[y][x] == 0
                
        # Compare results
        paths = [results[alg][0] for alg in algorithms]
        
        # All should find solutions
        for path in paths:
            assert path is not None
            
    def test_multiple_maze_generations_and_solutions(self):
        """Test multiple generation and solution cycles"""
        generator = MazeGenerator(9, 9)
        solver = MazeSolver(maze)
        
        # Test multiple cycles
        for i in range(3):
            maze, start, end = generator.generate_with_positions()
            
            # Should be solvable every time
            for algorithm in [Algorithm.BFS, Algorithm.DIJKSTRA]:
                path, visited = solver.solve(start, end, algorithm)
                
                assert path is not None
                assert len(path) > 0
                assert path[0] == start
                assert path[-1] == end
                
    def test_different_maze_sizes_integration(self):
        """Test integration with different maze sizes"""
        sizes = [(7, 7), (11, 11), (15, 15)]
        solver = MazeSolver(maze)
        
        for width, height in sizes:
            generator = MazeGenerator(width, height)
            maze, start, end = generator.generate_with_positions()
            
            # Test maze structure
            assert len(maze) == height
            assert len(maze[0]) == width
            
            # Test solvability
            path, visited = solver.solve(start, end, Algorithm.BFS)
            assert path is not None
            assert len(path) >= 2


class TestErrorHandlingIntegration:
    """Test error handling in integrated components"""
    
    def test_invalid_maze_handling(self):
        """Test handling of invalid maze structures"""
        # Test with empty maze
        try:
            solver = MazeSolver([])
        except (IndexError, ValueError):
            pass  # Expected error
            
        # Test with inconsistent maze structure
        invalid_maze = [
            [1, 1, 1],
            [1, 0],  # Missing column
            [1, 1, 1]
        ]
        
        # Should handle gracefully or raise appropriate error
        try:
            solver = MazeSolver(invalid_maze)
            path, visited = solver.solve((1, 1), (1, 1), Algorithm.BFS)
            # If it doesn't raise an error, should return empty path
            assert path == []
        except (IndexError, ValueError):
            # Expected error for malformed maze
            pass
            
    def test_invalid_start_end_positions(self):
        """Test handling of invalid start/end positions"""
        maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        solver = MazeSolver(maze)
        
        # Wall positions
        path, visited = solver.solve((0, 0), (3, 3), Algorithm.BFS)
        assert path == []
        
        # Out of bounds
        path, visited = solver.solve((-1, -1), (3, 3), Algorithm.BFS)
        assert path == []
        
        path, visited = solver.solve((1, 1), (10, 10), Algorithm.BFS)
        assert path == []


class TestPerformanceIntegration:
    """Test performance characteristics of integrated system"""
    
    def test_solving_performance_consistency(self):
        """Test that solving performance is consistent"""
        generator = MazeGenerator(15, 15)
        solver = MazeSolver(maze)
        
        # Generate one maze and solve multiple times
        maze, start, end = generator.generate_with_positions()
        
        results = []
        for _ in range(3):
            path, visited = solver.solve(start, end, Algorithm.BFS)
            results.append((len(path) if path else 0, len(visited)))
            
        # Results should be identical (deterministic)
        assert len(set(results)) == 1
        
    def test_real_time_performance(self):
        """Test real-time solving performance"""
        generator = MazeGenerator(11, 11)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Test that real-time generator produces reasonable number of steps
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            steps = list(solver.solve_animated(maze, start, end, algorithm))
            
            # Should produce some steps
            assert len(steps) > 0
            
            # Should not produce excessive steps
            total_cells = len(maze) * len(maze[0])
            assert len(steps) <= total_cells  # Shouldn't visit more than all cells