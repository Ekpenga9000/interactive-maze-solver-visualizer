"""
Breadth-First Search algorithm implementation
"""

from typing import List, Tuple, Set, Generator, Dict, Any, TYPE_CHECKING
from collections import deque
from .base_algorithm import BaseAlgorithm

if TYPE_CHECKING:
    from graph import ExplicitGraph

class BreadthFirstSearch(BaseAlgorithm):
    """Breadth-First Search pathfinding algorithm"""
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Solve using Breadth-First Search
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Returns:
            Tuple of (path, visited_cells)
        """
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                # Reconstruct path
                path = self.reconstruct_path(parent, start, end)
                return path, visited
            
            x, y = current
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return [], visited  # No path found
    
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int]) -> Generator[Dict[str, Any], None, None]:
        """
        Solve using animated Breadth-First Search
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Yields:
            Dictionary containing animation state
        """
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            yield {
                'current': current,
                'visited': visited.copy(),
                'queue': list(queue),
                'action': 'exploring'
            }
            
            # Check if we found the end
            if current == end:
                # Reconstruct path
                path = self.reconstruct_path(parent, start, end)
                yield {
                    'current': current,
                    'visited': visited.copy(),
                    'path': path,
                    'action': 'found'
                }
                return
            
            # Add unvisited neighbors to queue
            x, y = current
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
                    
                    yield {
                        'current': current,
                        'visited': visited.copy(),
                        'queue': list(queue),
                        'neighbor_added': neighbor,
                        'action': 'neighbor_added'
                    }
        
        # No solution found
        yield {
            'current': None,
            'visited': visited.copy(),
            'path': [],
            'action': 'no_solution'
        }