import random
from classBoatAlg import BoatAlg
from classSubAlg import SubAlg

# game logic fo the game
class GameLogic:
    def __init__(self, graph):
        self.graph = graph

        # Ensure start nodes are available
        if not self.graph.start_nodes:
            raise ValueError("No start nodes defined in the graph.")
        
        # Set initial positions
        self.sub_pos = random.choice(self.graph.start_nodes)
        all_nodes = list(self.graph.nodes.keys())
        possible_boat_starts = [n for n in all_nodes if n not in self.graph.start_nodes]

        if not possible_boat_starts:
            raise ValueError("No valid boat start nodes available (all are start nodes?).")

        self.boat_pos = random.choice(possible_boat_starts)

        # initializing algorithms
        self.boat_a = BoatAlg(self.graph)
        self.sub_a = SubAlg()

    # moving the sub
    def sub_move(self):
        self.sub_pos = self.sub_algorithm()
        return self.check_game_over()

    # moving the boat
    def boat_move(self):
        self.boat_pos = self.boat_a.calc_move(self.boat_pos)
        return self.check_game_over()

    # check if game over, first if sub reached end node then if boat caught sub
    def check_game_over(self):
        if self.sub_pos in self.graph.end_nodes:
            return "The Sub has reached an end node and escaped!"
        if self.sub_pos == self.boat_pos:
            return "The Boat has caught The Sub!"
        return None

    # algorithm for determing next move sub
    def sub_algorithm(self):
        neighbors = self.graph.neighbors(self.sub_pos)
        neighbors_valid = [n for n in neighbors if n > self.sub_pos]
        return random.choice(neighbors_valid)