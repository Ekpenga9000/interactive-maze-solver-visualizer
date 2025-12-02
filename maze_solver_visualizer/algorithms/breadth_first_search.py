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
            Dictionary containing animation state with breadth level and branch information
        """
        queue = deque([(start, 0, 'main')])  # (position, breadth_level, branch_id)
        visited = {start}
        parent = {start: None}
        breadth_levels = {start: 0}  # Track breadth level for each cell
        branch_assignments = {start: 'main'}  # Track which branch each cell belongs to
        current_queue_size = 1  # Track how many cells at current level
        next_branch_id = 0  # Counter for assigning branch IDs
        
        while queue:
            current, level, current_branch = queue.popleft()
            current_queue_size = len(queue) + 1  # +1 for current cell being processed
            
            yield {
                'current': current,
                'visited': visited.copy(),
                'queue': list(queue),
                'breadth_levels': breadth_levels.copy(),
                'branch_assignments': branch_assignments.copy(),
                'current_level': level,
                'queue_size': current_queue_size,
                'branching': current_queue_size > 2,  # Flag when breadth > 2
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
                    'breadth_levels': breadth_levels.copy(),
                    'branch_assignments': branch_assignments.copy(),
                    'branching': current_queue_size > 2,
                    'action': 'found'
                }
                return
            
            # Add unvisited neighbors to queue
            x, y = current
            neighbors = [n for n in self.get_neighbors(x, y) if n not in visited]
            
            # If we have multiple neighbors and queue is getting big, assign different branches
            for i, neighbor in enumerate(neighbors):
                visited.add(neighbor)
                parent[neighbor] = current
                breadth_levels[neighbor] = level + 1
                
                # Assign branch: first neighbor keeps current branch, others get new branches
                if i == 0 or len(queue) <= 2:
                    neighbor_branch = current_branch
                else:
                    neighbor_branch = f'branch_{next_branch_id}'
                    next_branch_id += 1
                
                branch_assignments[neighbor] = neighbor_branch
                queue.append((neighbor, level + 1, neighbor_branch))
                
                yield {
                    'current': current,
                    'visited': visited.copy(),
                    'queue': list(queue),
                    'neighbor_added': neighbor,
                    'neighbor_level': level + 1,
                    'breadth_levels': breadth_levels.copy(),
                    'branch_assignments': branch_assignments.copy(),
                    'queue_size': len(queue),
                    'branching': len(queue) > 2,
                    'action': 'neighbor_added'
                }
        
        # No solution found
        yield {
            'current': None,
            'visited': visited.copy(),
            'path': [],
            'breadth_levels': breadth_levels.copy(),
            'branch_assignments': branch_assignments.copy(),
            'branching': False,
            'action': 'no_solution'
        }