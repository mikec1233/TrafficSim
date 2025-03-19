import pytest
from models.intersection import Intersection

def test_intersection_creation():
    # Test with name
    i1 = Intersection("i1", 10.0, 20.0, "Main St")
    assert i1.id == "i1"
    assert i1.name == "Main St"
    assert i1.x == 10.0
    assert i1.y == 20.0
    assert 0.0 <= i1.congestion <= 1.0
    
    # Test without name (should create default)
    i2 = Intersection("i2", 30.0, 40.0)
    assert i2.id == "i2"
    assert i2.name == "Intersection_i2"
    assert i2.x == 30.0
    assert i2.y == 40.0

def test_to_dict():
    i = Intersection("i1", 10.0, 20.0, "Main St")
    i.congestion = 0.75  # Set congestion explicitly for test
    
    d = i.to_dict()
    assert d["id"] == "i1"
    assert d["name"] == "Main St"
    assert d["x"] == 10.0
    assert d["y"] == 20.0
    assert d["congestion"] == 0.75

def test_from_dict():
    data = {
        "id": "i1",
        "name": "Main St",
        "x": 10.0,
        "y": 20.0,
        "congestion": 0.75
    }
    
    i = Intersection.from_dict(data)
    assert i.id == "i1"
    assert i.name == "Main St"
    assert i.x == 10.0
    assert i.y == 20.0
    assert i.congestion == 0.75
    
    # Test without congestion
    data.pop("congestion")
    i = Intersection.from_dict(data)
    assert 0.0 <= i.congestion <= 1.0