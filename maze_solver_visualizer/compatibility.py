"""
Backward Compatibility Module
Provides compatibility with existing code that expects the old maze format
"""

from typing import List, Tuple, Set, Dict, Any, Optional
from graph import ExplicitGraph, TerrainType
from maze_generator import MazeGenerator as NewMazeGenerator
from maze_solver import MazeSolver as NewMazeSolver, Algorithm

class LegacyMazeGenerator:
    """Legacy maze generator that works with the old 2D list format"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._generator = NewMazeGenerator(width, height)
        self._last_start = None
        self._last_end = None
    
    def generate(self, randomize_positions: bool = True) -> List[List[int]]:
        """Generate a maze in the old 2D list format with optional position randomization"""
        if randomize_positions:
            # Generate with randomized start and end positions
            graph, start, end = self._generator.generate_with_positions(
                randomize_end=True,
                randomize_start=True
            )
            self._last_start = start
            self._last_end = end
            return graph.to_simple_grid()
        else:
            # Use legacy generation
            return self._generator.generate_legacy_maze()
    
    def get_start_position(self) -> Tuple[int, int]:
        """Get the start position"""
        if self._last_start is not None:
            return self._last_start
        return self._generator.get_start_position()
    
    def get_end_position(self) -> Tuple[int, int]:
        """Get the end position"""
        if self._last_end is not None:
            return self._last_end
        return self._generator.get_end_position()
    
    def generate_with_positions(self, randomize_positions: bool = True) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """Generate maze with start and end positions in old format"""
        maze = self.generate(randomize_positions)
        start = self.get_start_position()
        end = self.get_end_position()
        return maze, start, end
    
    def generate_multiple_paths(self, num_paths: int = 4) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """Generate a maze with multiple paths of different lengths"""
        graph, start, end = self._generator.generate_multiple_paths(num_paths)
        self._last_start = start
        self._last_end = end
        return graph.to_simple_grid(), start, end

class LegacyMazeSolver:
    """Legacy maze solver that works with the old 2D list format"""
    
    def __init__(self, maze: List[List[int]]):
        # Convert old maze to explicit graph
        self._graph = ExplicitGraph(len(maze[0]), len(maze))
        self._graph.build_from_maze_grid(maze)
        
        # Create new solver with the graph
        self._solver = NewMazeSolver(self._graph)
        
        # Store original maze for compatibility
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int], 
              algorithm: Algorithm) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Solve using the new solver but with old interface"""
        return self._solver.solve(start, end, algorithm)
    
    def solve_animated(self, start: Tuple[int, int], end: Tuple[int, int], 
                      algorithm: Algorithm):
        """Solve with animation using the new solver"""
        yield from self._solver.solve_animated(start, end, algorithm)
    
    def find_all_paths(self, start: Tuple[int, int], end: Tuple[int, int], 
                      max_paths: int = 50) -> Set[Tuple[int, int]]:
        """Find all possible paths using the new solver"""
        return self._solver.find_all_paths(start, end, max_paths)

# For backward compatibility, expose the legacy classes with the original names
MazeGenerator = LegacyMazeGenerator
MazeSolver = LegacyMazeSolver

# Enhanced versions with explicit graph features
class EnhancedMazeGenerator:
    """Enhanced maze generator with explicit graph features"""
    
    def __init__(self, width: int, height: int):
        self._generator = NewMazeGenerator(width, height)
    
    def generate_with_terrain(self, 
                            terrain_probabilities: Optional[Dict[TerrainType, float]] = None,
                            randomize_end: bool = False) -> Tuple[ExplicitGraph, Tuple[int, int], Tuple[int, int]]:
        """
        Generate maze with terrain costs and optional randomized end
        
        Args:
            terrain_probabilities: Optional terrain distribution
            randomize_end: Whether to randomize end position
            
        Returns:
            Tuple of (graph, start_position, end_position)
        """
        return self._generator.generate_with_positions(
            randomize_end=randomize_end,
            terrain_probabilities=terrain_probabilities
        )
    
    def generate_simple(self) -> Tuple[ExplicitGraph, Tuple[int, int], Tuple[int, int]]:
        """Generate simple maze with uniform terrain costs"""
        terrain_probs = {TerrainType.PATH: 1.0}  # All normal paths
        return self.generate_with_terrain(terrain_probs, randomize_end=False)

class EnhancedMazeSolver:
    """Enhanced maze solver with weighted pathfinding"""
    
    def __init__(self, graph: ExplicitGraph):
        self._solver = NewMazeSolver(graph)
        self.graph = graph
    
    def solve_weighted(self, start: Tuple[int, int], end: Tuple[int, int],
                      algorithm: Algorithm = Algorithm.DIJKSTRA) -> Dict[str, Any]:
        """
        Solve with detailed cost analysis
        
        Returns:
            Dictionary with path, visited cells, and cost information
        """
        path, visited = self._solver.solve(start, end, algorithm)
        
        result = {
            'path': path,
            'visited': visited,
            'path_length': len(path),
            'visited_count': len(visited)
        }
        
        # Calculate path cost if using weighted algorithm
        if algorithm == Algorithm.DIJKSTRA and path:
            total_cost = 0
            terrain_breakdown = {}
            
            for i in range(len(path)):
                position = path[i]
                terrain_info = self._solver.get_terrain_info(position)
                terrain_type = terrain_info['terrain']
                
                terrain_breakdown[terrain_type] = terrain_breakdown.get(terrain_type, 0) + 1
                
                if i > 0:  # Don't count start position cost
                    cost = terrain_info['cost']
                    total_cost += cost
            
            result['total_cost'] = total_cost
            result['terrain_breakdown'] = terrain_breakdown
        
        return result
    
    def get_random_end(self, exclude_start: Tuple[int, int]) -> Tuple[int, int]:
        """Get a random valid end position"""
        return self._solver.get_random_end_position(exclude_start)
    
    def analyze_terrain(self, position: Tuple[int, int]) -> Dict[str, Any]:
        """Get terrain analysis for a position"""
        return self._solver.get_terrain_info(position)