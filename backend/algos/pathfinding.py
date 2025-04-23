#Implementing the A* algorithm for faster pathfinding
from typing import List, Dict, Tuple, Optional
import heapq
import math
from models.network import TrafficNetwork

def a_star_shortest_path(network: TrafficNetwork, start_id: str, end_id: str) -> Tuple[List[str], float]:
    """
    Args:
        network: The traffic network
        start_id: ID of the starting intersection
        end_id: ID of the destination intersection
        
    Returns:
        Tuple containing:
        - List of intersection IDs representing the path
        - Total path cost/weight
        
    Raises:
        ValueError: If start or end intersections don't exist or if no path exists
    """
    #Verification for start and end ids 
    if start_id not in network.intersections:
        raise ValueError(f"Start intersection {start_id} does not exist")
    if end_id not in network.intersections:
        raise ValueError(f"End intersection {end_id} does not exist")
    
    #The end intersection (goal) that will be used for the heuristic 
    end_intersection = network.intersections[end_id]
    
    #Heuristic function
    def heuristic(intersection_id):
        """
        Using the manhattan distance
        Calculate straight-line distance to goal as heuristic

        Args:
            intersection_id: The id for the current intersection

        Returns: 
            euclidean distance to the end interection from the provided intersection
        """
        current = network.intersections[intersection_id]
        # Euclidean distance formula
        return math.sqrt(
            (current.x - end_intersection.x) ** 2 + 
            (current.y - end_intersection.y) ** 2
        )
    

    """
    A* will use a priority queue for A* algorithm:
        It has the format: (f_score, current_distance, intersection_id)
        Will use the current_distance as a tie-breaker for equal f_scores
        f_score = current_distance (g_score) + heuristic
    """ 
    start_f_score = heuristic(start_id)
    priority_queue = [(start_f_score, 0, start_id)]
    
    #Dictionary to keep track of g_scores (distance from start)
    g_scores = {start_id: 0}
    
    #Dictionary to keep track of f_scores (g_score + heuristic)
    f_scores = {start_id: start_f_score}
    
    #Dictionary to keep track of predecessors for path reconstruction
    predecessors = {}
    
    #Set to keep track of visited nodes
    visited = set()
    
    while priority_queue:
        #Get the intersection with the smallest f_score
        current_f_score, current_distance, current_id = heapq.heappop(priority_queue)
        
        #If we've reached the destination, we can stop
        if current_id == end_id:
            break
            
        #Skip if we've already processed this intersection
        if current_id in visited:
            continue
            
        #Mark as visited
        visited.add(current_id)
        
        #Check all neighbors
        for neighbor_id, weight in network.adjacency_list[current_id]:
            #Skip if neighbor has been visited
            if neighbor_id in visited:
                continue
                
            #Calculate new g_score (distance from start)
            tentative_g_score = current_distance + weight
            
            #If we found a shorter path to the neighbor
            if neighbor_id not in g_scores or tentative_g_score < g_scores[neighbor_id]:
                #Update predecessor
                predecessors[neighbor_id] = current_id
                
                #Update g_score
                g_scores[neighbor_id] = tentative_g_score
                
                #Calculate and update f_score
                f_score = tentative_g_score + heuristic(neighbor_id)
                f_scores[neighbor_id] = f_score
                
                #Add to priority queue
                heapq.heappush(priority_queue, (f_score, tentative_g_score, neighbor_id))
    
    #If we couldn't reach the destination
    if end_id not in predecessors and start_id != end_id:
        raise ValueError(f"No path exists from {start_id} to {end_id}")
    
    #Reconstruct the path
    path = []
    current = end_id
    
    #If start and end are the same, return a single-node path
    if start_id == end_id:
        return [start_id], 0
        
    #Trace back from end to start
    while current != start_id:
        path.append(current)
        current = predecessors[current]
        
    #Add the start node
    path.append(start_id)
    
    #Reverse to get path from start to end
    path.reverse()
    
    return path, g_scores[end_id]