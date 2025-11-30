"""
Maze Solver Module
Contains the main solver class that coordinates different pathfinding algorithms
"""

from typing import List, Tuple, Set, Generator, Dict, Any, TYPE_CHECKING
from enum import Enum
from algorithms import DepthFirstSearch, BreadthFirstSearch, Dijkstra

if TYPE_CHECKING:
    from graph import ExplicitGraph

class Algorithm(Enum):
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    DIJKSTRA = "Dijkstra's Algorithm"

class MazeSolver:
    """Coordinates different pathfinding algorithms for maze solving"""
    
    def __init__(self, graph: 'ExplicitGraph'):
        """
        Initialize maze solver with algorithm instances using explicit graph
        
        Args:
            graph: Explicit graph representation of the maze
        """
        self.graph = graph
        self.height = graph.height
        self.width = graph.width
        
        # Initialize algorithm instances with the explicit graph
        self.algorithms = {
            Algorithm.DFS: DepthFirstSearch(graph),
            Algorithm.BFS: BreadthFirstSearch(graph),
            Algorithm.DIJKSTRA: Dijkstra(graph)
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
    
    def get_random_end_position(self, exclude_start: Tuple[int, int]) -> Tuple[int, int]:
        """
        Get a random valid end position from the graph
        
        Args:
            exclude_start: Starting position to exclude from selection
            
        Returns:
            Random end position
        """
        random_pos = self.graph.get_random_passable_position()
        
        # If random position is same as start, try to find another one
        if random_pos == exclude_start:
            passable_positions = self.graph.get_all_passable_positions()
            available_positions = [pos for pos in passable_positions if pos != exclude_start]
            
            if available_positions:
                import random
                random_pos = random.choice(available_positions)
        
        return random_pos if random_pos else exclude_start
    
    def get_terrain_info(self, position: Tuple[int, int]) -> Dict[str, Any]:
        """
        Get terrain information for a position
        
        Args:
            position: Position to check
            
        Returns:
            Dictionary with terrain type and movement cost
        """
        terrain_type = self.graph.get_terrain_type(position)
        return {
            'terrain': terrain_type.name,
            'cost': terrain_type.value,
            'passable': self.graph.is_passable(position)
        }
    
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