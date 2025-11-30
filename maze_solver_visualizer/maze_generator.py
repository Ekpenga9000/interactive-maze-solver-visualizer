"""
Maze Generator Module
Generates random mazes using recursive backtracking algorithm with explicit graph support.
"""

import random
from typing import List, Tuple, Set, Dict, Optional
from graph import ExplicitGraph, TerrainType

class MazeGenerator:
    """Generates random mazes using recursive backtracking with explicit graph support"""
    
    def __init__(self, width: int, height: int):
        """
        Initialize maze generator
        
        Args:
            width: Width of the maze (should be odd)
            height: Height of the maze (should be odd)
        """
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        self.graph = ExplicitGraph(width, height)
        
    def generate(self, terrain_probabilities: Optional[Dict[TerrainType, float]] = None) -> ExplicitGraph:
        """
        Generate a random maze using recursive backtracking with explicit graph
        
        Args:
            terrain_probabilities: Optional probabilities for different terrain types
            
        Returns:
            ExplicitGraph representing the maze
        """
        if terrain_probabilities is None:
            terrain_probabilities = {
                TerrainType.PATH: 0.6,
                TerrainType.MUD: 0.2,
                TerrainType.WATER: 0.1,
                TerrainType.SAND: 0.1
            }
        
        # Reset maze
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Start from position (1, 1)
        self._carve_path(1, 1)
        
        # Ensure start position is clear
        self.maze[1][1] = 0
        
        # Build explicit graph from the generated maze
        self.graph.build_from_maze_grid(self.maze, terrain_probabilities)
        
        return self.graph
    
    def _carve_path(self, x: int, y: int):
        """
        Recursively carve paths through the maze
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
        """
        self.maze[y][x] = 0  # Mark current cell as path
        
        # Get all possible directions (up, down, left, right)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check if new position is valid and unvisited
            if (0 < new_x < self.width - 1 and 
                0 < new_y < self.height - 1 and 
                self.maze[new_y][new_x] == 1):
                
                # Carve the wall between current and new cell
                self.maze[y + dy // 2][x + dx // 2] = 0
                
                # Recursively carve from new position
                self._carve_path(new_x, new_y)
    
    def get_strategic_positions(self) -> List[Tuple[int, int]]:
        """
        Get strategic positions in the maze (corners, center, edges)
        
        Returns:
            List of strategic positions that are likely to be passable
        """
        strategic_positions = []
        
        # Corner positions (with some offset from actual corners to avoid walls)
        corners = [
            (1, 1),                                    # Top-left
            (self.width - 2, 1),                      # Top-right
            (1, self.height - 2),                     # Bottom-left
            (self.width - 2, self.height - 2)        # Bottom-right
        ]
        strategic_positions.extend(corners)
        
        # Center position
        center_x = self.width // 2
        center_y = self.height // 2
        # Ensure center is on an odd position (more likely to be passable in our maze generation)
        if center_x % 2 == 0:
            center_x += 1
        if center_y % 2 == 0:
            center_y += 1
        strategic_positions.append((center_x, center_y))
        
        # Edge midpoints
        edge_positions = [
            (self.width // 2, 1),                     # Top edge center
            (self.width // 2, self.height - 2),      # Bottom edge center
            (1, self.height // 2),                   # Left edge center
            (self.width - 2, self.height // 2)       # Right edge center
        ]
        strategic_positions.extend(edge_positions)
        
        # Filter to ensure positions are within bounds and on odd coordinates
        # (more likely to be passable paths in recursive backtracking maze)
        filtered_positions = []
        for x, y in strategic_positions:
            if (0 < x < self.width - 1 and 
                0 < y < self.height - 1):
                # Prefer odd coordinates for better path likelihood
                adj_x = x if x % 2 == 1 else min(x + 1, self.width - 2)
                adj_y = y if y % 2 == 1 else min(y + 1, self.height - 2)
                filtered_positions.append((adj_x, adj_y))
        
        return filtered_positions
    
    def get_random_strategic_position(self, exclude_positions: Optional[Set[Tuple[int, int]]] = None) -> Optional[Tuple[int, int]]:
        """
        Get a random strategic position, with fallback to any passable position
        
        Args:
            exclude_positions: Positions to exclude from selection
            
        Returns:
            Random strategic position, or None if none available
        """
        if exclude_positions is None:
            exclude_positions = set()
        
        # First try strategic positions
        strategic_positions = self.get_strategic_positions()
        available_strategic = [pos for pos in strategic_positions if pos not in exclude_positions]
        
        if hasattr(self, 'graph') and self.graph:
            # Filter to only passable positions
            passable_strategic = [pos for pos in available_strategic if self.graph.is_passable(pos)]
            if passable_strategic:
                return random.choice(passable_strategic)
        
        # Fallback to any passable position if no strategic positions are available
        return self.get_random_end_position(exclude_positions)

    def get_start_position(self) -> Tuple[int, int]:
        """Get the start position of the maze"""
        return (1, 1)
    
    def get_end_position(self) -> Tuple[int, int]:
        """Get the default end position of the maze"""
        return (self.width - 2, self.height - 2)
    
    def get_random_end_position(self, exclude_positions: Optional[Set[Tuple[int, int]]] = None) -> Optional[Tuple[int, int]]:
        """
        Get a random valid end position from the graph
        
        Args:
            exclude_positions: Optional set of positions to exclude (e.g., start position)
            
        Returns:
            Random end position, or None if no valid positions available
        """
        if exclude_positions is None:
            exclude_positions = set()
        
        passable_positions = self.graph.get_all_passable_positions()
        
        # Filter out excluded positions
        available_positions = [pos for pos in passable_positions if pos not in exclude_positions]
        
        if not available_positions:
            return None
        
        return random.choice(available_positions)
    
    def generate_with_positions(self, 
                              randomize_end: bool = False,
                              randomize_start: bool = False,
                              terrain_probabilities: Optional[Dict[TerrainType, float]] = None) -> Tuple[ExplicitGraph, Tuple[int, int], Tuple[int, int]]:
        """
        Generate a random maze and return it with start and end positions
        
        Args:
            randomize_end: Whether to randomize the end position
            randomize_start: Whether to randomize the start position  
            terrain_probabilities: Optional probabilities for different terrain types
            
        Returns:
            Tuple of (graph, start_position, end_position)
        """
        graph = self.generate(terrain_probabilities)
        
        # Determine start position
        if randomize_start:
            start = self.get_random_strategic_position()
            if start is None:
                start = self.get_start_position()  # Fallback
        else:
            start = self.get_start_position()
        
        # Determine end position
        if randomize_end:
            end = self.get_random_strategic_position({start})
            if end is None:
                # Fallback to default end position if no valid random position found
                end = self.get_end_position() if self.get_end_position() != start else self.get_random_end_position({start})
        else:
            end = self.get_end_position()
        
        # Ensure start and end are different
        if end == start:
            alternative_end = self.get_random_end_position({start})
            if alternative_end:
                end = alternative_end
        
        return graph, start, end
    
    def generate_legacy_maze(self) -> List[List[int]]:
        """
        Generate a traditional maze grid (for backward compatibility)
        
        Returns:
            2D list representing the maze (0 = path, 1 = wall)
        """
        # Reset maze
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Start from position (1, 1)
        self._carve_path(1, 1)
        
        # Ensure start and end points are clear
        self.maze[1][1] = 0  # Start
        self.maze[self.height - 2][self.width - 2] = 0  # End
        
        return self.maze