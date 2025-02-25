import random
from classBoatAlg import BoatAlg

# game logic fo the game
class GameLogic:
    def __init__(self, graph, start_pos_s):
        self.graph = graph
        
        # Set initial positions
        self.sub_pos = start_pos_s
        all_nodes = list(self.graph.nodes.keys())
        possible_boat_starts = [n for n in all_nodes if n not in self.graph.start_nodes]
        self.boat_pos = random.choice(possible_boat_starts)
        #Coment... :-3
        # initializing algorithm
        self.boat_a = BoatAlg(self.graph)

    # moving the sub
    def sub_move(self):
        self.sub_pos = self.sub_algorithm()
        return self.sub_pos

    # moving the boat
    def boat_move(self):
        self.boat_pos = self.boat_a.calc_move(self.boat_pos)
        return None

    # check if game over, first if sub reached end node then if boat caught sub
    def check_game_over(self):
        if self.sub_pos in self.graph.end_nodes:
            return 1
        elif self.sub_pos == self.boat_pos:
            return -1
        else:
            return 0