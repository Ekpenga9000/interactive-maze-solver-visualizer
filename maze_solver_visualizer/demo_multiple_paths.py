#!/usr/bin/env python3
"""
Multiple Paths Demo
Demonstrates the maze generation with multiple paths of different lengths
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maze_visualizer import MazeVisualizer

def main():
    """Demo the multiple paths feature"""
    print("=== Multiple Paths Maze Demo ===")
    print("This demo shows mazes with 3-4 different length paths from start to end.")
    print()
    print("Key differences from regular mazes:")
    print("  📍 Multiple distinct routes")
    print("  📏 Different path lengths")  
    print("  🎯 BFS finds shortest path")
    print("  🌪️  DFS may find longer paths")
    print("  ⚖️  Dijkstra optimizes for cost (if terrain weights enabled)")
    print()
    print("Enhanced Controls:")
    print("  G - Generate regular maze")
    print("  M - Generate maze with MULTIPLE PATHS ⭐")
    print("  S - Solve with current algorithm")
    print("  1/2/3 - Switch algorithms (DFS/BFS/Dijkstra)")
    print("  R - Reset")
    print("  Q - Quit")
    print()
    
    # Create visualizer
    visualizer = MazeVisualizer(800, 600, 21, 21)  # 21x21 for good visibility
    
    # Generate initial multiple-paths maze
    visualizer.generate_multiple_paths_maze()
    
    print("Starting maze visualizer with multiple paths...")
    print("Press 'M' to generate new multiple-paths mazes!")
    print("Press 'G' to compare with regular mazes.")
    print("Try different algorithms to see how they find different routes!")
    
    visualizer.run()

if __name__ == "__main__":
    main()