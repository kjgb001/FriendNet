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
            if person:
                graph.add_node(person)


    def _friends_graph(self, simulation, graph):
        # Add edges to friends graph, checking if friends graph is weighted or not
        if type(simulation.graphs["friends"]) == WU_MatrixGraph:
            vertices = simulation.graphs["friends"].get_vertices()
            for (a, b) in simulation.graphs["friends"].get_edges():
                u = vertices[a]
                v = vertices[b]

                if u is None or v is None:
                    continue  # skip dead edges

                graph.add_edge(
                    u, v, weight = simulation.graphs["friends"].get_edge(a, b)
                )
        else:
            vertices = simulation.graphs["friends"].get_vertices()
            for (a, b) in simulation.graphs["friends"].get_edges():
                u = vertices[a]
                v = vertices[b]

                if u is None or v is None:
                    continue  # skip dead edges
                graph.add_edge(
                    u, v
                )


    def _gossip_graph(self, simulation, graph, rumor):
        vertices = rumor.graph.get_vertices()
        for (a, b) in rumor.graph.get_edges():
            u = vertices[a]
            v = vertices[b]

            if u is None or v is None:
                continue  # skip dead edges

            graph.add_edge(
                u, v
            )


    def _trust_graph(self, simulation, graph):
        vertices = simulation.graphs["trust"].get_vertices()
        for (a, b) in simulation.graphs["trust"].get_edges():
            u = vertices[a]
            v = vertices[b]

            if u is None or v is None:
                continue  # skip dead edges
            graph.add_edge(
                u, v, weight = simulation.graphs["trust"].get_edge(a, b)
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
        