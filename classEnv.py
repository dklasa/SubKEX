import gymnasium as gym
from gym.spaces import Discrete, Dict
import numpy as np
import random
from classGame import GameLogic

class GameEnv(gym.Env):
    def __init__(self, graph):
        self.graph = graph

        max = 0
        for k in self.graph.nodes.keys():
            if len(self.graph.adjacency[k]) > max:
                max = len(self.graph.adjacency[k])
        
        # blir det problem när färre antal valmöjligheter än max? hur lösa?
        self.action_space = Discrete(max)
        self.observation_space = Dict({"is_start":Discrete(2), "is_end":Discrete(2), "neighbors":Discrete(max)})

        # ett spel får inte vara längre än 100 drag
        self.game_length = 100

        # randomiserar vart ubåten startar
        self.state = random.choice(self.graph.start_nodes)
        self.game_logic = GameLogic(graph, self.state)

    def reset(self):
        # startar om spelet
        self.game_length = 100
        self.state = random.choice(self.graph.start_nodes)
        self.game_logic = GameLogic(self.graph, self.state)
        return self.state

    def step(self, action):
        # ett drag gjort
        self.game_length -= 1

        # draget är till den noden den vill gå, blir nytt state
        self.state = action
        
        # uppdaterar game logic
        self.game_logic.sub_pos = self.state
        self.game_logic.boat_move()

        # om ubåten står på en slut nod -> reward = 1
        reward = self.game_logic.check_game_over()

        # kollar om klar med spelet
        if self.game_length == 0 or reward != 0:
            done = True
        else:
            done = False

        return self.state, reward, done

    # för GUI -> lägg in senare
    def render(self, mode='human'):
        pass