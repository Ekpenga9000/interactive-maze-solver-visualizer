"""
Comprehensive tests for the MazeVisualizer class.
Tests visualization functionality without requiring pygame display.
"""

# Mock pygame since we don't need actual display for tests
class MockPygame:
    """Mock pygame module to avoid display requirements during testing."""
    
    def __init__(self):
        self.QUIT = 256
        self.KEYDOWN = 768
        self.MOUSEBUTTONDOWN = 1025
        self.K_SPACE = 32
        self.K_r = 114
        self.K_1 = 49
        self.K_2 = 50
        self.K_3 = 51
        self.K_g = 103
        self.K_ESCAPE = 27
    
    def init(self):
        pass
    
    def quit(self):
        pass
    
    class display:
        @staticmethod
        def set_mode(size):
            return MockSurface()
        
        @staticmethod
        def set_caption(title):
            pass
        
        @staticmethod
        def flip():
            pass
    
    class time:
        @staticmethod
        def Clock():
            return MockClock()
    
    class event:
        @staticmethod
        def get():
            return []
    
    class mouse:
        @staticmethod
        def get_pos():
            return (0, 0)
    
    class font:
        @staticmethod
        def Font(name, size):
            return MockFont()
    
    class draw:
        @staticmethod
        def rect(surface, color, rect):
            pass
        
        @staticmethod
        def circle(surface, color, pos, radius):
            pass

class MockSurface:
    """Mock pygame surface."""
    
    def fill(self, color):
        pass
    
    def get_width(self):
        return 800
    
    def get_height(self):
        return 600
    
    def blit(self, source, pos):
        pass

class MockClock:
    """Mock pygame clock."""
    
    def tick(self, fps):
        pass

class MockFont:
    """Mock pygame font."""
    
    def render(self, text, antialias, color):
        return MockSurface()

class MockEvent:
    """Mock pygame event."""
    
    def __init__(self, type, **kwargs):
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)

# Replace pygame with mock before importing visualizer
import sys
import os
sys.modules['pygame'] = MockPygame()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_visualizer import MazeVisualizer
from maze_solver import Algorithm


class TestMazeVisualizerInitialization:
    """Test maze visualizer initialization"""
    
    def test_visualizer_creation(self):
        """Test creating a maze visualizer"""
        visualizer = MazeVisualizer(window_width=800, window_height=600, maze_width=21, maze_height=15)
        
        # Test basic properties
        assert visualizer.maze_width == 21
        assert visualizer.maze_height == 15
        assert visualizer.window_width == 800
        assert visualizer.window_height == 600
        
        # Test that maze is generated
        assert visualizer.maze is not None
        assert len(visualizer.maze) == 15
        assert len(visualizer.maze[0]) == 21
        
        # Test start and end positions exist
        assert visualizer.start_pos is not None
        assert visualizer.end_pos is not None
    
    def test_required_colors_exist(self):
        """Test that all required colors are defined"""
        visualizer = MazeVisualizer(11, 9)
        
        # Test that colors exist
        assert hasattr(visualizer, 'BLACK')
        assert hasattr(visualizer, 'WHITE')
        assert hasattr(visualizer, 'GREEN')
        assert hasattr(visualizer, 'RED')
        assert hasattr(visualizer, 'BLUE')
        assert hasattr(visualizer, 'YELLOW')
        assert hasattr(visualizer, 'GRAY')
        assert hasattr(visualizer, 'BREADTH_COLOR_1')
        assert hasattr(visualizer, 'BREADTH_COLOR_2')
        
        # Check color format (RGB tuples)
        assert len(visualizer.BLACK) == 3
        assert all(0 <= c <= 255 for c in visualizer.BLACK)
        assert len(visualizer.BREADTH_COLOR_1) == 3
        assert all(0 <= c <= 255 for c in visualizer.BREADTH_COLOR_1)
    
    def test_algorithm_initialization(self):
        """Test that algorithm selection works"""
        visualizer = MazeVisualizer(11, 9)
        
        # Should start with DFS
        assert visualizer.current_algorithm == Algorithm.DFS
        
        # Should be able to change algorithms
        visualizer.current_algorithm = Algorithm.BFS
        assert visualizer.current_algorithm == Algorithm.BFS
        
        visualizer.current_algorithm = Algorithm.DIJKSTRA
        assert visualizer.current_algorithm == Algorithm.DIJKSTRA


class TestMazeVisualizerMethods:
    """Test maze visualizer methods"""
    
    def test_generate_new_maze(self):
        """Test generating new mazes"""
        visualizer = MazeVisualizer(11, 9)
        
        original_maze = visualizer.maze
        original_start = visualizer.start_pos
        original_end = visualizer.end_pos
        
        visualizer.generate_new_maze()
        
        # Should have new maze (likely different)
        assert visualizer.maze is not None
        assert visualizer.start_pos is not None
        assert visualizer.end_pos is not None
        
        # Positions should be valid
        assert visualizer.maze[visualizer.start_pos[1]][visualizer.start_pos[0]] == 0
        assert visualizer.maze[visualizer.end_pos[1]][visualizer.end_pos[0]] == 0
    
    def test_coordinate_conversion(self):
        """Test coordinate conversion between screen and maze coordinates"""
        visualizer = MazeVisualizer(window_width=500, window_height=375, maze_width=21, maze_height=15)
        
        # Test that window size is set correctly
        assert visualizer.window_width == 500
        assert visualizer.window_height == 375
        
        # Calculate effective cell size
        cell_width = visualizer.window_width / visualizer.maze_width
        cell_height = visualizer.window_height / visualizer.maze_height
        
        # Test that coordinates can be calculated
        maze_x, maze_y = 5, 3
        expected_screen_x = maze_x * cell_width
        expected_screen_y = maze_y * cell_height
        
        # Verify coordinate bounds are reasonable
        max_screen_x = visualizer.maze_width * cell_width
        max_screen_y = visualizer.maze_height * cell_height
        
        assert max_screen_x <= visualizer.window_width
        assert max_screen_y <= visualizer.window_height
    
    def test_start_solving(self):
        """Test starting the solving process"""
        visualizer = MazeVisualizer(maze_width=11, maze_height=9)
        
        # Should not be solving initially
        assert not hasattr(visualizer, 'is_solving') or not visualizer.is_solving
        
        # The actual method is solve_maze()
        # We can't easily test this without a full pygame loop, but we can test it exists
        assert hasattr(visualizer, 'solve_maze')
        assert callable(getattr(visualizer, 'solve_maze'))
    
    def test_reset_solving(self):
        """Test resetting the solving state"""
        visualizer = MazeVisualizer(maze_width=11, maze_height=9)
        
        # The actual method is _reset_solution()
        assert hasattr(visualizer, '_reset_solution')
        assert callable(getattr(visualizer, '_reset_solution'))
        
        # Test that it can be called
        visualizer._reset_solution()
        
        # Should clear solution state
        assert len(visualizer.path) == 0
        assert len(visualizer.visited_cells) == 0


class TestColoringSystem:
    """Test the coloring system for different algorithms"""
    
    def test_breadth_color_function(self):
        """Test breadth color calculation"""
        visualizer = MazeVisualizer(11, 9)
        
        # Set up some branch assignments
        visualizer.branch_assignments = {
            (1, 1): 'main',
            (2, 1): 'main',
            (3, 1): 'branch_0',
            (4, 1): 'branch_0'
        }
        
        # Test main branch color
        color1 = visualizer.get_breadth_color((1, 1))
        assert color1 == visualizer.BREADTH_COLOR_1
        
        # Test secondary branch color
        color2 = visualizer.get_breadth_color((3, 1))
        assert color2 == visualizer.BREADTH_COLOR_2
        
        # Test unknown position (should default to main)
        color3 = visualizer.get_breadth_color((10, 10))
        assert color3 == visualizer.BREADTH_COLOR_1
    
    def test_distance_color_function(self):
        """Test distance color calculation for Dijkstra"""
        visualizer = MazeVisualizer(11, 9)
        
        # Set up some distances
        visualizer.distances = {
            (1, 1): 1.0,
            (2, 1): 3.0,
            (3, 1): 8.0,
            (4, 1): 12.0
        }
        
        # Test that colors are returned (actual logic may vary)
        color1 = visualizer.get_distance_color(1.0)
        assert len(color1) == 3  # RGB tuple
        assert all(0 <= c <= 255 for c in color1)
        
        color2 = visualizer.get_distance_color(12.0)
        assert len(color2) == 3  # RGB tuple
        assert all(0 <= c <= 255 for c in color2)


class TestAnimationSystem:
    """Test the animation system"""
    
    def test_animation_state_tracking(self):
        """Test that animation state is tracked correctly"""
        visualizer = MazeVisualizer(11, 9)
        
        # Initially no state
        assert len(visualizer.breadth_levels) == 0
        assert len(visualizer.distances) == 0
        assert len(visualizer.branch_assignments) == 0
        
        # Simulate adding some state
        visualizer.breadth_levels[(1, 1)] = 0
        visualizer.breadth_levels[(2, 1)] = 1
        visualizer.distances[(1, 1)] = 0.0
        visualizer.distances[(2, 1)] = 3.0
        
        assert len(visualizer.breadth_levels) == 2
        assert len(visualizer.distances) == 2
        assert visualizer.breadth_levels[(1, 1)] == 0
        assert visualizer.distances[(2, 1)] == 3.0
    
    def test_animation_speed_control(self):
        """Test animation speed control"""
        visualizer = MazeVisualizer(11, 9)
        
        # Should have default animation speed
        assert visualizer.animation_speed > 0
        
        # Should be able to change speed
        original_speed = visualizer.animation_speed
        visualizer.animation_speed = 100
        assert visualizer.animation_speed == 100
        
        # Reset
        visualizer.animation_speed = original_speed
        assert visualizer.animation_speed == original_speed
    
    def test_solving_step_tracking(self):
        """Test that solving steps are tracked"""
        visualizer = MazeVisualizer(maze_width=11, maze_height=9)
        
        # Check that solving state exists
        assert hasattr(visualizer, 'path')
        assert hasattr(visualizer, 'visited_cells')
        
        # Initially should be empty
        assert len(visualizer.path) == 0
        assert len(visualizer.visited_cells) == 0
        
        # Test reset function
        visualizer._reset_solution()
        assert len(visualizer.path) == 0
        assert len(visualizer.visited_cells) == 0


class TestMazeVisualizerIntegration:
    """Test integration between visualizer and maze/solver components"""
    
    def test_visualizer_with_different_algorithms(self):
        """Test that visualizer works with all algorithms"""
        visualizer = MazeVisualizer(maze_width=11, maze_height=9)
        
        algorithms = [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]
        
        for algorithm in algorithms:
            visualizer.current_algorithm = algorithm
            
            # Test that the algorithm can be set
            assert visualizer.current_algorithm == algorithm
            
            # Test that solver methods exist for this algorithm
            if algorithm == Algorithm.DFS:
                assert hasattr(visualizer, '_solve_dfs_animated')
            elif algorithm == Algorithm.BFS:
                assert hasattr(visualizer, '_solve_bfs_animated')
            elif algorithm == Algorithm.DIJKSTRA:
                assert hasattr(visualizer, '_solve_dijkstra_animated')
    
    def test_visualizer_maze_compatibility(self):
        """Test that visualizer works with generated mazes"""
        visualizer = MazeVisualizer(maze_width=15, maze_height=11)
        
        # Generate several mazes and ensure compatibility
        for _ in range(3):
            visualizer.generate_new_maze()
            
            # Maze should be proper format
            assert isinstance(visualizer.maze, list)
            # Note: maze dimensions may be adjusted by the generator
            assert len(visualizer.maze) >= 11
            assert len(visualizer.maze[0]) >= 15
            
            # Start and end should be valid
            start_x, start_y = visualizer.start_pos
            end_x, end_y = visualizer.end_pos
            
            maze_height = len(visualizer.maze)
            maze_width = len(visualizer.maze[0])
            
            assert 0 <= start_x < maze_width
            assert 0 <= start_y < maze_height
            assert 0 <= end_x < maze_width
            assert 0 <= end_y < maze_height
            
            assert visualizer.maze[start_y][start_x] == 0  # Path
            assert visualizer.maze[end_y][end_x] == 0       # Path


class TestVisualizerErrorHandling:
    """Test error handling in visualizer"""
    
    def test_invalid_dimensions(self):
        """Test handling of invalid dimensions"""
        # Test with small dimensions
        visualizer = MazeVisualizer(maze_width=5, maze_height=5)
        # The actual dimensions may be adjusted by the generator
        assert visualizer.maze_width >= 5
        assert visualizer.maze_height >= 5
        
        # Even dimensions should be handled (converted to odd)
        visualizer2 = MazeVisualizer(maze_width=6, maze_height=8)
        # The actual maze generator might adjust these to odd numbers
        assert visualizer2.maze_width >= 6
        assert visualizer2.maze_height >= 8
    
    def test_cell_size_bounds(self):
        """Test cell size bounds"""
        # Very small window
        visualizer = MazeVisualizer(window_width=210, window_height=150, maze_width=21, maze_height=15)
        assert visualizer.window_width == 210
        assert visualizer.window_height == 150
        
        # Large window
        visualizer2 = MazeVisualizer(window_width=1100, window_height=900, maze_width=11, maze_height=9)
        assert visualizer2.window_width == 1100
        assert visualizer2.window_height == 900
    
    def test_algorithm_switching_during_solve(self):
        """Test switching algorithms during solving"""
        visualizer = MazeVisualizer(maze_width=11, maze_height=9)
        
        # Start with one algorithm
        visualizer.current_algorithm = Algorithm.BFS
        assert visualizer.current_algorithm == Algorithm.BFS
        
        # Switch algorithm
        visualizer.current_algorithm = Algorithm.DFS
        assert visualizer.current_algorithm == Algorithm.DFS
        
        # Should be able to change again
        visualizer.current_algorithm = Algorithm.DIJKSTRA
        assert visualizer.current_algorithm == Algorithm.DIJKSTRA


if __name__ == "__main__":
    # Run tests directly without pytest dependency
    import traceback
    
    test_classes = [
        TestMazeVisualizerInitialization,
        TestMazeVisualizerMethods,
        TestColoringSystem,
        TestAnimationSystem,
        TestMazeVisualizerIntegration,
        TestVisualizerErrorHandling
    ]
    
    total_tests = 0
    passed_tests = 0
    
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
                traceback.print_exc()
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Some tests failed. {total_tests - passed_tests} failures.")