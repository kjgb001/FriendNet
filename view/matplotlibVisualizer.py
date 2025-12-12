from .visualizerBase import VisualizerBase
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import transforms
import networkx as nx
import math

class MatplotlibVisualizer(VisualizerBase):

    def __init__(self, simulation):
        plt.ion() # interactive mode
        self.fig, self.ax = plt.subplots()
        self.positions = {} # node positions
        self.page = 0 # Which graph to display when redraw is called
        
        self.portrait_zoom = 0.3 # adjust as needed
        self.image_cache = {
            person: OffsetImage(mpimg.imread(path), zoom = self.portrait_zoom)
            for person, path in simulation.image_map.items()}

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
            # Build a graph containing ONLY friend edges
            layout_graph = nx.Graph()
            layout_graph.add_nodes_from(nx_graph.nodes)

            for u, v, data in nx_graph.edges(data=True):
                if data.get("weight", 1.5) > 1.5:
                    layout_graph.add_edge(u, v, weight = data["weight"] - 1.0)

            scale = 2 + math.log(simulation.count) # Area grows with log(n)
            # Compute the theoretical FR optimal edge length
            area = (2 * scale) ** 2
            k = 0.75 * math.sqrt(area / simulation.count)
            # Increase k by a factor proportional to the portrait radius
            portrait_radius = 64 * self.portrait_zoom # change first number if size of images changes
            k *= 1 + (portrait_radius / 40) # denominator can be adjusted

            self.positions = nx.spring_layout(layout_graph, weight="weight", k=k, # increases desired inter-node distance
                                            iterations=300, scale=scale) # spreads clusters outward

        # Clear the visualization for redraw
        self.ax.clear()

        # Set colors and widths for edges
        colors = []
        widths = []

        for u, v in nx_graph.edges():
            w = nx_graph[u][v].get("weight", 1.5) # default to neutral

            # Set color
            if w > 1.55:
                colors.append("green")
            elif w < 1.45:
                colors.append("red")
            else:
                colors.append("gray")

            # Gets width by finding absolute distance from neutral then scaling
            if colors[-1] == "gray":
                width = 2.5
            else:
                width = 1 + abs(w - 1.5) * 5

            # Set width
            widths.append(width)

        # Reference dict for label positions
        label_positions = {
            node: (x, y - 0.5)   # adjust offset as needed
            for node, (x, y) in self.positions.items()
        }

        # Draw in networkx based on which page is active. 
        if self.page == 0: # Friend Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax, 
                edge_color = colors, width = widths)
            self.draw_node_images(self.ax, self.positions)
            self.draw_labels()
        elif self.page == 1: # Gossip Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax,
                arrows = True)
            self.draw_node_images(self.ax, self.positions)
            self.draw_labels(nx_graph, label_positions)
        else: # Trust Graph
            nx.draw_networkx_edges(nx_graph, self.positions, ax = self.ax,
                edge_color = colors, width = widths, style = "dotted")
            self.draw_node_images(self.ax, self.positions)
            self.draw_labels(nx_graph, label_positions)

        # Draw to matplotlib figure, flush, and pause for smoothness
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)


    def draw_node_images(self, ax, positions):
        for person, (x,y) in self.positions.items():
            ab = AnnotationBbox(self.image_cache[person], (x, y), frameon=False)
            self.ax.add_artist(ab)

    def draw_labels(self):
        for person, (x, y) in self.positions.items():
            # Pixel offset for label below image
            offset = transforms.ScaledTranslation(0, -20 / 72, self.ax.figure.dpi_scale_trans)

            text_transform = self.ax.transData + offset

            self.ax.text(
                x,
                y,
                f"{person.data.fname} {person.data.lname}",   # or full name
                transform=text_transform,
                ha='center',
                va='top',
                bbox=dict(
                    facecolor='white', 
                    edgecolor='black', 
                    boxstyle='round,pad=0.2',
                    alpha=0.8
                )
            )

