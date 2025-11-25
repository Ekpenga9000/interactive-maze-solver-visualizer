"""
Maze Generator Module
Generates random mazes using recursive backtracking algorithm.
"""

import random
from typing import List, Tuple, Set

class MazeGenerator:
    """Generates random mazes using recursive backtracking"""
    
    def __init__(self, width: int, height: int):
        """
        Initialize maze generator
        
        Args:
            width: Width of the maze (should be odd)
            height: Height of the maze (should be odd)
        """
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        
    def generate(self) -> List[List[int]]:
        """
        Generate a random maze using recursive backtracking
        
        Returns:
            2D list representing the maze (0 = path, 1 = wall)
        """
        # Start from position (1, 1)
        self._carve_path(1, 1)
        
        # Ensure start and end points are clear
        self.maze[1][1] = 0  # Start
        self.maze[self.height - 2][self.width - 2] = 0  # End
        
        return self.maze
    
    def _carve_path(self, x: int, y: int):
        """
        Recursively carve paths through the maze
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
        """
        self.maze[y][x] = 0  # Mark current cell as path
        
        # Get all possible directions (up, down, left, right)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check if new position is valid and unvisited
            if (0 < new_x < self.width - 1 and 
                0 < new_y < self.height - 1 and 
                self.maze[new_y][new_x] == 1):
                
                # Carve the wall between current and new cell
                self.maze[y + dy // 2][x + dx // 2] = 0
                
                # Recursively carve from new position
                self._carve_path(new_x, new_y)
    
    def get_start_position(self) -> Tuple[int, int]:
        """Get the start position of the maze"""
        return (1, 1)
    
    def get_end_position(self) -> Tuple[int, int]:
        """Get the end position of the maze"""
        return (self.width - 2, self.height - 2)
    
    def generate_with_positions(self) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """
        Generate a random maze and return it with start and end positions
        
        Returns:
            Tuple of (maze, start_position, end_position)
        """
        maze = self.generate()
        start = self.get_start_position()
        end = self.get_end_position()
        return maze, start, end