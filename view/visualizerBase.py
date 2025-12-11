from abc import ABC, abstractmethod
from core.matrixGraph import *
import networkx as nx

class VisualizerBase(ABC):
        
    @abstractmethod
    def redraw(self, simulation):
        pass

    @abstractmethod
    def close(self):
        pass

    def _add_vertices(self, simulation, graph):
        # Add vertices to networkx graphs from friends graph
        for person in simulation.graphs["friends"].vertices:
            graph.add_node(person)


    def _friends_graph(self, simulation, graph):
        # Add edges to friends graph, checking if friends graph is weighted or not
        if type(simulation.graphs["friends"]) == WU_MatrixGraph:
            for (a, b) in simulation.graphs["friends"].edges:
                graph.add_edge(
                    simulation.graphs["friends"].vertices[a], 
                    simulation.graphs["friends"].vertices[b], 
                    weight = simulation.graphs["friends"].get_edge(a, b)
                )
        else:
            for (a, b) in simulation.graphs["friends"].edges:
                graph.add_edge(
                    simulation.graphs["friends"].vertices[a], 
                    simulation.graphs["friends"].vertices[b]
                )


    def _gossip_graph(self, simulation, graph, rumor):
        for (a, b) in rumor.graph.edges:
                graph.add_edge(
                    simulation.graphs["gossip"].vertices[a], 
                    simulation.graphs["gossip"].vertices[b]
                )


    def _trust_graph(self, simulation, graph):
        for (a, b) in simulation.graphs["trust"].edges:
                graph.add_edge(
                    simulation.graphs["trust"].vertices[a], 
                    simulation.graphs["trust"].vertices[b], 
                    weight = simulation.graphs["trust"].get_edge(a, b)
                )
        

    def gen_nx_graphs(self, simulation, graph_to_gen, rumor):
        if graph_to_gen == 0:
            nx_graph = nx.Graph()
            self._add_vertices(simulation, nx_graph)
            self._friends_graph(simulation, nx_graph)
        else:
            nx_graph = nx.DiGraph()
            self._add_vertices(simulation, nx_graph)

            if graph_to_gen == 1 and rumor:
                self._gossip_graph(simulation, nx_graph, rumor)
            else:
                self._trust_graph(simulation, nx_graph)
        
        return nx_graph
        