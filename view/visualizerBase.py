from abc import ABC, abstractmethod
from core.matrixGraph import *
import networkx as nx

class VisualizerBase(ABC):
        
    @abstractmethod
    def redraw(self, simulation):
        pass

    def gen_nx_graphs(self, simulation):
        gossip = False
        trust = False
        # Initialize networkx graphs based on what is present, and set bools accordingly
        nx_friend_graph = nx.Graph()
        if "gossip" in simulation.graphs:
            nx_gossip_graph = nx.DiGraph()
            gossip = True
        if "trust" in simulation.graphs:
            nx_trust_graph = nx.DiGraph()
            trust = True

        # Add vertices to networkx graphs from friends graph
        for person in simulation.graphs["friends"].vertices:
            nx_friend_graph.add_node(person)
            if gossip:
                nx_gossip_graph.add_node(person)
            if trust:
                nx_trust_graph.add_node(person)

        # Add edges to networkx graphs, checking if friends graph is weighted or not
        if type(simulation.graphs["friends"]) == WU_MatrixGraph:
            for (a, b) in simulation.graphs["friends"].edges:
                nx_friend_graph.add_edge(a, b, weight = 
                    simulation.graphs["friends"].get_edge(a, b))
        else:
            for (a, b) in simulation.graphs["friends"].edges:
                nx_friend_graph.add_edge(a, b)

        if gossip:
            for (a, b) in simulation.graphs["gossip"].edges:
                nx_gossip_graph.add_edge(a, b)
        if trust:
            for (a, b) in simulation.graphs["trust"].edges:
                nx_trust_graph.add_edge(a, b, weight = 
                    simulation.graphs["trust"].get_edge(a, b))
        
        # Gather graphs into a set for return. Sets Nones to keep indexing consistent.
        graphs = [nx_friend_graph]
        if gossip:
            graphs.append(nx_gossip_graph)
        else:
            graphs.append(None)
        if trust:
            graphs.append(nx_trust_graph)
        else:
            graphs.append(None)

        return graphs