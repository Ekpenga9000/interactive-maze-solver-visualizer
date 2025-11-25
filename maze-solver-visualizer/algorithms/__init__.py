"""
Algorithms package for maze solving
Contains implementations of various pathfinding algorithms
"""

from .base_algorithm import BaseAlgorithm
from .depth_first_search import DepthFirstSearch
from .breadth_first_search import BreadthFirstSearch
from .dijkstra import Dijkstra

__all__ = [
    'BaseAlgorithm',
    'DepthFirstSearch', 
    'BreadthFirstSearch',
    'Dijkstra'
]