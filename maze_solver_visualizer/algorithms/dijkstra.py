"""
Dijkstra's algorithm implementation
"""

from typing import List, Tuple, Set, Generator, Dict, Any, TYPE_CHECKING
import heapq
from .base_algorithm import BaseAlgorithm

if TYPE_CHECKING:
    from graph import ExplicitGraph

class Dijkstra(BaseAlgorithm):
    """Dijkstra's pathfinding algorithm"""
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Solve using Dijkstra's Algorithm with weighted edges
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Returns:
            Tuple of (path, visited_cells)
        """
        # Priority queue: (distance, position)
        pq = [(0, start)]
        distances = {start: 0}
        parent = {start: None}
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == end:
                # Reconstruct path
                path = self.reconstruct_path(parent, start, end)
                return path, visited
            
            x, y = current
            # Use weighted neighbors from explicit graph
            for neighbor, edge_weight in self.get_neighbors_with_weights(x, y):
                if neighbor not in visited:
                    new_distance = current_dist + edge_weight
                    
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent[neighbor] = current
                        heapq.heappush(pq, (new_distance, neighbor))
        
        return [], visited  # No path found
    
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int]) -> Generator[Dict[str, Any], None, None]:
        """
        Solve using animated Dijkstra's Algorithm
        
        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)
            
        Yields:
            Dictionary containing animation state
        """
        pq = [(0, start)]
        distances = {start: 0}
        parent = {start: None}
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            yield {
                'current': current,
                'visited': visited.copy(),
                'distances': distances.copy(),
                'current_distance': current_dist,
                'action': 'exploring'
            }
            
            # Skip if we've already processed this cell with a shorter distance
            if current in visited:
                continue
            
            # Mark as visited
            visited.add(current)
            yield {
                'current': current,
                'visited': visited.copy(),
                'distances': distances.copy(),
                'current_distance': current_dist,
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
            
            # Process neighbors
            x, y = current
            # Use weighted neighbors from explicit graph
            for neighbor, edge_weight in self.get_neighbors_with_weights(x, y):
                if neighbor not in visited:
                    new_distance = current_dist + edge_weight
                    
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent[neighbor] = current
                        heapq.heappush(pq, (new_distance, neighbor))
                        
                        yield {
                            'current': current,
                            'visited': visited.copy(),
                            'distances': distances.copy(),
                            'neighbor_updated': neighbor,
                            'new_distance': new_distance,
                            'edge_weight': edge_weight,
                            'action': 'distance_updated'
                        }
        
        # No solution found
        yield {
            'current': None,
            'visited': visited.copy(),
            'path': [],
            'action': 'no_solution'
        }