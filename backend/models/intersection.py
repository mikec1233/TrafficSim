import random
from typing import Dict, Any, Optional

class Intersection:
    """
    This object represents an intersection

    """
    def __init__(self, id: str, x: float, y: float, name: Optional[str] = None):
        """
       Initializes a new intersection

       Args: 
        id: str - a unique indentifier for the intersection
        name: str - optional, human readable name
        x: x coord for intersection location
        y: y coord for intersection location
        """

        self.id = id
        self.name = name if name is not None else f"Intersection_{id}"
        self.x = x
        self.y = y
        self.congestion = random.random()

    def to_dict(self) -> Dict[str, Any]:
        """
        This will convert an intersection obj to a dictionary
        Need this for sending data through API for frontend vis

        Returns a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "congestion": self.congestion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Intersection':
        """
        Creates an intersection obj from the dictionary

        Args: Dictionary rep of the intersection
        Returns: A new intersection obj
        """
        intersection = cls(
            id=data["id"],
            name=data["name"],
            x=data["x"],
            y=data["y"]
        )
        #get congestion key, default to random if key doesnt exist
        intersection.congestion = data.get("congestion", random.random())
        return intersection





        
