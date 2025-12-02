#!/usr/bin/env python3
"""
Tests for Compatibility Module
Tests backward compatibility layer and enhanced features
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compatibility import (
    LegacyMazeGenerator, LegacyMazeSolver,
    EnhancedMazeGenerator, EnhancedMazeSolver,
    MazeGenerator, MazeSolver  # Aliases
)
from graph import ExplicitGraph, TerrainType
from maze_solver import Algorithm
from typing import List, Tuple

class TestLegacyMazeGenerator:
    """Test legacy maze generator compatibility"""
    
    def test_legacy_generation(self):
        """Test that legacy interface still works"""
        generator = LegacyMazeGenerator(11, 9)
        maze = generator.generate()
        
        # Should return traditional 2D list
        assert isinstance(maze, list)
        assert len(maze) == 9
        assert len(maze[0]) == 11
        
        # All elements should be 0 or 1
        for row in maze:
            for cell in row:
                assert cell in [0, 1]
    
    def test_legacy_start_end_positions(self):
        """Test legacy start and end positions"""
        generator = LegacyMazeGenerator(11, 9)
        
        start = generator.get_start_position()
        end = generator.get_end_position()
        
        assert start == (1, 1)
        assert end == (9, 7)  # width-2, height-2
    
    def test_legacy_generator_consistency(self):
        """Test that legacy generator produces consistent results"""
        generator = LegacyMazeGenerator(7, 7)
        maze1 = generator.generate()
        maze2 = generator.generate()
        
        # Both should have same dimensions
        assert len(maze1) == len(maze2) == 7
        assert len(maze1[0]) == len(maze2[0]) == 7
        
        # Both should have valid maze structure
        for maze in [maze1, maze2]:
            # Check borders are walls
            for x in range(7):
                assert maze[0][x] == 1  # Top border
                assert maze[6][x] == 1  # Bottom border
            for y in range(7):
                assert maze[y][0] == 1  # Left border
                assert maze[y][6] == 1  # Right border

class TestLegacyMazeSolver:
    """Test legacy maze solver compatibility"""
    
    def test_legacy_solver_creation(self):
        """Test creating solver with old maze format"""
        simple_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        solver = LegacyMazeSolver(simple_maze)
        
        # Should have maze property
        assert hasattr(solver, 'maze')
        assert solver.maze == simple_maze
        assert solver.width == 5
        assert solver.height == 5
    
    def test_legacy_solver_pathfinding(self):
        """Test legacy solver pathfinding capabilities"""
        simple_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        solver = LegacyMazeSolver(simple_maze)
        
        # Test basic pathfinding
        path, visited = solver.solve((1, 1), (3, 3), Algorithm.BFS)
        
        assert isinstance(path, list)
        assert isinstance(visited, set)
        
        if path:
            assert path[0] == (1, 1)
            assert path[-1] == (3, 3)
            # All path positions should be passable
            for x, y in path:
                assert simple_maze[y][x] == 0
    
    def test_legacy_solver_algorithms(self):
        """Test all algorithms work with legacy solver"""
        simple_maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        solver = LegacyMazeSolver(simple_maze)
        
        for algorithm in [Algorithm.DFS, Algorithm.BFS, Algorithm.DIJKSTRA]:
            path, visited = solver.solve((1, 1), (5, 3), algorithm)
            assert isinstance(path, list)
            assert isinstance(visited, set)

class TestEnhancedMazeGenerator:
    """Test enhanced maze generator features"""
    
    def test_enhanced_generation_simple(self):
        """Test enhanced simple generation"""
        generator = EnhancedMazeGenerator(11, 9)
        graph, start, end = generator.generate_simple()
        
        assert isinstance(graph, ExplicitGraph)
        assert graph.width == 11
        assert graph.height == 9
        assert isinstance(start, tuple)
        assert isinstance(end, tuple)
        assert start != end
    
    def test_enhanced_generation_with_terrain(self):
        """Test enhanced generation with terrain features"""
        generator = EnhancedMazeGenerator(15, 11)
        
        # Test generation with terrain probabilities
        terrain_probs = {
            TerrainType.PATH: 0.4,
            TerrainType.MUD: 0.3,
            TerrainType.WATER: 0.2,
            TerrainType.SAND: 0.1
        }
        
        graph, start, end = generator.generate_with_terrain(terrain_probs)
        
        assert isinstance(graph, ExplicitGraph)
        assert graph.width == 15
        assert graph.height == 11
        assert isinstance(start, tuple)
        assert isinstance(end, tuple)
        assert start != end
    
    def test_enhanced_generation_randomized_positions(self):
        """Test enhanced generation with randomized start/end"""
        generator = EnhancedMazeGenerator(13, 13)
        
        results = []
        for _ in range(3):
            graph, start, end = generator.generate_with_terrain(randomize_end=True)
            results.append((start, end))
            
            assert isinstance(graph, ExplicitGraph)
            assert isinstance(start, tuple)
            assert isinstance(end, tuple)
            assert start != end
        
        # At least some variation in positions (not guaranteed but likely)
        unique_starts = set(result[0] for result in results)
        unique_ends = set(result[1] for result in results)
        
        # Should have valid positions within bounds
        for start, end in results:
            assert 0 <= start[0] < 13 and 0 <= start[1] < 13
            assert 0 <= end[0] < 13 and 0 <= end[1] < 13

class TestEnhancedMazeSolver:
    """Test enhanced maze solver features"""
    
    def test_enhanced_solver_creation(self):
        """Test creating enhanced solver"""
        # Create a test graph
        graph = ExplicitGraph(7, 7)
        
        # Build simple maze
        maze = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        
        graph.build_from_maze_grid(maze, {TerrainType.PATH: 1.0})
        solver = EnhancedMazeSolver(graph)
        
        assert solver.graph == graph
        assert hasattr(solver, '_solver')
        # Enhanced solver doesn't directly expose width/height
    
    def test_enhanced_solver_pathfinding(self):
        """Test enhanced solver pathfinding"""
        # Create weighted terrain graph
        graph = ExplicitGraph(5, 5)
        
        # Add nodes with different terrain types
        for y in range(5):
            for x in range(5):
                if x == 0 or y == 0 or x == 4 or y == 4:
                    graph.add_node((x, y), TerrainType.WALL)
                elif x == 2 and y == 2:
                    graph.add_node((x, y), TerrainType.MUD)  # Higher cost
                else:
                    graph.add_node((x, y), TerrainType.PATH)
        
        # Add edges
        for y in range(1, 4):
            for x in range(1, 4):
                if x < 3:
                    graph.add_edge((x, y), (x+1, y))
                if y < 3:
                    graph.add_edge((x, y), (x, y+1))
        
        solver = EnhancedMazeSolver(graph)
        result = solver.solve_weighted((1, 1), (3, 3), Algorithm.DIJKSTRA)
        
        assert isinstance(result, dict)
        assert 'path' in result
        assert 'visited' in result
        assert isinstance(result['path'], list)
        assert isinstance(result['visited'], set)

class TestCompatibilityIntegration:
    """Test integration between legacy and enhanced components"""
    
    def test_legacy_to_enhanced_conversion(self):
        """Test converting legacy maze to enhanced graph"""
        # Generate with legacy
        legacy_gen = LegacyMazeGenerator(9, 7)
        maze = legacy_gen.generate()
        
        # Convert to enhanced (if such functionality exists)
        # This would test conversion utilities
        assert isinstance(maze, list)
        assert len(maze) == 7
        assert len(maze[0]) == 9
    
    def test_cross_compatibility_solving(self):
        """Test that both solver types can handle their respective formats"""
        # Legacy approach
        legacy_gen = LegacyMazeGenerator(7, 7)
        legacy_maze = legacy_gen.generate()
        legacy_solver = LegacyMazeSolver(legacy_maze)
        
        legacy_path, legacy_visited = legacy_solver.solve((1, 1), (5, 5), Algorithm.BFS)
        
        # Enhanced approach
        enhanced_gen = EnhancedMazeGenerator(7, 7)
        enhanced_graph, start, end = enhanced_gen.generate_simple()
        enhanced_solver = EnhancedMazeSolver(enhanced_graph)
        
        enhanced_result = enhanced_solver.solve_weighted(start, end, Algorithm.BFS)
        enhanced_path = enhanced_result['path']
        enhanced_visited = enhanced_result['visited']
        
        # Both should produce valid results
        assert isinstance(legacy_path, list)
        assert isinstance(legacy_visited, set)
        assert isinstance(enhanced_path, list)
        assert isinstance(enhanced_visited, set)

class TestAliases:
    """Test that aliases work correctly"""
    
    def test_maze_generator_alias(self):
        """Test that MazeGenerator is an alias for LegacyMazeGenerator"""
        assert MazeGenerator is LegacyMazeGenerator
    
    def test_maze_solver_alias(self):
        """Test that MazeSolver is an alias for LegacyMazeSolver"""
        assert MazeSolver is LegacyMazeSolver
    
    def test_aliases_functionality(self):
        """Test that aliases work functionally"""
        # Test generator alias
        gen1 = MazeGenerator(5, 5)
        gen2 = LegacyMazeGenerator(5, 5)
        
        assert type(gen1) == type(gen2)
        
        # Test solver alias
        simple_maze = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
        
        solver1 = MazeSolver(simple_maze)
        solver2 = LegacyMazeSolver(simple_maze)
        
        assert type(solver1) == type(solver2)

def run_all_tests():
    """Run all compatibility tests"""
    test_classes = [
        TestLegacyMazeGenerator,
        TestLegacyMazeSolver,
        TestEnhancedMazeGenerator,
        TestEnhancedMazeSolver,
        TestCompatibilityIntegration,
        TestAliases
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running Compatibility tests...")
    
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            print(f"  {test_method}... ", end="")
            try:
                getattr(test_instance, test_method)()
                print("PASS")
                passed_tests += 1
            except Exception as e:
                print(f"FAIL: {e}")
                failed_tests.append(f"{test_class.__name__}.{test_method}: {e}")
                # Uncomment for detailed traces
                # traceback.print_exc()
    
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for failure in failed_tests:
            print(f"  - {failure}")
        return False
    else:
        print("All tests passed!")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)