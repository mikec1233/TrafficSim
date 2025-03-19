from typing import Dict, List, Tuple, Optional, Any
from .intersection import Intersection
from .road import Road

class TrafficNetwork:
    """
    This object represents the entire network with intersections and roads.
    """
    
    def __init__(self):
        """
        Initialize an empty traffic network.
        In here we have 3 main datastructures:
        a map of the intersection IDs and corresponding obj 
        map of road IDs and their corresponding roads
        adjacency list of the graph
            each intersection ID mapped with a list of tuples(neighbor_id, weight)
        """
        self.intersections: Dict[str, Intersection] = {}
        
        self.roads: Dict[str, Road] = {}
        
        # maps each intersection ID to a list of (neighbor_id, weight) tuples
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}
    
    def add_intersection(self, intersection: Intersection) -> None:
        """
        add an intersection to the network.
        
        Args:
            The intersection to add
        """
        self.intersections[intersection.id] = intersection
        
        # make an empty adjacency list entry for this intersection
        if intersection.id not in self.adjacency_list:
            self.adjacency_list[intersection.id] = []
    
    def add_road(self, road: Road) -> None:
        """
        Add a road to the network.
        
        Args:
        The road to add
        """
        self.roads[road.id] = road
        
        # Calculate the road's effective weight based on distance and congestion
        road.calculate_effective_weight(self)
        
        #becase this is an undirected graph, we need to update adjacency list in both directions 
        if road.source_id not in self.adjacency_list:
            self.adjacency_list[road.source_id] = []
        if road.target_id not in self.adjacency_list:
            self.adjacency_list[road.target_id] = []
        
        # Only add the connection if the road is open
        if road.is_open:
            self.adjacency_list[road.source_id].append((road.target_id, road.weight))
            self.adjacency_list[road.target_id].append((road.source_id, road.weight))
    
    def get_intersection(self, intersection_id: str) -> Optional[Intersection]:
        """
        Get an intersection by its ID.
        
        Args:
            intersection_id (str): The ID of the intersection to retrieve
            
        Returns:
            Optional[Intersection]: The intersection if found, None otherwise
        """
        return self.intersections.get(intersection_id)
    
    def get_road(self, road_id: str) -> Optional[Road]:
        """
        Get a road by its ID.
        
        Args:
        The ID of the road to retrieve
            
        Returns:
        The road if found, None otherwise
        """
        return self.roads.get(road_id)
    
    def get_road_between(self, source_id: str, target_id: str) -> Optional[Road]:
        """
        Find a road connecting two intersections.
        
        Args:
            source_id (str): ID of the first intersection
            target_id (str): ID of the second intersection
            
        Returns:
            Optional[Road]: The connecting road if found, None otherwise
        """
        for road in self.roads.values():
            # Check for the road in both directions
            if ((road.source_id == source_id and road.target_id == target_id) or
                (road.source_id == target_id and road.target_id == source_id)):
                return road
        return None
    
    def close_road(self, road_id: str) -> None:
        """
        Close a road and update the adjacency list.
        
        Args:
            road_id (str): The ID of the road to close
        """
        road = self.get_road(road_id)
        if road:
            road.is_open = False
            """
            
            Remove the road from the adjacency list in both directions
            Starting from the source intersection, we filter the the list of connections to keep only the connections that don’t lead to the target intersection of the closed road

            We do the same for the target intersection.

            For example if we have a road connecting intersection A and B, we remove B from A’s list of neighbors and A from B’s
            
            """ 
            self.adjacency_list[road.source_id] = [
                (node_id, weight) for node_id, weight in self.adjacency_list[road.source_id]
                if node_id != road.target_id
            ]
            self.adjacency_list[road.target_id] = [
                (node_id, weight) for node_id, weight in self.adjacency_list[road.target_id]
                if node_id != road.source_id
            ]