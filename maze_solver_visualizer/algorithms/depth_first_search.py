"""
Depth-First Search algorithm implementation
"""

from typing import List, Tuple, Set, Generator, Dict, Any
from .base_algorithm import BaseAlgorithm

class DepthFirstSearch(BaseAlgorithm):
    """Depth-First Search pathfinding algorithm"""
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Solve using Depth-First Search (recursive)
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Returns:
            Tuple of (path, visited_cells)
        """
        visited = set()
        path = []
        
        def dfs_recursive(current: Tuple[int, int]) -> bool:
            x, y = current
            
            if current in visited:
                return False
                
            visited.add(current)
            path.append(current)
            
            if current == end:
                return True
            
            # Try all neighbors
            for neighbor in self.get_neighbors(x, y):
                if dfs_recursive(neighbor):
                    return True
            
            # Backtrack
            path.pop()
            return False
        
        dfs_recursive(start)
        return path, visited
    
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int]) -> Generator[Dict[str, Any], None, None]:
        """
        Solve using animated Depth-First Search
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Yields:
            Dictionary containing animation state
        """
        stack = [start]
        visited = set()
        parent = {start: None}
        
        while stack:
            current = stack[-1]  # Peek at top of stack
            
            yield {
                'current': current,
                'visited': visited.copy(),
                'stack': stack.copy(),
                'action': 'exploring'
            }
            
            # Mark as visited
            if current not in visited:
                visited.add(current)
                yield {
                    'current': current,
                    'visited': visited.copy(),
                    'stack': stack.copy(),
                    'action': 'visited'
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
            
            # Find unvisited neighbors
            neighbors = self.get_neighbors(current[0], current[1])
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            
            if unvisited_neighbors:
                # Choose first unvisited neighbor
                next_cell = unvisited_neighbors[0]
                parent[next_cell] = current
                stack.append(next_cell)
            else:
                # Backtrack
                stack.pop()
                yield {
                    'current': current,
                    'visited': visited.copy(),
                    'stack': stack.copy(),
                    'action': 'backtrack'
                }
        
        # No solution found
        yield {
            'current': None,
            'visited': visited.copy(),
            'path': [],
            'action': 'no_solution'
        }