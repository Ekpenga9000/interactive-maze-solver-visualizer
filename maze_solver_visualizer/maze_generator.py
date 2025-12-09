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
    
    def generate_multiple_paths(self, 
                              num_paths: int = 4,
                              terrain_probabilities: Optional[Dict[TerrainType, float]] = None) -> Tuple[ExplicitGraph, Tuple[int, int], Tuple[int, int]]:
        """
        Generate a maze with multiple paths of different lengths from start to end
        
        Args:
            num_paths: Target number of different paths (3-4 recommended)
            terrain_probabilities: Optional probabilities for different terrain types
            
        Returns:
            Tuple of (graph, start_position, end_position)
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
        
        # Define start and end positions
        start_pos = (1, 1)
        end_pos = (self.width - 2, self.height - 2)
        
        # Create initial path structure with multiple routes
        self._create_multiple_path_structure(start_pos, end_pos, num_paths)
        
        # Fill in remaining areas with standard maze generation
        self._fill_remaining_areas()
        
        # Ensure key positions are clear
        self.maze[start_pos[1]][start_pos[0]] = 0
        self.maze[end_pos[1]][end_pos[0]] = 0
        
        # Build explicit graph from the generated maze
        self.graph.build_from_maze_grid(self.maze, terrain_probabilities)
        
        return self.graph, start_pos, end_pos
    
    def _create_multiple_path_structure(self, start: Tuple[int, int], end: Tuple[int, int], num_paths: int):
        """
        Create the basic structure for multiple paths of different lengths
        
        Args:
            start: Start position
            end: End position
            num_paths: Number of paths to create
        """
        # Create paths more efficiently
        # Path 1: Direct path (always create this)
        self._create_direct_path(start, end)
        
        # Only create additional paths for larger mazes to avoid overcomplexity
        if self.width >= 15 and self.height >= 15:
            # Path 2: Top route (medium length)
            self._create_top_route(start, end)
            
            # Path 3: Bottom route (medium-long length) 
            self._create_bottom_route(start, end)
            
            if num_paths >= 4 and self.width >= 21:
                # Path 4: Center route (only for larger mazes)
                self._create_zigzag_route(start, end)
    
    def _create_direct_path(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Create a relatively direct path from start to end"""
        x, y = start
        end_x, end_y = end
        
        # Move horizontally first
        while x < end_x:
            self.maze[y][x] = 0
            x += 1
        
        # Now move vertically
        while y < end_y:
            self.maze[y][x] = 0
            y += 1
        
        # Ensure end is connected
        self.maze[end_y][end_x] = 0
    
    def _create_top_route(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Create a path that goes through the top portion of the maze"""
        start_x, start_y = start
        end_x, end_y = end
        
        # Calculate waypoint in top area
        top_y = max(3, self.height // 4)
        mid_x = self.width // 2
        
        # Connect start to top waypoint
        self._carve_connection(start, (start_x, top_y))
        self._carve_connection((start_x, top_y), (mid_x, top_y))
        self._carve_connection((mid_x, top_y), (end_x, top_y))
        self._carve_connection((end_x, top_y), end)
    
    def _create_bottom_route(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Create a path that goes through the bottom portion of the maze"""
        start_x, start_y = start
        end_x, end_y = end
        
        # Calculate waypoint in bottom area
        bottom_y = min(self.height - 4, self.height * 3 // 4)
        mid_x = self.width * 3 // 4
        
        # Connect start to bottom waypoint
        self._carve_connection(start, (mid_x, start_y))
        self._carve_connection((mid_x, start_y), (mid_x, bottom_y))
        self._carve_connection((mid_x, bottom_y), (end_x, bottom_y))
        self._carve_connection((end_x, bottom_y), end)
    
    def _create_zigzag_route(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Create a zigzag path through the center (longest route)"""
        start_x, start_y = start
        end_x, end_y = end
        
        # Create a longer path with multiple waypoints
        waypoints = [
            start,
            (self.width // 4, self.height // 3),
            (self.width * 3 // 4, self.height // 2),
            (self.width // 3, self.height * 2 // 3),
            (end_x, self.height * 3 // 4),
            end
        ]
        
        # Connect waypoints sequentially
        for i in range(len(waypoints) - 1):
            self._carve_connection(waypoints[i], waypoints[i + 1])
    
    def _carve_connection(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Carve a simple connection between two points"""
        x1, y1 = from_pos
        x2, y2 = to_pos
        
        # Simple L-shaped connection - ensure all intermediate cells are carved
        current_x, current_y = x1, y1
        
        # First horizontal movement
        while current_x != x2:
            self.maze[current_y][current_x] = 0
            if current_x < x2:
                current_x += 1
            else:
                current_x -= 1
        
        # Then vertical movement
        while current_y != y2:
            self.maze[current_y][current_x] = 0
            if current_y < y2:
                current_y += 1
            else:
                current_y -= 1
        
        # Ensure destination is clear
        self.maze[y2][x2] = 0
    
    def _fill_remaining_areas(self):
        """Fill remaining wall areas with additional maze structure using recursive backtracking"""
        # More selective filling - only fill larger empty areas
        for y in range(3, self.height - 3, 4):  # Less frequent sampling
            for x in range(3, self.width - 3, 4):  # Less frequent sampling
                if self.maze[y][x] == 1:  # Wall that could be a path start
                    # Check if this area is large enough to warrant filling
                    empty_area = 0
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if (0 < y + dy < self.height - 1 and 
                                0 < x + dx < self.width - 1 and 
                                self.maze[y + dy][x + dx] == 1):
                                empty_area += 1
                    
                    # Only fill if there's a significant empty area
                    if empty_area >= 5:
                        self._carve_path(x, y)