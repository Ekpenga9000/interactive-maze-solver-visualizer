"""
Tests for Maze Generator
Comprehensive testing of maze generation functionality
"""
import pytest
from maze_generator import MazeGenerator


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
        maze = generator.generate()
        assert len(maze) == 3
        assert len(maze[0]) == 3


class TestMazeGeneration:
    """Test maze generation algorithm"""
    
    def test_generate_returns_2d_list(self, small_maze_generator):
        """Test that generate() returns a 2D list"""
        maze = small_maze_generator.generate()
        assert isinstance(maze, list)
        assert all(isinstance(row, list) for row in maze)
        
    def test_generate_correct_dimensions(self, small_maze_generator):
        """Test generated maze has correct dimensions"""
        maze = small_maze_generator.generate()
        assert len(maze) == small_maze_generator.height
        assert len(maze[0]) == small_maze_generator.width
        assert all(len(row) == small_maze_generator.width for row in maze)
        
    def test_generate_contains_only_valid_values(self, small_maze_generator):
        """Test generated maze contains only 0s and 1s"""
        maze = small_maze_generator.generate()
        for row in maze:
            for cell in row:
                assert cell in [0, 1], f"Invalid cell value: {cell}"
                
    def test_generate_has_border_walls(self, small_maze_generator):
        """Test generated maze has walls around the border"""
        maze = small_maze_generator.generate()
        height, width = len(maze), len(maze[0])
        
        # Top and bottom borders
        assert all(maze[0][x] == 1 for x in range(width))
        assert all(maze[height-1][x] == 1 for x in range(width))
        
        # Left and right borders
        assert all(maze[y][0] == 1 for y in range(height))
        assert all(maze[y][width-1] == 1 for y in range(height))
        
    def test_start_position_is_clear(self, small_maze_generator):
        """Test start position is not a wall"""
        maze = small_maze_generator.generate()
        start_x, start_y = small_maze_generator.get_start_position()
        assert maze[start_y][start_x] == 0
        
    def test_end_position_is_clear(self, small_maze_generator):
        """Test end position is not a wall"""
        maze = small_maze_generator.generate()
        end_x, end_y = small_maze_generator.get_end_position()
        assert maze[end_y][end_x] == 0
        
    def test_multiple_generations_are_different(self, medium_maze_generator):
        """Test that multiple generations produce different mazes"""
        # Generate multiple mazes using different generator instances
        mazes = []
        for i in range(5):
            generator = MazeGenerator(11, 11)  # Create new generator each time
            maze = generator.generate()
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
    
    def test_get_start_position_valid(self, small_maze_generator):
        """Test get_start_position returns valid coordinates"""
        start_x, start_y = small_maze_generator.get_start_position()
        assert isinstance(start_x, int)
        assert isinstance(start_y, int)
        assert 0 <= start_x < small_maze_generator.width
        assert 0 <= start_y < small_maze_generator.height
        
    def test_get_end_position_valid(self, small_maze_generator):
        """Test get_end_position returns valid coordinates"""
        end_x, end_y = small_maze_generator.get_end_position()
        assert isinstance(end_x, int)
        assert isinstance(end_y, int)
        assert 0 <= end_x < small_maze_generator.width
        assert 0 <= end_y < small_maze_generator.height
        
    def test_start_end_positions_different(self, medium_maze_generator):
        """Test start and end positions are different"""
        start_pos = medium_maze_generator.get_start_position()
        end_pos = medium_maze_generator.get_end_position()
        assert start_pos != end_pos
        
    def test_start_position_consistency(self, small_maze_generator):
        """Test start position is consistent"""
        pos1 = small_maze_generator.get_start_position()
        pos2 = small_maze_generator.get_start_position()
        assert pos1 == pos2
        
    def test_end_position_consistency(self, small_maze_generator):
        """Test end position is consistent"""
        pos1 = small_maze_generator.get_end_position()
        pos2 = small_maze_generator.get_end_position()
        assert pos1 == pos2


class TestMazeSizes:
    """Test maze generation with different sizes"""
    
    @pytest.mark.parametrize("width,height", [
        (5, 5), (11, 7), (21, 15), (31, 21), (41, 31)
    ])
    def test_various_maze_sizes(self, width, height):
        """Test maze generation with various sizes"""
        generator = MazeGenerator(width, height)
        maze = generator.generate()
        
        assert len(maze) == height
        assert len(maze[0]) == width
        assert all(len(row) == width for row in maze)
        
        # Test start and end positions are valid
        start_x, start_y = generator.get_start_position()
        end_x, end_y = generator.get_end_position()
        
        assert 0 <= start_x < width
        assert 0 <= start_y < height
        assert 0 <= end_x < width
        assert 0 <= end_y < height
        
        # Test positions are clear
        assert maze[start_y][start_x] == 0
        assert maze[end_y][end_x] == 0


class TestMazeProperties:
    """Test maze structural properties"""
    
    def test_maze_has_paths(self, medium_maze_generator):
        """Test generated maze has some open paths"""
        maze = medium_maze_generator.generate()
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
        
    def test_maze_connectivity_basic(self, small_maze_generator):
        """Basic test that start can potentially reach end"""
        maze = small_maze_generator.generate()
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


class TestMazeEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_very_small_maze(self):
        """Test with very small maze dimensions"""
        generator = MazeGenerator(3, 3)
        maze = generator.generate()
        
        # Should still generate a valid maze
        assert len(maze) == 3
        assert len(maze[0]) == 3
        assert maze[1][1] == 0  # Start position should be clear
        
    def test_rectangular_mazes(self):
        """Test with non-square mazes"""
        # Wide maze
        generator_wide = MazeGenerator(21, 11)
        maze_wide = generator_wide.generate()
        assert len(maze_wide) == 11
        assert len(maze_wide[0]) == 21
        
        # Tall maze
        generator_tall = MazeGenerator(11, 21)
        maze_tall = generator_tall.generate()
        assert len(maze_tall) == 21
        assert len(maze_tall[0]) == 11
        
    def test_regeneration_works(self, medium_maze_generator):
        """Test that regenerating mazes works correctly"""
        maze1 = medium_maze_generator.generate()
        maze2 = medium_maze_generator.generate()
        maze3 = medium_maze_generator.generate()
        
        # All mazes should have same dimensions
        assert len(maze1) == len(maze2) == len(maze3)
        assert len(maze1[0]) == len(maze2[0]) == len(maze3[0])
        
        # Start and end positions should be consistent
        start1 = medium_maze_generator.get_start_position()
        start2 = medium_maze_generator.get_start_position()
        assert start1 == start2