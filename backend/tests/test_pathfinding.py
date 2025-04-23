import pytest
import math
from models.intersection import Intersection
from models.road import Road
from models.network import TrafficNetwork
from algos.pathfinding import a_star_shortest_path

def test_a_star_simple_path():
    """Test A* algorithm on a simple path with 3 intersections in a line."""
    network = TrafficNetwork()
    
    # Create three intersections in a line
    i1 = Intersection("i1", 0, 0, "Start")
    i2 = Intersection("i2", 5, 0, "Middle")
    i3 = Intersection("i3", 10, 0, "End")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    network.add_intersection(i3)
    
    # Create roads connecting them
    r1 = Road("r1", "i1", "i2")
    r2 = Road("r2", "i2", "i3")
    
    network.add_road(r1)
    network.add_road(r2)
    
    # Find shortest path from i1 to i3
    path, cost = a_star_shortest_path(network, "i1", "i3")
    
    # Expected path is i1 -> i2 -> i3
    assert path == ["i1", "i2", "i3"]
    
    # Calculate expected cost manually (based on Euclidean distance and default congestion)
    expected_cost = 5 * 1.5 + 5 * 1.5  # 5 units * (1 + congestion of 0.5)
    assert abs(cost - expected_cost) < 0.001

def test_a_star_with_obstacle():
    """Test A* algorithm with an obstacle requiring a detour."""
    network = TrafficNetwork()
    
    # Create four intersections in a square
    i1 = Intersection("i1", 0, 0, "Start")
    i2 = Intersection("i2", 10, 0, "Right")
    i3 = Intersection("i3", 0, 10, "Top")
    i4 = Intersection("i4", 10, 10, "End")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    network.add_intersection(i3)
    network.add_intersection(i4)
    
    # Create roads connecting them (no direct i1 -> i4 road)
    r1 = Road("r1", "i1", "i2")  # Bottom edge
    r2 = Road("r2", "i1", "i3")  # Left edge
    r3 = Road("r3", "i2", "i4")  # Right edge
    r4 = Road("r4", "i3", "i4")  # Top edge
    
    network.add_road(r1)
    network.add_road(r2)
    network.add_road(r3)
    network.add_road(r4)
    
    # Find shortest path from i1 to i4
    path, cost = a_star_shortest_path(network, "i1", "i4")
    
    # We should have either i1 -> i2 -> i4 or i1 -> i3 -> i4 (both are equal distance)
    assert path in [["i1", "i2", "i4"], ["i1", "i3", "i4"]]
    
    # Calculate expected cost manually (based on Euclidean distance)
    expected_cost_option1 = 10 * 1.5 + 10 * 1.5
    expected_cost_option2 = 10 * 1.5 + 10 * 1.5
    assert abs(cost - expected_cost_option1) < 0.001 or abs(cost - expected_cost_option2) < 0.001

def test_a_star_road_closure():
    """Test A* algorithm when a road is closed and an alternative route must be found."""
    network = TrafficNetwork()
    
    # Create four intersections in a square
    i1 = Intersection("i1", 0, 0, "Start")
    i2 = Intersection("i2", 10, 0, "Right")
    i3 = Intersection("i3", 0, 10, "Top")
    i4 = Intersection("i4", 10, 10, "End")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    network.add_intersection(i3)
    network.add_intersection(i4)
    
    # Create roads connecting them
    r1 = Road("r1", "i1", "i2")  # Bottom edge
    r2 = Road("r2", "i1", "i3")  # Left edge
    r3 = Road("r3", "i2", "i4")  # Right edge
    r4 = Road("r4", "i3", "i4")  # Top edge
    
    network.add_road(r1)
    network.add_road(r2)
    network.add_road(r3)
    network.add_road(r4)
    
    # Close the i1 -> i2 road
    network.close_road("r1")
    
    # Find shortest path from i1 to i4
    path, cost = a_star_shortest_path(network, "i1", "i4")
    
    # Expected path is now i1 -> i3 -> i4 (since i1 -> i2 is closed)
    assert path == ["i1", "i3", "i4"]
    
    # Calculate expected cost manually
    expected_cost = 10 * 1.5 + 10 * 1.5
    assert abs(cost - expected_cost) < 0.001

def test_a_star_single_node_path():
    """Test A* algorithm when start and end are the same."""
    network = TrafficNetwork()
    
    # Create an intersection
    i1 = Intersection("i1", 0, 0, "Start/End")
    network.add_intersection(i1)
    
    # Find shortest path from i1 to i1
    path, cost = a_star_shortest_path(network, "i1", "i1")
    
    # Expected path is just i1
    assert path == ["i1"]
    
    # Expected cost is 0
    assert cost == 0

def test_a_star_nonexistent_intersection():
    """Test A* algorithm with nonexistent intersections."""
    network = TrafficNetwork()
    
    # Create an intersection
    i1 = Intersection("i1", 0, 0, "Start")
    network.add_intersection(i1)
    
    # Test with nonexistent start intersection
    with pytest.raises(ValueError):
        a_star_shortest_path(network, "nonexistent", "i1")
    
    # Test with nonexistent end intersection
    with pytest.raises(ValueError):
        a_star_shortest_path(network, "i1", "nonexistent")

def test_a_star_no_path():
    """Test A* algorithm when there is no path between intersections."""
    network = TrafficNetwork()
    
    # Create two disconnected intersections
    i1 = Intersection("i1", 0, 0, "Start")
    i2 = Intersection("i2", 10, 10, "End")
    
    network.add_intersection(i1)
    network.add_intersection(i2)
    
    # No road connecting them
    
    # Try to find shortest path from i1 to i2
    with pytest.raises(ValueError):
        a_star_shortest_path(network, "i1", "i2")