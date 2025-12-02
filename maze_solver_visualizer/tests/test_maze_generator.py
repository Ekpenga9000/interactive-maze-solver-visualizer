"""
Tests for Maze Generator
Comprehensive testing of maze generation functionality
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_generator import MazeGenerator

# Test fixtures
def create_small_maze_generator():
    """Create a small maze generator for testing"""
    return MazeGenerator(5, 5)

def create_medium_maze_generator():
    """Create a medium maze generator for testing"""
    return MazeGenerator(11, 9)

def create_large_maze_generator():
    """Create a large maze generator for testing"""
    return MazeGenerator(21, 15)

class TestMazeGeneratorBasic:
    """Test basic maze generator functionality"""
    
    def test_maze_generator_initialization(self):
        """Test maze generator can be initialized with valid dimensions"""
        generator = MazeGenerator(11, 9)
        assert generator.width == 11
        assert generator.height == 9
        
    def test_maze_generator_invalid_dimensions(self):
        """Test maze generator handles invalid dimensions"""
        # Even dimensions should still work but may not be optimal
        generator = MazeGenerator(10, 8)
        assert generator.width == 10
        assert generator.height == 8
        
    def test_maze_generator_minimum_size(self):
        """Test maze generator with minimum valid size"""
        generator = MazeGenerator(3, 3)
        maze = generator.generate_legacy_maze()
        assert len(maze) == 3
        assert len(maze[0]) == 3

class TestMazeGeneration:
    """Test maze generation algorithm"""
    
    def test_generate_returns_2d_list(self):
        """Test that generate_legacy_maze() returns a 2D list"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        assert isinstance(maze, list)
        assert all(isinstance(row, list) for row in maze)
        
    def test_generate_correct_dimensions(self):
        """Test generated maze has correct dimensions"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        assert len(maze) == small_maze_generator.height
        assert len(maze[0]) == small_maze_generator.width
        assert all(len(row) == small_maze_generator.width for row in maze)
        
    def test_generate_contains_only_valid_values(self):
        """Test generated maze contains only 0s and 1s"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        for row in maze:
            for cell in row:
                assert cell in [0, 1], f"Invalid cell value: {cell}"
                
    def test_generate_has_border_walls(self):
        """Test generated maze has walls around the border"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        height, width = len(maze), len(maze[0])
        
        # Top and bottom borders
        assert all(maze[0][x] == 1 for x in range(width))
        assert all(maze[height-1][x] == 1 for x in range(width))
        
        # Left and right borders
        assert all(maze[y][0] == 1 for y in range(height))
        assert all(maze[y][width-1] == 1 for y in range(height))
        
    def test_start_position_is_clear(self):
        """Test start position is not a wall"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        start_x, start_y = small_maze_generator.get_start_position()
        assert maze[start_y][start_x] == 0
        
    def test_end_position_is_clear(self):
        """Test end position is not a wall"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        end_x, end_y = small_maze_generator.get_end_position()
        assert maze[end_y][end_x] == 0
        
    def test_multiple_generations_are_different(self):
        """Test that multiple generations produce different mazes"""
        # Generate multiple mazes using different generator instances
        mazes = []
        for i in range(5):
            generator = MazeGenerator(11, 11)  # Create new generator each time
            maze = generator.generate_legacy_maze()
            mazes.append(maze)
        
        # Check that at least some mazes are different
        unique_mazes = set()
        for maze in mazes:
            # Convert maze to tuple for hashability
            maze_tuple = tuple(tuple(row) for row in maze)
            unique_mazes.add(maze_tuple)
        
        # Should have at least 2 different mazes out of 5
        assert len(unique_mazes) >= 2, "All generated mazes are identical (very unlikely)"

class TestMazeStartEnd:
    """Test start and end position functionality"""
    
    def test_get_start_position_valid(self):
        """Test get_start_position returns valid coordinates"""
        small_maze_generator = create_small_maze_generator()
        start_x, start_y = small_maze_generator.get_start_position()
        assert isinstance(start_x, int)
        assert isinstance(start_y, int)
        assert 0 <= start_x < small_maze_generator.width
        assert 0 <= start_y < small_maze_generator.height
        
    def test_get_end_position_valid(self):
        """Test get_end_position returns valid coordinates"""
        small_maze_generator = create_small_maze_generator()
        end_x, end_y = small_maze_generator.get_end_position()
        assert isinstance(end_x, int)
        assert isinstance(end_y, int)
        assert 0 <= end_x < small_maze_generator.width
        assert 0 <= end_y < small_maze_generator.height
        
    def test_start_end_positions_different(self):
        """Test start and end positions are different"""
        medium_maze_generator = create_medium_maze_generator()
        start_pos = medium_maze_generator.get_start_position()
        end_pos = medium_maze_generator.get_end_position()
        assert start_pos != end_pos
        
    def test_start_position_consistency(self):
        """Test start position is consistent"""
        small_maze_generator = create_small_maze_generator()
        pos1 = small_maze_generator.get_start_position()
        pos2 = small_maze_generator.get_start_position()
        assert pos1 == pos2
        
    def test_end_position_consistency(self):
        """Test end position is consistent"""
        small_maze_generator = create_small_maze_generator()
        pos1 = small_maze_generator.get_end_position()
        pos2 = small_maze_generator.get_end_position()
        assert pos1 == pos2

class TestMazeSizes:
    """Test maze generation with different sizes"""
    
    def test_various_maze_sizes(self):
        """Test maze generation with various sizes"""
        test_dimensions = [
            (5, 5), (11, 7), (21, 15), (31, 21), (15, 11)
        ]
        
        for width, height in test_dimensions:
            generator = MazeGenerator(width, height)
            maze = generator.generate_legacy_maze()
            
            assert len(maze) == height, f"Height mismatch for {width}x{height}"
            assert len(maze[0]) == width, f"Width mismatch for {width}x{height}"
            assert all(len(row) == width for row in maze), f"Row width inconsistent for {width}x{height}"
            
            # Test start and end positions are valid
            start_x, start_y = generator.get_start_position()
            end_x, end_y = generator.get_end_position()
            
            assert 0 <= start_x < width, f"Invalid start_x for {width}x{height}"
            assert 0 <= start_y < height, f"Invalid start_y for {width}x{height}"
            assert 0 <= end_x < width, f"Invalid end_x for {width}x{height}"
            assert 0 <= end_y < height, f"Invalid end_y for {width}x{height}"
            
            # Test positions are clear
            assert maze[start_y][start_x] == 0, f"Start position blocked for {width}x{height}"
            assert maze[end_y][end_x] == 0, f"End position blocked for {width}x{height}"
    
    def test_small_maze_sizes(self):
        """Test with very small maze dimensions"""
        small_sizes = [(3, 3), (5, 3), (3, 5), (7, 5)]
        
        for width, height in small_sizes:
            generator = MazeGenerator(width, height)
            maze = generator.generate_legacy_maze()
            
            assert len(maze) == height
            assert len(maze[0]) == width
            
            # Should have valid start/end even for small mazes
            start_x, start_y = generator.get_start_position()
            end_x, end_y = generator.get_end_position()
            
            assert maze[start_y][start_x] == 0
            assert maze[end_y][end_x] == 0

class TestMazeProperties:
    """Test maze structural properties"""
    
    def test_maze_has_paths(self):
        """Test generated maze has some open paths"""
        medium_maze_generator = create_medium_maze_generator()
        maze = medium_maze_generator.generate_legacy_maze()
        open_cells = sum(
            1 for row in maze
            for cell in row
            if cell == 0
        )
        total_cells = len(maze) * len(maze[0])
        
        # At least some cells should be open paths
        assert open_cells > 0
        # But not all cells (there should be some walls)
        assert open_cells < total_cells
        
    def test_maze_connectivity_basic(self):
        """Basic test that start can potentially reach end"""
        small_maze_generator = create_small_maze_generator()
        maze = small_maze_generator.generate_legacy_maze()
        start_x, start_y = small_maze_generator.get_start_position()
        end_x, end_y = small_maze_generator.get_end_position()
        
        # This is a basic structural test - actual pathfinding tested in solver tests
        assert maze[start_y][start_x] == 0
        assert maze[end_y][end_x] == 0
        
        # There should be at least one path cell adjacent to start
        adjacent_cells = [
            (start_x + dx, start_y + dy)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if (0 <= start_x + dx < len(maze[0]) and 
                0 <= start_y + dy < len(maze))
        ]
        
        has_adjacent_path = any(
            maze[y][x] == 0
            for x, y in adjacent_cells
        )
        assert has_adjacent_path, "Start position has no adjacent path cells"
    
    def test_maze_border_consistency(self):
        """Test maze borders are consistently walls"""
        sizes_to_test = [(7, 7), (11, 9), (15, 13)]
        
        for width, height in sizes_to_test:
            generator = MazeGenerator(width, height)
            maze = generator.generate_legacy_maze()
            
            # Check all border cells are walls
            for x in range(width):
                assert maze[0][x] == 1, f"Top border not wall at ({x}, 0)"
                assert maze[height-1][x] == 1, f"Bottom border not wall at ({x}, {height-1})"
            
            for y in range(height):
                assert maze[y][0] == 1, f"Left border not wall at (0, {y})"
                assert maze[y][width-1] == 1, f"Right border not wall at ({width-1}, {y})"

class TestMazeEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_very_small_maze(self):
        """Test with very small maze dimensions"""
        generator = MazeGenerator(3, 3)
        maze = generator.generate_legacy_maze()
        
        # Should still generate a valid maze
        assert len(maze) == 3
        assert len(maze[0]) == 3
        assert maze[1][1] == 0  # Center position should be clear (likely start)
        
    def test_rectangular_mazes(self):
        """Test with non-square mazes"""
        # Wide maze
        generator_wide = MazeGenerator(21, 11)
        maze_wide = generator_wide.generate_legacy_maze()
        assert len(maze_wide) == 11
        assert len(maze_wide[0]) == 21
        
        # Tall maze
        generator_tall = MazeGenerator(11, 21)
        maze_tall = generator_tall.generate_legacy_maze()
        assert len(maze_tall) == 21
        assert len(maze_tall[0]) == 11
        
    def test_regeneration_works(self):
        """Test that regenerating mazes works correctly"""
        medium_maze_generator = create_medium_maze_generator()
        maze1 = medium_maze_generator.generate_legacy_maze()
        maze2 = medium_maze_generator.generate_legacy_maze()
        maze3 = medium_maze_generator.generate_legacy_maze()
        
        # All mazes should have same dimensions
        assert len(maze1) == len(maze2) == len(maze3)
        assert len(maze1[0]) == len(maze2[0]) == len(maze3[0])
        
        # Start and end positions should be consistent
        start1 = medium_maze_generator.get_start_position()
        start2 = medium_maze_generator.get_start_position()
        assert start1 == start2
        
    def test_maze_generation_deterministic(self):
        """Test maze generation consistency"""
        # Create multiple generators with same dimensions
        generators = [MazeGenerator(9, 7) for _ in range(3)]
        
        for generator in generators:
            maze = generator.generate_legacy_maze()
            
            # Basic structural tests
            assert len(maze) == 7
            assert len(maze[0]) == 9
            
            start_x, start_y = generator.get_start_position()
            end_x, end_y = generator.get_end_position()
            
            assert maze[start_y][start_x] == 0
            assert maze[end_y][end_x] == 0
            
            # Start and end should be different
            assert (start_x, start_y) != (end_x, end_y)
    
    def test_maze_even_dimensions(self):
        """Test maze generation with even dimensions"""
        even_sizes = [(8, 6), (10, 8), (12, 10)]
        
        for width, height in even_sizes:
            generator = MazeGenerator(width, height)
            maze = generator.generate_legacy_maze()
            
            # Should still generate valid maze structure
            assert len(maze) == height
            assert len(maze[0]) == width
            
            # Should have borders
            assert all(maze[0][x] == 1 for x in range(width))
            assert all(maze[height-1][x] == 1 for x in range(width))
            assert all(maze[y][0] == 1 for y in range(height))
            assert all(maze[y][width-1] == 1 for y in range(height))

class TestMazePerformance:
    """Test maze generation performance and scalability"""
    
    def test_large_maze_generation(self):
        """Test generation of large mazes"""
        large_sizes = [(51, 41), (71, 51), (31, 71)]
        
        for width, height in large_sizes:
            generator = MazeGenerator(width, height)
            maze = generator.generate_legacy_maze()
            
            # Should complete without errors
            assert len(maze) == height
            assert len(maze[0]) == width
            
            # Should have proper start/end positions
            start_x, start_y = generator.get_start_position()
            end_x, end_y = generator.get_end_position()
            
            assert 0 <= start_x < width
            assert 0 <= start_y < height
            assert 0 <= end_x < width 
            assert 0 <= end_y < height
            
            assert maze[start_y][start_x] == 0
            assert maze[end_y][end_x] == 0

def run_all_tests():
    """Run all maze generator tests"""
    test_classes = [
        TestMazeGeneratorBasic,
        TestMazeGeneration,
        TestMazeStartEnd,
        TestMazeSizes,
        TestMazeProperties,
        TestMazeEdgeCases,
        TestMazePerformance
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running Maze Generator tests...")
    
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