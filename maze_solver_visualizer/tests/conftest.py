# Test Configuration and Fixtures
import pytest
import sys
import os
from typing import List, Tuple, Set

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm

# Test fixtures for reuse across test modules
@pytest.fixture
def small_maze_generator():
    """Create a small maze generator for testing"""
    return MazeGenerator(11, 9)  # Small odd-sized maze

@pytest.fixture
def medium_maze_generator():
    """Create a medium maze generator for testing"""
    return MazeGenerator(21, 15)  # Medium odd-sized maze

@pytest.fixture
def large_maze_generator():
    """Create a large maze generator for testing"""
    return MazeGenerator(41, 31)  # Large odd-sized maze

@pytest.fixture
def simple_test_maze():
    """Create a simple 5x5 test maze for algorithm testing"""
    # Simple maze layout:
    # 1 1 1 1 1
    # 1 0 0 0 1
    # 1 0 1 0 1
    # 1 0 0 0 1
    # 1 1 1 1 1
    return [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

@pytest.fixture
def complex_test_maze():
    """Create a more complex test maze"""
    # Complex maze with multiple paths
    return [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

@pytest.fixture
def impossible_maze():
    """Create a maze with no solution"""
    return [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1]
    ]

@pytest.fixture
def maze_solver_simple(simple_test_maze):
    """Create a maze solver with simple test maze"""
    return MazeSolver(simple_test_maze)

@pytest.fixture
def maze_solver_complex(complex_test_maze):
    """Create a maze solver with complex test maze"""
    return MazeSolver(complex_test_maze)

@pytest.fixture
def maze_solver_impossible(impossible_maze):
    """Create a maze solver with impossible maze"""
    return MazeSolver(impossible_maze)