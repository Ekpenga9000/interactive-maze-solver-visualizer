#!/usr/bin/env python3
"""
Script to analyze the average number of breadth levels in generated mazes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm
from statistics import mean, median, stdev
import time

def analyze_maze_breadth_levels(width=21, height=21, num_samples=10):
    """
    Analyze breadth levels in multiple maze samples
    
    Args:
        width: Maze width
        height: Maze height  
        num_samples: Number of mazes to analyze
    """
    print(f"Analyzing breadth levels in {num_samples} mazes of size {width}x{height}")
    print("=" * 60)
    
    breadth_level_data = []
    max_levels = []
    path_lengths = []
    
    for i in range(num_samples):
        print(f"\nAnalyzing maze {i+1}/{num_samples}...")
        
        # Generate maze
        generator = MazeGenerator(width, height)
        graph, start, end = generator.generate_with_positions(randomize_end=True)
        
        # Solve with BFS to get breadth levels
        solver = MazeSolver(graph)
        path, visited = solver.solve(start, end, Algorithm.BFS)
        
        # Get breadth levels by running BFS animation once
        breadth_levels = {}
        bfs_algo = solver.algorithms[Algorithm.BFS]
        
        for state in bfs_algo.solve_animated(start, end):
            if 'breadth_levels' in state:
                breadth_levels.update(state['breadth_levels'])
            if state['action'] == 'found':
                break
        
        # Analyze the levels
        if breadth_levels:
            max_level = max(breadth_levels.values())
            unique_levels = set(breadth_levels.values())
            num_unique_levels = len(unique_levels)
            
            max_levels.append(max_level)
            breadth_level_data.append(num_unique_levels)
            path_lengths.append(len(path))
            
            print(f"  Start: {start}, End: {end}")
            print(f"  Path length: {len(path)}")
            print(f"  Max breadth level: {max_level}")
            print(f"  Unique breadth levels: {num_unique_levels}")
            print(f"  Breadth level distribution: {dict(sorted({level: list(breadth_levels.values()).count(level) for level in unique_levels}.items()))}")
        else:
            print(f"  No solution found for maze {i+1}")
    
    # Calculate statistics
    if breadth_level_data:
        print("\n" + "=" * 60)
        print("SUMMARY STATISTICS")
        print("=" * 60)
        print(f"Number of mazes analyzed: {len(breadth_level_data)}")
        print(f"Maze dimensions: {width}x{height}")
        print()
        
        print("BREADTH LEVELS:")
        print(f"  Average number of unique levels: {mean(breadth_level_data):.2f}")
        print(f"  Median number of unique levels: {median(breadth_level_data):.2f}")
        print(f"  Standard deviation: {stdev(breadth_level_data):.2f}" if len(breadth_level_data) > 1 else "  Standard deviation: N/A (need >1 sample)")
        print(f"  Range: {min(breadth_level_data)} - {max(breadth_level_data)}")
        print()
        
        print("MAX BREADTH LEVELS:")
        print(f"  Average max level reached: {mean(max_levels):.2f}")
        print(f"  Median max level reached: {median(max_levels):.2f}")
        print(f"  Range: {min(max_levels)} - {max(max_levels)}")
        print()
        
        print("PATH LENGTHS:")
        print(f"  Average path length: {mean(path_lengths):.2f}")
        print(f"  Median path length: {median(path_lengths):.2f}")
        print(f"  Range: {min(path_lengths)} - {max(path_lengths)}")
        print()
        
        print("OBSERVATIONS:")
        print(f"  - BFS explores in levels 0 through {max(max_levels)}")
        print(f"  - Most mazes have {min(breadth_level_data)}-{max(breadth_level_data)} distinct breadth levels")
        print(f"  - The wave-like visualization will cycle through {len(breadth_level_data)} levels on average")
        print(f"  - Color palette of 10 colors should handle {(10/mean(max_levels)*100):.1f}% of levels without cycling")

def compare_maze_sizes():
    """Compare breadth levels across different maze sizes"""
    print("COMPARING DIFFERENT MAZE SIZES")
    print("=" * 60)
    
    sizes = [(11, 11), (21, 21), (31, 31), (41, 41)]
    samples_per_size = 5
    
    for width, height in sizes:
        print(f"\nAnalyzing {width}x{height} mazes...")
        
        max_levels = []
        for i in range(samples_per_size):
            generator = MazeGenerator(width, height)
            graph, start, end = generator.generate_with_positions(randomize_end=True)
            solver = MazeSolver(graph)
            
            breadth_levels = {}
            bfs_algo = solver.algorithms[Algorithm.BFS]
            
            for state in bfs_algo.solve_animated(start, end):
                if 'breadth_levels' in state:
                    breadth_levels.update(state['breadth_levels'])
                if state['action'] == 'found':
                    break
            
            if breadth_levels:
                max_levels.append(max(breadth_levels.values()))
        
        if max_levels:
            print(f"  Average max breadth level: {mean(max_levels):.1f}")
            print(f"  Range: {min(max_levels)} - {max(max_levels)}")

if __name__ == "__main__":
    # Analyze standard maze size (21x21)
    analyze_maze_breadth_levels(21, 21, 15)
    
    print("\n" + "=" * 80)
    
    # Compare different sizes
    compare_maze_sizes()