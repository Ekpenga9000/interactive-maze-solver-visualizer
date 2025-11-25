"""
Recursive Maze Solver & Visualizer
A program that generates random mazes and solves them using various algorithms:
- Depth-First Search (DFS)
- Breadth-First Search (BFS) 
- Dijkstra's Algorithm

Author: Your Name
Date: November 23, 2025
"""

import pygame
import sys
import random
from collections import deque
import heapq
from enum import Enum
from typing import List, Tuple, Optional, Set

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAZE_WIDTH = 41  # Odd number for proper maze generation
MAZE_HEIGHT = 31  # Odd number for proper maze generation
CELL_SIZE = min(WINDOW_WIDTH // MAZE_WIDTH, WINDOW_HEIGHT // MAZE_HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Algorithm types
class Algorithm(Enum):
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    DIJKSTRA = "Dijkstra's Algorithm"

def main():
    """Main function to run the maze solver visualizer"""
    print("Maze Solver & Visualizer")
    print("========================")
    print("Dependencies installed successfully!")
    print("- pygame:", pygame.version.ver)
    print("\nStarting maze solver visualizer...")
    
    # Import here to avoid circular imports
    from maze_visualizer import MazeVisualizer
    
    try:
        # Create and run the visualizer
        visualizer = MazeVisualizer(
            window_width=800,
            window_height=600,
            maze_width=41,
            maze_height=31
        )
        visualizer.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()