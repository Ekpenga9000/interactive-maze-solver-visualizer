"""
Base Algorithm class for maze solving
Defines the interface that all pathfinding algorithms must implement
"""

from abc import ABC, abstractmethod # Abstract Base Class
from typing import List, Tuple, Set, Generator, Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING: # to avoid circular imports
    from graph import ExplicitGraph # Forward declaration of ExplicitGraph

class BaseAlgorithm(ABC):
    """Abstract base class for maze solving algorithms"""
    
    def __init__(self, graph: 'ExplicitGraph'):
        """
        Initialize the algorithm with an explicit graph
        
        Args:
            graph: Explicit graph representation of the maze
        """
        self.graph = graph
        self.height = graph.height
        self.width = graph.width
    
    @property # Backward compatibility property
    def maze(self) -> List[List[int]]:
        """
        Backward compatibility property that returns a 2D list representation
        
        Returns:
            2D list where 0 = passable, 1 = wall (for backward compatibility)
        """
        return self.graph.to_simple_grid()
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get valid neighboring cells using precomputed adjacency
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of valid neighbor coordinates
        """
        return self.graph.get_neighbor_positions((x, y))
    
    def get_neighbors_with_weights(self, x: int, y: int) -> List[Tuple[Tuple[int, int], float]]:
        """
        Get valid neighboring cells with their edge weights
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of (neighbor_position, edge_weight) tuples
        """
        return self.graph.get_neighbors((x, y))
    
    def get_edge_weight(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Get the weight of moving from pos1 to pos2
        
        Args:
            pos1: Starting position
            pos2: Ending position
            
        Returns:
            Edge weight
        """
        return self.graph.get_edge_weight(pos1, pos2)
    
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