import pytest
import math
from models.intersection import Intersection
from models.road import Road
from models.network import TrafficNetwork

def test_road_creation():
    road = Road("r1", "i1", "i2")
    assert road.id == "r1"
    assert road.source_id == "i1"
    assert road.target_id == "i2"
    assert road.weight == 1.0
    assert road.congestion == 0.5
    assert road.is_open == True
    
    # Test with custom weight
    road = Road("r1", "i1", "i2", 2.5)
    assert road.weight == 2.5

def test_calculate_effective_weight():
    # Create a simple network with two intersections
    network = TrafficNetwork()
    
    # Create intersections at coordinates (0,0) and (3,4)
    intersection1 = Intersection("i1", 0, 0)
    intersection2 = Intersection("i2", 3, 4)
    
    network.add_intersection(intersection1)
    network.add_intersection(intersection2)
    
    # Create a road between them
    road = Road("r1", "i1", "i2")
    
    # Calculate the effective weight
    effective_weight = road.calculate_effective_weight(network)
    
    # Expected Euclidean distance is 5 (3-4-5 triangle)
    # With default congestion of 0.5, effective weight should be 5 * 1.5 = 7.5
    assert abs(effective_weight - 7.5) < 0.001
    
    # Test with different congestion
    road.congestion = 0.8
    effective_weight = road.calculate_effective_weight(network)
    assert abs(effective_weight - (5 * 1.8)) < 0.001

def test_to_dict():
    road = Road("r1", "i1", "i2", 2.5)
    road.congestion = 0.75
    
    d = road.to_dict()
    assert d["id"] == "r1"
    assert d["source"] == "i1"
    assert d["target"] == "i2"
    assert d["weight"] == 2.5
    assert d["congestion"] == 0.75
    assert d["is_open"] == True

def test_from_dict():
    data = {
        "id": "r1",
        "source": "i1",
        "target": "i2",
        "weight": 2.5,
        "congestion": 0.75,
        "is_open": True
    }
    
    road = Road.from_dict(data)
    assert road.id == "r1"
    assert road.source_id == "i1"
    assert road.target_id == "i2"
    assert road.weight == 2.5
    assert road.congestion == 0.75
    assert road.is_open == True
    
    # Test without optional fields
    data = {
        "id": "r1",
        "source": "i1",
        "target": "i2",
        "weight": 2.5
    }
    
    road = Road.from_dict(data)
    assert road.congestion == 0.5  # Default
    assert road.is_open == True    # Default