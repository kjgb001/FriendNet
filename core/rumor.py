from matrixgraph import MatrixGraph
from graphInterface import GraphInterface
from node import *
import uuid
import random

class Rumor():

    def __init__(self, graph, spreader, target, rumor, trust = None):
        self.uid = uuid.uuid4()
        self.friend_graph = check_friend_graph(graph)

        rumor_graph = MatrixGraph((v for v in self.friend_graph.vertices), None)
        self.graph = rumor_graph

        self.spreader = spreader
        self.target = target
        self.rumor = rumor

        self.visited = set() # Used to ensure spread_rumor does not infinitely recurse

        if trust:
            self.trust_graph = check_trust_graph(trust)

        spread_rumor(spreader, target, rumor)


    def check_friend_graph(self, graph):
        if isinstance(graph, GraphInterface):
            raise TypeError(f"Rumor: Friend graph must be a graph, got {type(graph)}.")

        if len(graph) < 1:
            raise ValueError(f"Rumor: Friend graph is empty.")


    def check_trust_graph(self, graph):
        if type(graph) != W_MatrixGraph:
            raise TypeError(f"Rumor: Trust graph must be a Weighted Directed graph, got {type(graph)}.")

        if len(graph) < 1:
            raise ValueError(f"Rumor: Trust graph is empty.")


    def update_rumor_graph_vertices(graph):
        self.friend_graph = check_graph(graph)
        
        for i in range(len(graph)):
            if graph.vertices[i] not in self.graph.vertices:
                self.graph.add_vertex(graph.vertices[i])


    def spread_rumor(self, spreader, rumor):
        spreader_friends = self.friend_graph.get_connections(spreader)
        spread_bool = False
        trust_level = 0

        self.visited.add(spreader)

        ''' TODO: have spreader attempt to spread the rumor to their friends randomly if unweighted graph,
                else start from closest friends with randomness baked in. Then, if trust graph present,
                use trust score in helper function that determines if the friend continues propogation. '''
        
        for friend in spreader_friends:
            # TODO: Make rumors spread more strongly through close friends by checking edge strength and altering spread RNG

            # Determine if rumor will propogate further
            if self.trust_graph:
                trust_level = self.trust_graph.get_edge(friend, spreader) - 1 # subtract one to normalize value
                spread_bool = random.random() < trust_level
            else:
                spread_bool = random.randint(0, 1) == 1

            # If the friend hasn't already heard the rumor and 
            if friend not in visited and spread_bool:
                self.graph.add_edge(spreader, friend)
                spread_rumor(friend, rumor)
                    


    def get_id():
        return self.uid