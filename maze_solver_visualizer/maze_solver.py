"""
Maze Solver Module
Contains the main solver class that coordinates different pathfinding algorithms
"""

from typing import List, Tuple, Set, Generator, Dict, Any
from enum import Enum
from algorithms import DepthFirstSearch, BreadthFirstSearch, Dijkstra

class Algorithm(Enum):
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    DIJKSTRA = "Dijkstra's Algorithm"

class MazeSolver:
    """Coordinates different pathfinding algorithms for maze solving"""
    
    def __init__(self, maze: List[List[int]]):
        """
        Initialize maze solver with algorithm instances
        
        Args:
            maze: 2D list representing the maze (0 = path, 1 = wall)
        """
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        
        # Initialize algorithm instances
        self.algorithms = {
            Algorithm.DFS: DepthFirstSearch(maze),
            Algorithm.BFS: BreadthFirstSearch(maze),
            Algorithm.DIJKSTRA: Dijkstra(maze)
        }
        
    def solve(self, start: Tuple[int, int], end: Tuple[int, int], 
              algorithm: Algorithm) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Solve the maze using specified algorithm
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            algorithm: Algorithm to use
            
        Returns:
            Tuple of (path, visited_cells)
        """
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return self.algorithms[algorithm].solve(start, end)
    
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int], 
                      algorithm: Algorithm) -> Generator[Dict[str, Any], None, None]:
        """
        Solve the maze using specified algorithm with animation
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            algorithm: Algorithm to use
            
        Yields:
            Animation state information
        """
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        yield from self.algorithms[algorithm].solve_animated(start, end)
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get valid neighboring cells (maintained for backward compatibility)
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of valid neighbor coordinates
        """
        return self.algorithms[Algorithm.DFS].get_neighbors(x, y)