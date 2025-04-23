import pytest
from models.intersection import Intersection
from models.road import Road
from models.network import TrafficNetwork

def test_network_creation():
    """Test creating an empty network."""
    network = TrafficNetwork()
    assert network.intersections == {}
    assert network.roads == {}
    assert network.adjacency_list == {}

def test_add_intersection():
    """Test adding intersections to the network."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    i2 = Intersection("i2", 10, 10, "Second")
    
    network.add_intersection(i1)
    assert "i1" in network.intersections
    assert network.intersections["i1"] == i1
    assert "i1" in network.adjacency_list
    assert network.adjacency_list["i1"] == []
    
    network.add_intersection(i2)
    assert "i2" in network.intersections
    assert network.intersections["i2"] == i2
    assert "i2" in network.adjacency_list
    assert network.adjacency_list["i2"] == []

def test_add_road():
    """Test adding roads to the network."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    i2 = Intersection("i2", 10, 10, "Second")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    
    road = Road("r1", "i1", "i2")
    network.add_road(road)
    
    # Check that the road is added to the roads dictionary
    assert "r1" in network.roads
    assert network.roads["r1"] == road
    
    # Check the adjacency list updates
    assert len(network.adjacency_list["i1"]) == 1
    assert network.adjacency_list["i1"][0][0] == "i2"  # Target ID
    assert network.adjacency_list["i1"][0][1] > 0  # Weight
    
    # Check bidirectional connection
    assert len(network.adjacency_list["i2"]) == 1
    assert network.adjacency_list["i2"][0][0] == "i1"  # Target ID
    assert network.adjacency_list["i2"][0][1] > 0  # Weight

def test_get_intersection():
    """Test retrieving an intersection by ID."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    network.add_intersection(i1)
    
    retrieved = network.get_intersection("i1")
    assert retrieved == i1
    
    # Test nonexistent intersection
    assert network.get_intersection("nonexistent") is None

def test_get_road():
    """Test retrieving a road by ID."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    i2 = Intersection("i2", 10, 10, "Second")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    
    road = Road("r1", "i1", "i2")
    network.add_road(road)
    
    retrieved = network.get_road("r1")
    assert retrieved == road
    
    # Test nonexistent road
    assert network.get_road("nonexistent") is None

def test_get_road_between():
    """Test finding a road between two intersections."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    i2 = Intersection("i2", 10, 10, "Second")
    i3 = Intersection("i3", 20, 20, "Third")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    network.add_intersection(i3)
    
    road1 = Road("r1", "i1", "i2")
    road2 = Road("r2", "i2", "i3")
    
    network.add_road(road1)
    network.add_road(road2)
    
    # Test finding existing road (both directions)
    assert network.get_road_between("i1", "i2") == road1
    assert network.get_road_between("i2", "i1") == road1
    
    # Test finding nonexistent road
    assert network.get_road_between("i1", "i3") is None

def test_close_road():
    """Test closing a road and its effect on the adjacency list."""
    network = TrafficNetwork()
    
    i1 = Intersection("i1", 0, 0, "First")
    i2 = Intersection("i2", 10, 10, "Second")
    i3 = Intersection("i3", 20, 20, "Third")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    network.add_intersection(i3)
    
    road1 = Road("r1", "i1", "i2")
    road2 = Road("r2", "i2", "i3")
    
    network.add_road(road1)
    network.add_road(road2)
    
    # Before closing, i2 should have connections to both i1 and i3
    assert len(network.adjacency_list["i2"]) == 2
    connections = [node_id for node_id, _ in network.adjacency_list["i2"]]
    assert "i1" in connections
    assert "i3" in connections
    
    # Close the road between i1 and i2
    network.close_road("r1")
    
    # Check that the road is marked as closed
    assert network.get_road("r1").is_open == False
    
    # Check that the adjacency list is updated
    assert len(network.adjacency_list["i1"]) == 0  # No more connections from i1
    assert len(network.adjacency_list["i2"]) == 1  # i2 should only connect to i3 now
    assert network.adjacency_list["i2"][0][0] == "i3"  # i2's only connection should be to i3

def test_network_with_multiple_roads():
    """Test a more complex network with multiple roads and intersections."""
    network = TrafficNetwork()
    
    # Create a grid of 3x3 intersections
    intersections = {}
    for i in range(3):
        for j in range(3):
            id = f"i{i}{j}"
            intersections[id] = Intersection(id, i*10, j*10, f"Intersection_{i}_{j}")
            network.add_intersection(intersections[id])
    
    # Connect horizontal roads
    for i in range(3):
        for j in range(2):
            road_id = f"h{i}{j}"
            source_id = f"i{i}{j}"
            target_id = f"i{i}{j+1}"
            road = Road(road_id, source_id, target_id)
            network.add_road(road)
    
    # Connect vertical roads
    for i in range(2):
        for j in range(3):
            road_id = f"v{i}{j}"
            source_id = f"i{i}{j}"
            target_id = f"i{i+1}{j}"
            road = Road(road_id, source_id, target_id)
            network.add_road(road)
    
    # Check that all intersections have the correct number of connections
    # Corner intersections should have 2 connections
    assert len(network.adjacency_list["i00"]) == 2
    assert len(network.adjacency_list["i02"]) == 2
    assert len(network.adjacency_list["i20"]) == 2
    assert len(network.adjacency_list["i22"]) == 2
    
    # Edge intersections (not corners) should have 3 connections
    assert len(network.adjacency_list["i01"]) == 3
    assert len(network.adjacency_list["i10"]) == 3
    assert len(network.adjacency_list["i12"]) == 3
    assert len(network.adjacency_list["i21"]) == 3
    
    # Center intersection should have 4 connections
    assert len(network.adjacency_list["i11"]) == 4
    
    # Check total number of roads
    assert len(network.roads) == 12  # 6 horizontal + 6 vertical roads