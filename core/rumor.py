from core.matrixGraph import MatrixGraph
from core.graphInterface import GraphInterface
from core.node import *
import uuid
import random

class Rumor():

    def __init__(self, friend_graph, spreader, target, rumor, trust = None):
        ''' Rumor class to store rumor information, query stored information, propogate rumors, and trace their propogation. '''
        self.uid = uuid.uuid4()
        self.friend_graph = self.check_friend_graph(friend_graph)

        rumor_graph = MatrixGraph(list(self.friend_graph.vertices), None)
        self.graph = rumor_graph

        self.spreader = spreader
        self.target = target
        self.rumor = rumor

        self.visited = set() # Used to ensure spread_rumor does not infinitely recurse

        if trust:
            self.trust_graph = self.check_trust_graph(trust)
        else:
            self.trust_graph = trust

        self.spread_rumor(spreader)


    def check_friend_graph(self, graph):
        if not isinstance(graph, GraphInterface):
            raise TypeError(f"Rumor: Friend graph must be a graph, got {type(graph)}.")

        if len(graph) < 1:
            raise ValueError(f"Rumor: Friend graph is empty.")

        return graph


    def check_trust_graph(self, graph):
        if type(graph) != W_MatrixGraph:
            raise TypeError(f"Rumor: Trust graph must be a Weighted Directed graph, got {type(graph)}.")

        if len(graph) < 1:
            raise ValueError(f"Rumor: Trust graph is empty.")

        return graph


    def update_graphs(self, graph):
        ''' Takes in a graph to replace the current friend graph, and adds vertices from this graph to the rumor graph if not present. ''' 
        self.friend_graph = self.check_friend_graph(graph)
        
        for i in range(len(graph)):
            if graph.vertices[i] not in self.graph.vertices:
                self.graph.add_vertex(graph.vertices[i])


    def spread_rumor(self, spreader = None):
        ''' Recursive function that takes in the rumor info and spreads to connected vertices based on weights and RNG. '''
        if not spreader:
            spreader = self.spreader
        
        spreader_friends = self.friend_graph.get_connections(spreader)
        spread_bool = False
        selection_chance = 0
        trust_level = 0

        self.visited.add(spreader)
        
        for friend in spreader_friends:
            # Make rumors spread semi-randomly and more strongly through close friends by checking edge strength and introducing a new RNG bool variable
            if type(self.friend_graph) == WU_MatrixGraph:
                selection_chance = (self.friend_graph.get_edge(spreader, friend) - 1) * 1.5 # subtract one to normalize value then increase by 50% to soften probabilistic curve
                selected = random.random() < selection_chance
            else:
                # In case of unweighted friend graph use blind RNG (adjust number to change chance, higher = more likely)
                selected = random.random() < 0.75

            # Determine if rumor will propogate to this friend
            if selected:
                if self.trust_graph:
                    trust_level = self.trust_graph.get_edge(friend, spreader) - 1 # subtract one to normalize value
                    spread_bool = random.random() < trust_level
                else:
                    spread_bool = random.randint(0, 1) == 1

            # If the friend hasn't already heard the rumor and it is set to spread, add edge to trust graph and recurse
            if friend not in self.visited and spread_bool:
                self.graph.add_edge(spreader, friend)
                self.spread_rumor(friend)


    def get_id(self):
        return self.uid
    
    def get_rumor_graph(self):
        return self.graph

    def get_spreader(self):
        return self.spreader

    def get_target(self):
        return self.target

    def get_rumor(self):
        return self.rumor


    def __len__(self):
        # Count edges in the rumor graph
        edge_count = sum(
            1 for i in range(len(self.graph.vertices))
            for j in range(len(self.graph.vertices))
            if self.graph.get_edge(i, j) not in (None, 0)
        )
        return edge_count


    def __str__(self):
        '''Return a human-readable summary of the rumor and its propagation.'''
        lines = [
            f"Rumor ID: {self.uid}",
            f"Spreader: {self.spreader}",
            f"Target: {self.target}",
            f"Rumor Content: \"{self.rumor}\"",
            "",
        ]

        # List visited names, if any
        if self.visited:
            filtered = [str(v) for v in self.visited if v != self.spreader]
            visited_list = ", ".join(filtered) if len(filtered) > 0 else "None"
            lines.append(f"People Who Have Heard It: {visited_list}")
        else:
            lines.append("People Who Have Heard It: None")

        lines.append(f"Times Rumor was Spread: {self.__len__()}")

        return "\n".join(lines)
