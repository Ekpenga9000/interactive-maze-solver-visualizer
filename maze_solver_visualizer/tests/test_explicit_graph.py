#!/usr/bin/env python3
"""
Tests for Explicit Graph Module
Tests the core graph data structure, terrain types, and weighted edges
"""

import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import ExplicitGraph, GraphNode, TerrainType
from typing import Dict, List, Tuple

class TestTerrainType:
    """Test terrain type enumeration"""
    
    def test_terrain_values(self):
        """Test that terrain types have correct cost values"""
        assert TerrainType.WALL.value == -1
        assert TerrainType.PATH.value == 1
        assert TerrainType.MUD.value == 3
        assert TerrainType.WATER.value == 5
        assert TerrainType.SAND.value == 2
        assert TerrainType.ICE.value == 1
    
    def test_terrain_ordering(self):
        """Test that terrain costs are ordered correctly"""
        assert TerrainType.PATH.value <= TerrainType.ICE.value
        assert TerrainType.PATH.value < TerrainType.SAND.value
        assert TerrainType.SAND.value < TerrainType.MUD.value
        assert TerrainType.MUD.value < TerrainType.WATER.value

class TestGraphNode:
    """Test GraphNode functionality"""
    
    def test_node_creation(self):
        """Test creating a graph node"""
        position = (5, 5)
        node = GraphNode(position, TerrainType.PATH)
        
        assert node.position == position
        assert node.terrain == TerrainType.PATH
        assert node.neighbors == {}
        assert node.is_passable()
    
    def test_wall_node(self):
        """Test wall node is not passable"""
        node = GraphNode((0, 0), TerrainType.WALL)
        assert not node.is_passable()
    
    def test_add_neighbor(self):
        """Test adding neighbors with weights"""
        node = GraphNode((5, 5), TerrainType.PATH)
        neighbor_pos = (5, 6)
        weight = 2.5
        
        node.add_neighbor(neighbor_pos, weight)
        
        assert neighbor_pos in node.neighbors
        assert node.neighbors[neighbor_pos] == weight
    
    def test_multiple_neighbors(self):
        """Test adding multiple neighbors"""
        node = GraphNode((5, 5), TerrainType.PATH)
        neighbors = [
            ((4, 5), 1.0),
            ((6, 5), 3.0),
            ((5, 4), 2.0),
            ((5, 6), 1.0)
        ]
        
        for pos, weight in neighbors:
            node.add_neighbor(pos, weight)
        
        assert len(node.neighbors) == 4
        for pos, weight in neighbors:
            assert node.neighbors[pos] == weight

class TestExplicitGraph:
    """Test ExplicitGraph functionality"""
    
    def test_graph_creation(self):
        """Test creating an empty graph"""
        graph = ExplicitGraph(10, 10)
        
        assert graph.width == 10
        assert graph.height == 10
        assert len(graph.nodes) == 0
        assert len(graph.passable_positions) == 0
    
    def test_add_node(self):
        """Test adding nodes to graph"""
        graph = ExplicitGraph(10, 10)
        position = (5, 5)
        
        graph.add_node(position, TerrainType.PATH)
        
        assert position in graph.nodes
        assert graph.nodes[position].terrain == TerrainType.PATH
        assert position in graph.passable_positions
    
    def test_add_wall_node(self):
        """Test that wall nodes are not added to passable positions"""
        graph = ExplicitGraph(10, 10)
        position = (0, 0)
        
        graph.add_node(position, TerrainType.WALL)
        
        assert position in graph.nodes
        assert position not in graph.passable_positions
    
    def test_add_edge_bidirectional(self):
        """Test adding bidirectional edges"""
        graph = ExplicitGraph(10, 10)
        pos1 = (5, 5)
        pos2 = (5, 6)
        
        graph.add_node(pos1, TerrainType.PATH)
        graph.add_node(pos2, TerrainType.MUD)
        graph.add_edge(pos1, pos2, bidirectional=True)
        
        # Check both directions exist
        assert pos2 in graph.nodes[pos1].neighbors
        assert pos1 in graph.nodes[pos2].neighbors
        
        # Check correct weights (cost of entering destination)
        assert graph.nodes[pos1].neighbors[pos2] == TerrainType.MUD.value
        assert graph.nodes[pos2].neighbors[pos1] == TerrainType.PATH.value
    
    def test_add_edge_unidirectional(self):
        """Test adding unidirectional edges"""
        graph = ExplicitGraph(10, 10)
        pos1 = (5, 5)
        pos2 = (5, 6)
        
        graph.add_node(pos1, TerrainType.PATH)
        graph.add_node(pos2, TerrainType.WATER)
        graph.add_edge(pos1, pos2, bidirectional=False)
        
        # Check only one direction exists
        assert pos2 in graph.nodes[pos1].neighbors
        assert pos1 not in graph.nodes[pos2].neighbors
        
        # Check correct weight
        assert graph.nodes[pos1].neighbors[pos2] == TerrainType.WATER.value
    
    def test_no_edge_to_wall(self):
        """Test that edges are not created to/from walls"""
        graph = ExplicitGraph(10, 10)
        pos1 = (5, 5)
        pos2 = (5, 6)
        
        graph.add_node(pos1, TerrainType.PATH)
        graph.add_node(pos2, TerrainType.WALL)
        graph.add_edge(pos1, pos2, bidirectional=True)
        
        # No edges should be created
        assert pos2 not in graph.nodes[pos1].neighbors
        assert pos1 not in graph.nodes[pos2].neighbors
    
    def test_get_neighbors(self):
        """Test getting neighbors with weights"""
        graph = ExplicitGraph(10, 10)
        center = (5, 5)
        neighbors = [
            ((4, 5), TerrainType.PATH),
            ((6, 5), TerrainType.MUD),
            ((5, 4), TerrainType.SAND),
            ((5, 6), TerrainType.WATER)
        ]
        
        # Add center node
        graph.add_node(center, TerrainType.PATH)
        
        # Add neighbors and edges
        for pos, terrain in neighbors:
            graph.add_node(pos, terrain)
            graph.add_edge(center, pos, bidirectional=False)
        
        # Get neighbors
        neighbor_data = graph.get_neighbors(center)
        
        assert len(neighbor_data) == 4
        
        # Check each neighbor has correct weight
        neighbor_dict = dict(neighbor_data)
        for pos, terrain in neighbors:
            assert pos in neighbor_dict
            assert neighbor_dict[pos] == terrain.value

def run_all_tests():
    """Run all tests in this module"""
    test_classes = [TestTerrainType, TestGraphNode, TestExplicitGraph]
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    print("Running ExplicitGraph tests...")
    
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        test_instance = test_class()
        
        # Get all test methods
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_') and callable(getattr(test_instance, method))]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                print(f"  {test_method}...", end=" ")
                getattr(test_instance, test_method)()
                print("PASS")
                passed_tests += 1
            except Exception as e:
                print(f"FAIL: {e}")
                failed_tests.append(f"{test_class.__name__}.{test_method}: {e}")
                traceback.print_exc()
    
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