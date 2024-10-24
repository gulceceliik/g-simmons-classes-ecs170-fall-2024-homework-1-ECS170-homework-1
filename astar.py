from tiles import TilesNode
from queue import PriorityQueue

def heuristic(node: TilesNode) -> int:
    """
    Evaluate the heuristic value of the current node.
    This implementation simply counts the number of misplaced tiles.

    Returns
    -------
    heuristic_value : int
        The heuristic value of the current node.
    """
    goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    if not isinstance(node, TilesNode):
        raise TypeError(f"Expected TilesNode, got {type(node).__name__}")
    
    node.goal_state = goal_state  # Assign goal_state attribute of node to a local variable goal_state 
    misplaced_tile_count = 0 
    
    for i in range(len(node.state)):
        for j in range(len(node.state[i])):
            tile = node.state[i][j] 
            goal_tile= node.goal_state[i][j]
            if tile != goal_tile and tile != 0:
                misplaced_tile_count += 1 

    return misplaced_tile_count


def AStar(root: TilesNode, heuristic: callable) -> list["TilesNode"] or None:  # type: ignore
    unexplored = PriorityQueue()
    counter = 0
    unexplored.put((0, counter, root))
    explored = set() # This set keeps track of explored nodes 
    g_score = {root: 0} #Cost from root to the current node 
    f_score = {root: heuristic(root)} #Total estimated cost of the cheapest solution 

    while not unexplored.empty(): #The loop continues as long as there are nodes left to explore 
        current_node = unexplored.get()[2]     
        #Checking if we've reached the goal state 
        if current_node.is_goal():
            return current_node.get_path()  # Return the goal node if current_node is the goal state 
        
        explored.add(current_node)

        for child in current_node.get_children():
            if child in explored:
                continue
        
            new_g_score = g_score[current_node] + 1
            if child not in g_score or new_g_score < g_score[child]:
                g_score[child] = new_g_score
                f_score[child] = new_g_score + heuristic(child)

                # Add the child node to the unexplored queue with its f_score
                unexplored.put((f_score[child], counter, child))
                counter += 1
    
    return None  # Return None if no path was found
