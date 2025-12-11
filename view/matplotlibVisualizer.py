from .visualizerBase import VisualizerBase
import matplotlib.pyplot as plt
import networkx as nx

class MatplotlibVisualizer(VisualizerBase):

    def __init__(self, simulation):
        plt.ion() # interactive mode
        self.fig, self.ax = plt.subplots()
        self.positions = {} # node positions
        self.page = 0 # Which graph to display when redraw is called

        def _on_close(event):
            import sys
            sys.exit(0)
        self.fig.canvas.mpl_connect("close_event", _on_close)

        plt.show()
        self.redraw(simulation)

    def close(self):
        plt.close(self.fig)
        

    def redraw(self, simulation, rumor = None):
        # Get graph in networkx form, and determine if rumor should be passed as is
        if self.page != 1:
            rumor = None
        nx_graph = self.gen_nx_graphs(simulation, self.page, rumor)
        
        # Update positions only if they don't exist or node count changes
        if self.positions is None or len(self.positions) != nx_graph.number_of_nodes():
            self.positions = nx.spring_layout(nx_graph)

        # Clear the visualization for redraw
        self.ax.clear()

        # Set colors and widths for edges
        colors = []
        widths = []

        for u, v in nx_graph.edges():
            w = nx_graph[u][v].get("weight", 1.5) # default to neutral

            # Set color
            if w > 1.5:
                colors.append("green")
            elif w < 1.5:
                colors.append("red")
            else:
                colors.append("gray")

            # Gets width by finding absolute distance from neutral then scaling
            width = 1 + abs(w - 1.5) * 5

            # Set width
            widths.append(width)

        # Draw in networkx based on which page is active. 
        if self.page == 0: # Friend Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax, 
                edge_color = colors, width = widths)
            nx.draw_networkx_nodes(nx_graph, self.positions, ax = self.ax)
            nx.draw_networkx_labels(nx_graph, self.positions, ax = self.ax)
        elif self.page == 1: # Gossip Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax,
                arrows = True)
            nx.draw_networkx_nodes(nx_graph, self.positions, ax = self.ax)
            nx.draw_networkx_labels(nx_graph, self.positions, ax = self.ax)
        else: # Trust Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax,
                edge_color = colors, width = widths, style = "dotted")
            nx.draw_networkx_nodes(nx_graph, self.positions, ax = self.ax)
            nx.draw_networkx_labels(nx_graph, self.positions, ax = self.ax)

        # Draw to matplotlib figure, flush, and pause for smoothness
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)