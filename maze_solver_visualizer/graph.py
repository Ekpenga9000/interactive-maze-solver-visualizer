"""
Explicit Graph Module
Represents mazes as explicit graphs with weighted edges for performance-critical pathfinding
"""

from typing import Dict, List, Tuple, Set, Optional
from enum import Enum
from dataclasses import dataclass
import random

class TerrainType(Enum):
    """Different terrain types with associated costs"""
    WALL = -1       # Impassable
    PATH = 1        # Normal path
    MUD = 3         # Slow terrain
    WATER = 5       # Very slow terrain
    SAND = 2        # Slightly slow terrain
    ICE = 1         # Fast terrain (same as normal for now)

@dataclass #    Data class for graph nodes
class GraphNode:
    """Represents a node in the explicit graph"""
    position: Tuple[int, int]
    terrain: TerrainType
    neighbors: Dict[Tuple[int, int], float]  # position -> edge_weight
    
    def __init__(self, position: Tuple[int, int], terrain: TerrainType):
        self.position = position
        self.terrain = terrain
        self.neighbors = {}
    
    def add_neighbor(self, neighbor_pos: Tuple[int, int], weight: float):
        """Add a neighbor with the given edge weight"""
        self.neighbors[neighbor_pos] = weight
    
    def is_passable(self) -> bool:
        """Check if this node is passable"""
        return self.terrain != TerrainType.WALL

class ExplicitGraph:
    """Explicit graph representation of a maze with weighted edges"""
    
    def __init__(self, width: int, height: int):
        """
        Initialize empty graph
        
        Args:
            width: Width of the grid
            height: Height of the grid
        """
        self.width = width
        self.height = height
        self.nodes: Dict[Tuple[int, int], GraphNode] = {}
        self.passable_positions: List[Tuple[int, int]] = []
        
    def add_node(self, position: Tuple[int, int], terrain: TerrainType):
        """
        Add a node to the graph
        
        Args:
            position: (x, y) coordinate
            terrain: Terrain type for the node
        """
        node = GraphNode(position, terrain)
        self.nodes[position] = node
        
        if terrain != TerrainType.WALL:
            self.passable_positions.append(position)
    
    def add_edge(self, pos1: Tuple[int, int], pos2: Tuple[int, int], bidirectional: bool = True):
        """
        Add weighted edge between two nodes
        
        Args:
            pos1: First position
            pos2: Second position
            bidirectional: Whether to add edge in both directions
        """
        if pos1 not in self.nodes or pos2 not in self.nodes:
            return
        
        node1 = self.nodes[pos1]
        node2 = self.nodes[pos2]
        
        # Only add edges between passable nodes
        if not (node1.is_passable() and node2.is_passable()):
            return
        
        # Calculate weight as the cost of entering the destination node
        weight_1_to_2 = node2.terrain.value
        node1.add_neighbor(pos2, weight_1_to_2)
        
        if bidirectional:
            weight_2_to_1 = node1.terrain.value
            node2.add_neighbor(pos1, weight_2_to_1)
    
    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """
        Get neighbors of a node with their edge weights
        
        Args:
            position: Position to get neighbors for
            
        Returns:
            List of (neighbor_position, edge_weight) tuples
        """
        if position not in self.nodes:
            return []
        
        node = self.nodes[position]
        return [(pos, weight) for pos, weight in node.neighbors.items()]
    
    def get_neighbor_positions(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get just the neighbor positions (for compatibility with existing code)
        
        Args:
            position: Position to get neighbors for
            
        Returns:
            List of neighbor positions
        """
        if position not in self.nodes:
            return []
        
        return list(self.nodes[position].neighbors.keys())
    
    def get_edge_weight(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Get the weight of the edge from pos1 to pos2
        
        Args:
            pos1: Starting position
            pos2: Ending position
            
        Returns:
            Edge weight, or float('inf') if no edge exists
        """
        if pos1 not in self.nodes:
            return float('inf')
        
        return self.nodes[pos1].neighbors.get(pos2, float('inf'))
    
    def is_passable(self, position: Tuple[int, int]) -> bool:
        """
        Check if a position is passable
        
        Args:
            position: Position to check
            
        Returns:
            True if passable, False otherwise
        """
        if position not in self.nodes:
            return False
        
        return self.nodes[position].is_passable()
    
    def get_terrain_type(self, position: Tuple[int, int]) -> TerrainType:
        """
        Get the terrain type at a position
        
        Args:
            position: Position to check
            
        Returns:
            TerrainType at the position
        """
        if position not in self.nodes:
            return TerrainType.WALL
        
        return self.nodes[position].terrain
    
    def get_random_passable_position(self) -> Optional[Tuple[int, int]]:
        """
        Get a random passable position from the graph
        
        Returns:
            Random passable position, or None if no passable positions exist
        """
        if not self.passable_positions:
            return None
        
        return random.choice(self.passable_positions)
    
    def get_all_passable_positions(self) -> List[Tuple[int, int]]:
        """
        Get all passable positions in the graph
        
        Returns:
            List of all passable positions
        """
        return self.passable_positions.copy()
    
    def build_from_maze_grid(self, maze_grid: List[List[int]], 
                           terrain_probabilities: Optional[Dict[TerrainType, float]] = None):
        """
        Build the explicit graph from a traditional maze grid
        
        Args:
            maze_grid: 2D list where 0 = path, 1 = wall
            terrain_probabilities: Optional probabilities for different terrain types
        """
        if terrain_probabilities is None:
            terrain_probabilities = {
                TerrainType.PATH: 0.7,
                TerrainType.MUD: 0.15,
                TerrainType.WATER: 0.05,
                TerrainType.SAND: 0.1
            }
        
        # Clear existing data
        self.nodes.clear()
        self.passable_positions.clear()
        
        # Create nodes
        for y in range(len(maze_grid)):
            for x in range(len(maze_grid[y])):
                if maze_grid[y][x] == 1:  # Wall
                    terrain = TerrainType.WALL
                else:  # Passable - randomly assign terrain type
                    terrain = self._choose_random_terrain(terrain_probabilities)
                
                self.add_node((x, y), terrain)
        
        # Create edges between adjacent passable nodes
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        
        for position in self.nodes:
            x, y = position
            for dx, dy in directions:
                neighbor_pos = (x + dx, y + dy)
                if neighbor_pos in self.nodes:
                    self.add_edge(position, neighbor_pos, bidirectional=False)
    
    def _choose_random_terrain(self, probabilities: Dict[TerrainType, float]) -> TerrainType:
        """
        Choose a random terrain type based on probabilities
        
        Args:
            probabilities: Dictionary mapping terrain types to their probabilities
            
        Returns:
            Selected terrain type
        """
        rand_val = random.random()
        cumulative_prob = 0.0
        
        for terrain, prob in probabilities.items():
            cumulative_prob += prob
            if rand_val <= cumulative_prob:
                return terrain
        
        # Fallback to PATH if probabilities don't sum to 1.0
        return TerrainType.PATH
    
    def to_visual_grid(self) -> List[List[int]]:
        """
        Convert the graph back to a visual grid for display purposes
        
        Returns:
            2D list compatible with existing visualization code
        """
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        for (x, y), node in self.nodes.items():
            if node.is_passable():
                # Map different terrain types to different numbers for visualization
                terrain_map = {
                    TerrainType.PATH: 0,
                    TerrainType.MUD: 2,
                    TerrainType.WATER: 3,
                    TerrainType.SAND: 4,
                    TerrainType.ICE: 5
                }
                grid[y][x] = terrain_map.get(node.terrain, 0)
            else:
                grid[y][x] = 1  # Wall
        
        return grid
    
    def to_simple_grid(self) -> List[List[int]]:
        """
        Convert the graph to a simple grid for backward compatibility
        
        Returns:
            2D list where 0 = passable (any terrain), 1 = wall
        """
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        for (x, y), node in self.nodes.items():
            if node.is_passable():
                grid[y][x] = 0  # All passable terrain becomes 0
            else:
                grid[y][x] = 1  # Wall
        
        return grid