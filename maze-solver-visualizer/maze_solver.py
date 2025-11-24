"""
Maze Solver Module
Contains algorithms for solving mazes: DFS, BFS, and Dijkstra's Algorithm
"""

from collections import deque
import heapq
from typing import List, Tuple, Optional, Set, Dict
from enum import Enum

class Algorithm(Enum):
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    DIJKSTRA = "Dijkstra's Algorithm"

class MazeSolver:
    """Solves mazes using various pathfinding algorithms"""
    
    def __init__(self, maze: List[List[int]]):
        """
        Initialize maze solver
        
        Args:
            maze: 2D list representing the maze (0 = path, 1 = wall)
        """
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.path = []
        self.visited_cells = set()
        
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
        if algorithm == Algorithm.DFS:
            return self._solve_dfs(start, end)
        elif algorithm == Algorithm.BFS:
            return self._solve_bfs(start, end)
        elif algorithm == Algorithm.DIJKSTRA:
            return self._solve_dijkstra(start, end)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring cells"""
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
    
    def _solve_dfs(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Solve using Depth-First Search (recursive)"""
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
            for neighbor in self._get_neighbors(x, y):
                if dfs_recursive(neighbor):
                    return True
            
            # Backtrack
            path.pop()
            return False
        
        dfs_recursive(start)
        return path, visited
    
    def _solve_bfs(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Solve using Breadth-First Search"""
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path, visited
            
            x, y = current
            for neighbor in self._get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return [], visited  # No path found
    
    def _solve_dijkstra(self, start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Solve using Dijkstra's Algorithm"""
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
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path, visited
            
            x, y = current
            for neighbor in self._get_neighbors(x, y):
                if neighbor not in visited:
                    new_distance = current_dist + 1  # Each step has cost 1
                    
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent[neighbor] = current
                        heapq.heappush(pq, (new_distance, neighbor))
        
        return [], visited  # No path found