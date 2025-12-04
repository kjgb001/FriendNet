from matrixgraph import MatrixGraph
from graphInterface import GraphInterface
from node import *
import uuid
import random

class Rumor():

    def __init__(self, graph, spreader, target, rumor, trust = None):
        self.uid = uuid.uuid4()
        self.friend_graph = check_friend_graph(graph)

        rumor_graph = MatrixGraph(v for v in self.friend_graph.vertices)
        self.graph = rumor_graph

        self.spreader = spreader
        self.target = target
        self.rumor = rumor

        if trust:
            self.trust_graph = check_trust_graph(trust)
        else:
            self.trust_graph = trust

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
            raise ValueError(f"Rumor: Friend graph is empty.")


    def update_rumor_graph_vertices(graph):
        self.friend_graph = check_graph(graph)
        
        for i in range(len(graph)):
            if graph.vertices[i] not in self.graph.vertices:
                self.graph.add_vertex(graph.vertices[i])


    def spread_rumor(self, spreader, target, rumor):
        spreader_friends = self.friend_graph.get_connections(spreader)

        ''' TODO: have spreader attempt to spread the rumor to their friends randomly if unweighted graph,
                else start from closest friends with randomness baked in. Then, if trust graph present,
                use trust score in helper function that determines if the friend continues propogation. '''


    def get_id():
        return self.uid