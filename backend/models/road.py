import math
from typing import Dict, Any, Optional

#Right now I have congestion hard coded in, but I want this to potentially be more dynamic

class Road:
    """
    Represents a road object connecting two intersections in our network
    """

    def __init__(self, id: str, source_id: str, target_id: str, weight: Optional[float] = None):
        """
        Initialize a new road obj
        Args: 
        id: str - id for the road
        source_id: str - source intersection id
        target_id: str - target intersection id 
        weight: float - base weight for the road, If None it will get calc later

        """
        self.id = id
        self.source_id = source_id
        self.target_id = target_id
        self.weight = weight if weight is not None else 1.0
        self.congestion = 0.5 #default moderate congestion
        self.is_open = True #default open

    def calculate_effective_weight(self, network):
        """
        Calculates the effective weight of the road to be used in algo
        Will be using the distance and the congestion to calculate
        Args: network - object containing the intersections
        returns: Float representing the effective weight of the road
        """

        source = network.get_intersection(self.source_id)
        target = network.get_intersection(self.target_id)

        #get the distance between our two points
        distance = math.sqrt((target.x - source.x) ** 2 + (target.y - source.y) ** 2)

        #adjust weight according to congestion

        effective_weight = distance * (1 + self.congestion)
        self.weight = effective_weight
        return effective_weight
    
    def to_dict(self) -> Dict[str, Any]:
        """
        converts road to a dictionary for API 
        
        Returns:
            Dict[str, Any]: Dictionary representation of the road
        """
        return {
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "weight": self.weight,
            "congestion": self.congestion,
            "is_open": self.is_open
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Road':
        """
        creates a road object from dictionary data.
        
        Args:
            data (Dict[str, Any]): Dictionary containing road data
            
        Returns:
            Road: A new road object
        """
        road = cls(
            id=data["id"],
            source_id=data["source"],
            target_id=data["target"],
            weight=data["weight"]
        )
        road.congestion = data.get("congestion", 0.5)
        road.is_open = data.get("is_open", True)
        return road