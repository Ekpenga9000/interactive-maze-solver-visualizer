"""
Performance Tests for Maze Solver Visualizer
Testing performance characteristics and benchmarks
"""
import pytest
import time
from typing import List, Tuple, Dict
from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm


class TestMazeGenerationPerformance:
    """Test maze generation performance"""
    
    @pytest.mark.parametrize("size", [(9, 9), (15, 15), (21, 21)])
    def test_generation_time(self, size):
        """Test maze generation time for different sizes"""
        width, height = size
        generator = MazeGenerator(width, height)
        
        start_time = time.time()
        maze, start, end = generator.generate_with_positions()
        generation_time = time.time() - start_time
        
        # Should generate maze in reasonable time
        assert generation_time < 5.0  # Should be fast
        
        # Verify maze properties
        assert len(maze) == height
        assert len(maze[0]) == width
        assert maze[start[1]][start[0]] == 0
        assert maze[end[1]][end[0]] == 0
        
    def test_multiple_generations_performance(self):
        """Test performance of multiple maze generations"""
        generator = MazeGenerator(11, 11)
        
        start_time = time.time()
        for _ in range(10):
            maze, start, end = generator.generate_with_positions()
        total_time = time.time() - start_time
        
        # Should handle multiple generations efficiently
        assert total_time < 10.0
        average_time = total_time / 10
        assert average_time < 1.0


class TestAlgorithmPerformance:
    """Test algorithm performance characteristics"""
    
    @pytest.mark.parametrize("algorithm", [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA])
    def test_algorithm_solving_time(self, algorithm, complex_test_maze):
        """Test solving time for each algorithm"""
        solver = MazeSolver(maze)
        start = (1, 1)
        end = (5, 4)
        
        start_time = time.time()
        path, visited = solver.solve(complex_test_maze, start, end, algorithm)
        solve_time = time.time() - start_time
        
        # Should solve in reasonable time
        assert solve_time < 1.0
        
        # Should find valid solution
        if path:
            assert path[0] == start
            assert path[-1] == end
            
    def test_algorithm_performance_comparison(self):
        """Compare performance of different algorithms"""
        generator = MazeGenerator(15, 15)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        performance_results = {}
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            start_time = time.time()
            path, visited = solver.solve(start, end, algorithm)
            solve_time = time.time() - start_time
            
            performance_results[algorithm] = {
                'time': solve_time,
                'path_length': len(path) if path else 0,
                'visited_count': len(visited)
            }
        
        # All algorithms should complete in reasonable time
        for algorithm, results in performance_results.items():
            assert results['time'] < 2.0
            
    @pytest.mark.parametrize("size", [(11, 11), (19, 19), (25, 25)])
    def test_algorithm_scalability(self, size):
        """Test algorithm performance scalability"""
        width, height = size
        generator = MazeGenerator(width, height)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Test BFS (known to be optimal and efficient)
        start_time = time.time()
        path, visited = solver.solve(maze, start, end, Algorithm.BFS)
        solve_time = time.time() - start_time
        
        # Larger mazes should still solve in reasonable time
        max_time = 5.0  # Allow more time for larger mazes
        assert solve_time < max_time
        
        # Should find solution
        assert path is not None
        assert len(path) > 0


class TestRealTimePerformance:
    """Test real-time solving performance"""
    
    @pytest.mark.parametrize("algorithm", [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA])
    def test_real_time_generation_speed(self, algorithm):
        """Test real-time step generation speed"""
        generator = MazeGenerator(11, 11)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Test that real-time generation is fast enough
        start_time = time.time()
        steps = list(solver.solve_animated(maze, start, end, algorithm))
        generation_time = time.time() - start_time
        
        # Should generate all steps quickly
        assert generation_time < 2.0
        
        # Should produce reasonable number of steps
        assert len(steps) > 0
        assert len(steps) <= len(maze) * len(maze[0])  # Upper bound
        
    def test_real_time_step_consistency(self):
        """Test consistency of real-time step generation"""
        generator = MazeGenerator(9, 9)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Generate steps multiple times
        results = []
        for _ in range(3):
            steps = list(solver.solve_animated(maze, start, end, Algorithm.BFS))
            results.append(len(steps))
        
        # Should produce consistent results
        assert len(set(results)) == 1  # All runs should produce same number of steps


class TestMemoryPerformance:
    """Test memory usage characteristics"""
    
    def test_maze_memory_usage(self):
        """Test memory usage for different maze sizes"""
        sizes = [(9, 9), (15, 15), (21, 21)]
        
        for width, height in sizes:
            generator = MazeGenerator(width, height)
            maze, start, end = generator.generate_with_positions()
            
            # Verify maze structure doesn't use excessive memory
            assert len(maze) == height
            assert all(len(row) == width for row in maze)
            
            # Test that maze can be processed efficiently
            solver = MazeSolver(maze)
            path, visited = solver.solve(maze, start, end, Algorithm.BFS)
            
            # Memory usage should be reasonable (visited set shouldn't be excessive)
            max_visited = width * height
            assert len(visited) <= max_visited
            
    def test_algorithm_memory_efficiency(self, complex_test_maze):
        """Test memory efficiency of algorithms"""
        solver = MazeSolver(maze)
        start = (1, 1)
        end = (5, 4)
        
        maze_size = len(complex_test_maze) * len(complex_test_maze[0])
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = solver.solve(complex_test_maze, start, end, algorithm)
            
            # Visited set shouldn't exceed maze size
            assert len(visited) <= maze_size
            
            # Path shouldn't be excessively long
            if path:
                assert len(path) <= maze_size  # Upper bound


class TestStressTests:
    """Stress tests for the system"""
    
    def test_repeated_solving_stress(self):
        """Stress test with repeated solving"""
        generator = MazeGenerator(13, 13)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Solve many times
        for i in range(20):
            for algorithm in [Algorithm.BFS, Algorithm.DIJKSTRA]:
                path, visited = solver.solve(start, end, algorithm)
                
                # Should consistently find solution
                assert path is not None
                assert len(path) > 0
                assert path[0] == start
                assert path[-1] == end
                
    def test_multiple_maze_stress(self):
        """Stress test with multiple different mazes"""
        solver = MazeSolver(maze)
        
        # Generate and solve many different mazes
        for i in range(10):
            size = 11 + (i % 3) * 2  # Vary size: 11, 13, 15
            generator = MazeGenerator(size, size)
            maze, start, end = generator.generate_with_positions()
            
            # Test with BFS (most reliable)
            path, visited = solver.solve(maze, start, end, Algorithm.BFS)
            
            assert path is not None
            assert len(path) >= 2
            assert path[0] == start
            assert path[-1] == end
            
    def test_large_maze_stress(self):
        """Stress test with large maze"""
        # Test with larger maze (but reasonable for testing)
        generator = MazeGenerator(25, 25)
        maze, start, end = generator.generate_with_positions()
        solver = MazeSolver(maze)
        
        # Should handle large maze efficiently
        start_time = time.time()
        path, visited = solver.solve(maze, start, end, Algorithm.BFS)
        solve_time = time.time() - start_time
        
        # Should solve large maze in reasonable time
        assert solve_time < 5.0
        
        # Should find valid solution
        assert path is not None
        assert len(path) > 0
        assert path[0] == start
        assert path[-1] == end


class TestEdgePerformance:
    """Test performance with edge cases"""
    
    def test_minimal_maze_performance(self):
        """Test performance with minimal maze"""
        # Smallest possible solvable maze
        minimal_maze = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        
        solver = MazeSolver(maze)
        start = (1, 1)
        end = (1, 1)  # Start equals end
        
        # Should handle instantly
        start_time = time.time()
        path, visited = solver.solve(minimal_maze, start, end, Algorithm.BFS)
        solve_time = time.time() - start_time
        
        assert solve_time < 0.1  # Should be very fast
        assert path == [start]
        
    def test_linear_maze_performance(self):
        """Test performance with linear maze"""
        # Create long linear maze
        width = 21
        linear_maze = [[1] * width for _ in range(3)]
        for i in range(1, width - 1):
            linear_maze[1][i] = 0
            
        solver = MazeSolver(maze)
        start = (1, 1)
        end = (width - 2, 1)
        
        # Should handle linear maze efficiently
        start_time = time.time()
        path, visited = solver.solve(linear_maze, start, end, Algorithm.BFS)
        solve_time = time.time() - start_time
        
        assert solve_time < 0.5
        if path:
            assert path[0] == start
            assert path[-1] == end
            assert len(path) == width - 2  # Optimal length


class TestBenchmarks:
    """Benchmark tests for comparison"""
    
    def test_algorithm_efficiency_benchmark(self):
        """Benchmark algorithm efficiency"""
        # Create standardized test maze
        benchmark_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        solver = MazeSolver(maze)
        start = (1, 1)
        end = (9, 7)
        
        benchmark_results = {}
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            start_time = time.time()
            path, visited = solver.solve(benchmark_maze, start, end, algorithm)
            solve_time = time.time() - start_time
            
            benchmark_results[algorithm] = {
                'time': solve_time,
                'path_length': len(path) if path else 0,
                'visited_count': len(visited),
                'efficiency': len(path) / len(visited) if path and visited else 0
            }
        
        # Verify all algorithms found solutions
        for algorithm, results in benchmark_results.items():
            assert results['path_length'] > 0, f"{algorithm} should find solution"
            assert results['time'] < 1.0, f"{algorithm} should be fast enough"
            
        # BFS and Dijkstra should find optimal paths (same length)
        bfs_length = benchmark_results[Algorithm.BFS]['path_length']
        dijkstra_length = benchmark_results[Algorithm.DIJKSTRA]['path_length']
        assert bfs_length == dijkstra_length, "BFS and Dijkstra should find same optimal length"