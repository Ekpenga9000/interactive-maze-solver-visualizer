"""
Base Algorithm class for maze solving
Defines the interface that all pathfinding algorithms must implement
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Set, Generator, Dict, Any

class BaseAlgorithm(ABC):
    """Abstract base class for maze solving algorithms"""
    
    def __init__(self, maze: List[List[int]]):
        """
        Initialize the algorithm with a maze
        
        Args:
            maze: 2D list representing the maze (0 = path, 1 = wall)
        """
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get valid neighboring cells
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of valid neighbor coordinates
        """
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check bounds and if cell is not a wall
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and 
                self.maze[new_y][new_x] == 0):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    @abstractmethod
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Solve the maze from start to end
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Returns:
            Tuple of (path, visited_cells)
        """
        pass
    
    @abstractmethod
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int]) -> Generator[Dict[str, Any], None, None]:
        """
        Solve the maze with animation steps
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Yields:
            Dictionary containing current state information for animation
        """
        pass
    
    def reconstruct_path(self, parent: Dict[Tuple[int, int], Tuple[int, int]], 
                        start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from parent dictionary
        
        Args:
            parent: Dictionary mapping each cell to its parent
            start: Starting position
            end: Ending position
            
        Returns:
            List of coordinates representing the path
        """
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path