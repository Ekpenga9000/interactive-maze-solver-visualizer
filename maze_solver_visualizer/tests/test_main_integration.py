#!/usr/bin/env python3
"""
Tests for Main Entry Points and Integration
Tests the main execution paths and overall system integration
"""

import pytest
import sys
import os
import tempfile
import unittest.mock as mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, parse_arguments, create_and_solve_maze
from demo import main as demo_main
from maze_solver import MazeSolver, Algorithm
from maze_generator import MazeGenerator
from maze_visualizer import MazeVisualizer

class TestMainFunction:
    """Test main.py functionality"""
    
    def test_parse_arguments_defaults(self):
        """Test argument parsing with default values"""
        # Mock sys.argv to test argument parsing
        with mock.patch('sys.argv', ['main.py']):
            args = parse_arguments()
            
            assert args.width == 25
            assert args.height == 25
            assert args.algorithm == "bfs"
            assert args.visualize == False
            assert args.random_positions == False
    
    def test_parse_arguments_custom(self):
        """Test argument parsing with custom values"""
        test_args = [
            'main.py', 
            '--width', '15',
            '--height', '20', 
            '--algorithm', 'dijkstra',
            '--visualize',
            '--random-positions'
        ]
        
        with mock.patch('sys.argv', test_args):
            args = parse_arguments()
            
            assert args.width == 15
            assert args.height == 20
            assert args.algorithm == "dijkstra"
            assert args.visualize == True
            assert args.random_positions == True
    
    def test_parse_arguments_validation(self):
        """Test argument validation"""
        # Test invalid algorithm
        with mock.patch('sys.argv', ['main.py', '--algorithm', 'invalid']):
            with pytest.raises(SystemExit):
                parse_arguments()
        
        # Test invalid dimensions
        with mock.patch('sys.argv', ['main.py', '--width', '0']):
            with pytest.raises(SystemExit):
                parse_arguments()
                
        with mock.patch('sys.argv', ['main.py', '--height', '-5']):
            with pytest.raises(SystemExit):
                parse_arguments()
    
    def test_create_and_solve_maze_basic(self):
        """Test basic maze creation and solving"""
        result = create_and_solve_maze(
            width=5, 
            height=5, 
            algorithm='bfs',
            visualize=False,
            random_positions=False
        )
        
        assert 'maze_generator' in result
        assert 'maze_solver' in result
        assert 'path' in result
        assert 'visited' in result
        assert 'start' in result
        assert 'end' in result
        
        # Basic sanity checks
        assert isinstance(result['path'], list)
        assert isinstance(result['visited'], set)
        assert isinstance(result['start'], tuple)
        assert isinstance(result['end'], tuple)
        assert len(result['start']) == 2
        assert len(result['end']) == 2
    
    def test_create_and_solve_maze_all_algorithms(self):
        """Test maze solving with all algorithms"""
        algorithms = ['bfs', 'dfs', 'dijkstra']
        
        for algorithm in algorithms:
            result = create_and_solve_maze(
                width=7,
                height=7,
                algorithm=algorithm,
                visualize=False,
                random_positions=False
            )
            
            assert result is not None, f"Failed to solve with {algorithm}"
            assert 'path' in result
            
            # Should find a path (assuming maze is solvable)
            if len(result['path']) > 0:
                assert result['path'][0] == result['start']
                assert result['path'][-1] == result['end']
    
    def test_create_and_solve_maze_random_positions(self):
        """Test maze creation with random start/end positions"""
        result1 = create_and_solve_maze(
            width=15,
            height=15,
            algorithm='bfs',
            visualize=False,
            random_positions=True
        )
        
        result2 = create_and_solve_maze(
            width=15,
            height=15,
            algorithm='bfs',
            visualize=False,
            random_positions=True
        )
        
        # Should have valid positions
        assert result1['start'] != result1['end']
        assert result2['start'] != result2['end']
        
        # Random positions should be different between runs (highly likely)
        # Note: This could theoretically fail due to randomness, but very unlikely
        positions_different = (
            result1['start'] != result2['start'] or 
            result1['end'] != result2['end']
        )
        assert positions_different, "Random positions should vary between runs"
    
    @mock.patch('maze_visualizer.MazeVisualizer')
    def test_create_and_solve_maze_with_visualization(self, mock_visualizer_class):
        """Test maze solving with visualization enabled"""
        mock_visualizer = mock_visualizer_class.return_value
        mock_visualizer.run.return_value = None
        
        result = create_and_solve_maze(
            width=10,
            height=10,
            algorithm='bfs',
            visualize=True,
            random_positions=False
        )
        
        # Should still return result
        assert result is not None
        assert 'path' in result
        
        # Visualizer should have been created and run
        mock_visualizer_class.assert_called_once()
        mock_visualizer.run.assert_called_once()
    
    def test_main_function_integration(self):
        """Test main function integration"""
        test_args = [
            'main.py',
            '--width', '7',
            '--height', '7', 
            '--algorithm', 'bfs'
        ]
        
        with mock.patch('sys.argv', test_args):
            with mock.patch('builtins.print') as mock_print:
                main()
                
                # Should have printed some output
                assert mock_print.called
                
                # Check that useful information was printed
                printed_output = ' '.join([str(call.args[0]) for call in mock_print.call_args_list])
                assert any(keyword in printed_output.lower() for keyword in ['maze', 'path', 'time', 'solution'])

class TestDemoIntegration:
    """Test demo.py functionality"""
    
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    def test_demo_basic_execution(self, mock_print, mock_input):
        """Test demo runs without errors"""
        # Mock user inputs
        mock_input.side_effect = [
            '5',   # width
            '5',   # height
            '1',   # algorithm choice (BFS)
            'n',   # visualize
            'n',   # random positions
            'n'    # continue
        ]
        
        try:
            demo_main()
            success = True
        except SystemExit:
            success = True  # Expected for demo exit
        except Exception as e:
            success = False
            pytest.fail(f"Demo failed with exception: {e}")
        
        # Should have printed something
        assert mock_print.called
    
    @mock.patch('builtins.input')
    @mock.patch('maze_visualizer.MazeVisualizer')
    def test_demo_with_visualization(self, mock_visualizer_class, mock_input):
        """Test demo with visualization option"""
        mock_visualizer = mock_visualizer_class.return_value
        mock_visualizer.run.return_value = None
        
        mock_input.side_effect = [
            '7',   # width
            '7',   # height
            '2',   # algorithm choice (DFS)
            'y',   # visualize
            'y',   # random positions
            'n'    # continue
        ]
        
        try:
            demo_main()
        except SystemExit:
            pass  # Expected
        
        # Should have created visualizer
        mock_visualizer_class.assert_called()
    
    @mock.patch('builtins.input')
    def test_demo_invalid_inputs(self, mock_input):
        """Test demo handles invalid inputs gracefully"""
        mock_input.side_effect = [
            'invalid',  # Invalid width
            '10',       # Valid width
            'abc',      # Invalid height
            '10',       # Valid height
            '5',        # Invalid algorithm choice
            '1',        # Valid algorithm choice (BFS)
            'maybe',    # Invalid visualization choice
            'n',        # Valid visualization choice
            'n',        # Random positions
            'n'         # Continue
        ]
        
        try:
            demo_main()
            success = True
        except SystemExit:
            success = True  # Expected for demo exit
        except Exception as e:
            success = False
            pytest.fail(f"Demo should handle invalid inputs gracefully: {e}")
        
        assert success

class TestSystemIntegration:
    """Test overall system integration"""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Create maze
        generator = MazeGenerator(11, 11)
        maze = generator.generate_maze()
        
        # Solve with multiple algorithms
        algorithms = [Algorithm.BFS, Algorithm.DFS, Algorithm.DIJKSTRA]
        
        for algorithm in algorithms:
            solver = MazeSolver(maze, algorithm)
            path, visited = solver.solve((1, 1), (9, 9))
            
            # Basic validation
            assert isinstance(path, list)
            assert isinstance(visited, set)
            
            if len(path) > 0:  # If path found
                assert path[0] == (1, 1)
                assert path[-1] == (9, 9)
                assert all(pos in visited for pos in path)
    
    def test_different_maze_sizes(self):
        """Test system with different maze sizes"""
        sizes = [(5, 5), (15, 10), (21, 21), (3, 7)]
        
        for width, height in sizes:
            # Generate maze
            generator = MazeGenerator(width, height)
            maze = generator.generate_maze()
            
            # Solve with BFS
            solver = MazeSolver(maze, Algorithm.BFS)
            start = (1, 1) if width > 1 and height > 1 else (0, 0)
            end_x = min(width - 2, width - 1) if width > 2 else width - 1
            end_y = min(height - 2, height - 1) if height > 2 else height - 1
            end = (end_x, end_y)
            
            if start != end:  # Only test if start and end are different
                path, visited = solver.solve(start, end)
                
                # Basic validation
                assert isinstance(path, list)
                assert isinstance(visited, set)
                assert len(visited) > 0  # Should visit at least start position
    
    def test_memory_and_performance_basic(self):
        """Basic performance and memory test"""
        import time
        import gc
        
        # Test with moderately large maze
        width, height = 25, 25
        
        # Measure memory before
        gc.collect()
        
        start_time = time.time()
        
        # Generate and solve maze
        generator = MazeGenerator(width, height)
        maze = generator.generate_maze()
        solver = MazeSolver(maze, Algorithm.BFS)
        path, visited = solver.solve((1, 1), (width-2, height-2))
        
        end_time = time.time()
        
        # Basic performance check (should complete in reasonable time)
        execution_time = end_time - start_time
        assert execution_time < 10, f"Execution took too long: {execution_time:.2f}s"
        
        # Memory cleanup
        del generator, maze, solver, path, visited
        gc.collect()
    
    def test_error_handling_integration(self):
        """Test error handling in integrated workflow"""
        # Test with invalid maze structure
        invalid_maze = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # All walls
        
        solver = MazeSolver(invalid_maze, Algorithm.BFS)
        path, visited = solver.solve((1, 1), (1, 1))  # Same start and end
        
        # Should handle gracefully
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        # Test with out-of-bounds positions
        generator = MazeGenerator(5, 5)
        maze = generator.generate_maze()
        solver = MazeSolver(maze, Algorithm.BFS)
        
        # Out-of-bounds end position
        path, visited = solver.solve((1, 1), (10, 10))
        assert len(path) == 0  # Should return empty path
        
        # Out-of-bounds start position
        path, visited = solver.solve((-1, -1), (3, 3))
        assert len(path) == 0  # Should return empty path

class TestConfigurationAndSettings:
    """Test various configuration options"""
    
    def test_all_algorithm_combinations(self):
        """Test all valid algorithm combinations"""
        algorithms = ['bfs', 'dfs', 'dijkstra']
        sizes = [(7, 7), (11, 11)]
        
        for algorithm in algorithms:
            for width, height in sizes:
                result = create_and_solve_maze(
                    width=width,
                    height=height,
                    algorithm=algorithm,
                    visualize=False,
                    random_positions=False
                )
                
                assert result is not None
                assert 'maze_solver' in result
                
                # Check algorithm was set correctly
                expected_algorithm = {
                    'bfs': Algorithm.BFS,
                    'dfs': Algorithm.DFS,
                    'dijkstra': Algorithm.DIJKSTRA
                }[algorithm]
                
                assert result['maze_solver'].algorithm == expected_algorithm
    
    def test_edge_case_dimensions(self):
        """Test edge case maze dimensions"""
        edge_cases = [
            (3, 3),    # Minimum practical size
            (51, 51),  # Large odd size
            (5, 15),   # Rectangular
            (15, 5),   # Rectangular other direction
        ]
        
        for width, height in edge_cases:
            result = create_and_solve_maze(
                width=width,
                height=height,
                algorithm='bfs',
                visualize=False,
                random_positions=False
            )
            
            assert result is not None
            assert result['maze_generator'].width == width
            assert result['maze_generator'].height == height
    
    def test_configuration_persistence(self):
        """Test that configuration is maintained throughout execution"""
        width, height = 13, 17
        algorithm = 'dijkstra'
        
        result = create_and_solve_maze(
            width=width,
            height=height,
            algorithm=algorithm,
            visualize=False,
            random_positions=True
        )
        
        # Configuration should be preserved
        assert result['maze_generator'].width == width
        assert result['maze_generator'].height == height
        assert result['maze_solver'].algorithm == Algorithm.DIJKSTRA
        
        # Start and end should be valid positions within maze
        start_x, start_y = result['start']
        end_x, end_y = result['end']
        
        assert 0 <= start_x < width
        assert 0 <= start_y < height
        assert 0 <= end_x < width
        assert 0 <= end_y < height

if __name__ == "__main__":
    pytest.main([__file__])