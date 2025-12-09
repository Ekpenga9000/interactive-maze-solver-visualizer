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
        
        # Store all possible paths
        self.last_all_paths = set()
        
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
    
    def find_all_paths(self, start: Tuple[int, int], end: Tuple[int, int], 
                      max_paths: int = 50) -> Set[Tuple[int, int]]:
        """
        Find all cells that could potentially be part of any path from start to end
        Uses fast bidirectional BFS instead of exhaustive path enumeration
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            max_paths: Unused - kept for compatibility
            
        Returns:
            Set of all cells that could be part of any valid path from start to end
        """
        # Fast approach: find all cells reachable from start that can also reach end
        from collections import deque
        
        # BFS from start - find all reachable cells
        start_reachable = set()
        queue = deque([start])
        start_reachable.add(start)
        
        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get_neighbor_positions(current):
                if neighbor not in start_reachable:
                    start_reachable.add(neighbor)
                    queue.append(neighbor)
        
        # BFS from end backwards - find all cells that can reach end
        end_reachable = set()
        queue = deque([end])
        end_reachable.add(end)
        
        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get_neighbor_positions(current):
                if neighbor not in end_reachable:
                    end_reachable.add(neighbor)
                    queue.append(neighbor)
        
        # Intersection: cells that can reach end AND be reached from start
        potential_path_cells = start_reachable & end_reachable
        
        self.last_all_paths = potential_path_cells
        return potential_path_cells