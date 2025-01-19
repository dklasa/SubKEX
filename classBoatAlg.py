import random

class BoatAlg:
    def __init__(self, graph):
        self.graph = graph
        
        # Get all available nodes excluding start and end nodes
        self.patrol_nodes = [
            node for node in self.graph.nodes.keys()
            if node not in self.graph.start_nodes and node not in self.graph.end_nodes
        ]

        # Initialize the visit count for each patrol node
        self.visited_count = {node: 0 for node in self.patrol_nodes}

    def calc_move(self, current_position):
        """
        Determines the next move for the boat.
        Selects the least visited node among patrol nodes with randomness.
        """
        # Mark the current position as visited
        self.visited_count[current_position] += 1

        # Find the minimum visit count among all patrol nodes
        min_visits = min(self.visited_count.values())

        # Get all nodes that have been visited the least number of times
        least_visited_nodes = [node for node, count in self.visited_count.items() if count == min_visits]

        # Randomly select one of the least visited nodes to move to
        next_position = random.choice(least_visited_nodes)

        return next_position