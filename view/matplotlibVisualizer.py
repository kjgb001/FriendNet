from .visualizerBase import VisualizerBase
import matplotlib.pyplot as plt
import networkx as nx

class MatplotlibVisualizer(VisualizerBase):

    def __init__(self, simulation):
        plt.ion() # interactive mode
        self.fig, self.ax = plt.subplots()
        self.positions = {} # node positions

        plt.show()
        self.redraw(simulation)
        

    def redraw(self, simulation):
        nx_graphs = self.gen_nx_graphs(simulation)
        nx_friend_graph = nx_graphs[0]
    
        if self.positions is None or len(self.positions) != nx_graphs[0].number_of_nodes():
            self.positions = nx.spring_layout(nx_friend_graph)

        self.ax.clear()
        nx.draw_networkx_edges(nx_friend_graph, self.positions, ax=self.ax)
        nx.draw_networkx_nodes(nx_friend_graph, self.positions, ax=self.ax)
        nx.draw_networkx_labels(nx_friend_graph, self.positions, ax=self.ax)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        plt.pause(0.001)