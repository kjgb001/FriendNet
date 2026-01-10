from .visualizerBase import VisualizerBase
import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false" # Force Qt to stop whining about not getting window focus
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import transforms
from PySide6 import QtCore
from PySide6.QtCore import QTimer
import networkx as nx
import math
import time

class MatplotlibVisualizer(VisualizerBase):

    def __init__(self, simulation):
        plt.ion() # interactive mode
        self.fig, self.ax = plt.subplots()
        self.positions = {} # node positions
        self.page = 0 # Which graph to display when redraw is called
        self.sim = simulation
        self.rumor = None

        self.highlighted_node = None   # Person or None
        self._last_hover_redraw = 0
        self._hover_redraw_interval = 0.05  # 50 ms = 20 FPS

        # Qt timer for clearing hover events. Solution to stubborn missed motion events bug.
        self._hover_clear_timer = QTimer()
        self._hover_clear_timer.setSingleShot(True)
        self._hover_clear_timer.timeout.connect(self._clear_hover_timeout)
        
        self.portrait_zoom = 0.3 # adjust as needed
        self.portrait_radius, self.arrow_margin = self._calculate_radii(self.portrait_zoom)
        self.image_cache = {
            person: mpimg.imread(path)
            for person, path in self.sim.image_map.items()
        }

        def _on_close(event):
            # Tell the app to stop
            self.sim.interface.shutdown()

        self.fig.canvas.mpl_connect("close_event", _on_close)
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_hover)

        manager = plt.get_current_fig_manager()
        window = manager.window
        # Force Qt to stop stealing window focus
        window.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        window.setWindowFlag(QtCore.Qt.WindowDoesNotAcceptFocus, True)

        window.show()
        self.redraw()

    def close(self):
        plt.close(self.fig)

    def pump_events(self, interval=0.01):
        import threading
        assert threading.current_thread() is threading.main_thread()
        plt.pause(interval)

    def _calculate_radii(self, portrait_zoom):
        portrait_radius = 64 * portrait_zoom # change first number if size of images changes
        portrait_pts = portrait_radius * 72 / self.fig.dpi
        arrow_margin = portrait_pts + 10 # set to arrow mutation scale

        return portrait_radius, arrow_margin


    def redraw(self, rumor = None):
        # Get graph in networkx form, and determine if rumor should be passed as is
        if self.page != 1:
            rumor = None
        else:
            if not self.rumor:
                self.rumor = self.sim.rumors[-1] # set to latest rumor if none already set
            rumor = self.rumor

        nx_graph = self.gen_nx_graphs(self.sim, self.page, rumor)
        
        # Update positions only if they don't exist or node count changes
        if self.positions is None or len(self.positions) != nx_graph.number_of_nodes():
            # Build a graph containing ONLY friend edges
            layout_graph = nx.Graph()
            layout_graph.add_nodes_from(nx_graph.nodes)

            # Add edges to position graph if they are friendships, with a fallback for un-weighted friend graphs
            for u, v, data in nx_graph.edges(data = True):
                w = data.get("weight")
                if w is None:
                    layout_graph.add_edge(u, v, weight = 0.6)
                elif w > 1.55:
                    layout_graph.add_edge(u, v, weight = w - 1.0)

            scale = 2 + math.log(self.sim.count) # Area grows with log(n)
            # Compute the theoretical FR optimal edge length
            area = (2 * scale) ** 2
            k = 0.75 * math.sqrt(area / self.sim.count)
            # Increase k by a factor proportional to the portrait radius
            k *= 1 + (self.portrait_radius / 40) # denominator can be adjusted

            self.positions = nx.spring_layout(layout_graph, weight="weight", k=k, # increases desired inter-node distance
                                            iterations=300, scale=scale) # spreads clusters outward

        # Clear the visualization for redraw
        self.ax.clear()

        # Set scaling explicitly
        xs = [x for x, y in self.positions.values()]
        ys = [y for x, y in self.positions.values()]

        pad = 0.5  # tweak for breathing room

        self.ax.set_xlim(min(xs) - pad, max(xs) + pad)
        self.ax.set_ylim(min(ys) - pad, max(ys) + pad)

        self.ax.set_aspect("equal", adjustable="box")
        self.ax.axis("off")

        # Highlight visibility logic
        highlight = self.highlighted_node
        if highlight is not None and highlight in nx_graph:
            neighbors = set(nx_graph.neighbors(highlight))
            visible_nodes = neighbors | {highlight}
        else:
            visible_nodes = None

        # Set colors, widths, and alphas for edges
        colors = []
        widths = []
        alphas = []

        for u, v in nx_graph.edges():
            w = nx_graph[u][v].get("weight", 1.75) # default to friend

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

            # Dim edges not connected to highlighted node
            if visible_nodes is not None:
                if u in visible_nodes and v in visible_nodes:
                    alpha = 1.0 if self.page == 0 or u == self.highlighted_node else 0.1 # If directed edges only highlight outgoing edges 
                else:
                    alpha = 0.1
            else:
                alpha = 1.0

            # Set width and alpha
            widths.append(width)
            alphas.append(alpha)

        # Reference dict for label positions
        label_positions = {
            node: (x, y - 0.5)   # adjust offset as needed
            for node, (x, y) in self.positions.items()
        }

        # Draw edges (manual draw to support per-edge alpha)
        for (u, v), color, width, alpha in zip(nx_graph.edges(), colors, widths, alphas):
            x = [self.positions[u][0], self.positions[v][0]]
            y = [self.positions[u][1], self.positions[v][1]]

            linestyle = None
            if self.page == 1:
                color = "black"
            if self.page == 2:
                linestyle = "--"
            else:
                linestlye = "-"

            if self.page == 0:
                self.ax.plot(
                    x, y,
                    color=color,
                    linewidth=width,
                    alpha=alpha,
                    zorder=1,
                    linestyle=linestyle
                )
            else:
                x1, y1 = self.positions[u]
                x2, y2 = self.positions[v]

                arrow = FancyArrowPatch(
                    (x1, y1),
                    (x2, y2),
                    arrowstyle='->',
                    linewidth=width,
                    linestyle=linestyle,
                    color=color,
                    alpha=alpha,
                    mutation_scale=10,
                    shrinkA=self.arrow_margin,
                    shrinkB=self.arrow_margin,
                    zorder=1
                )

                self.ax.add_patch(arrow)

        # Node alpha logic
        node_alphas = {}
        for node in nx_graph.nodes():
            if visible_nodes is not None and node not in visible_nodes:
                node_alphas[node] = 0.2
            else:
                node_alphas[node] = 1.0

        # Draw in networkx based on which page is active. 
        if self.page == 0: # Friend Graph
            self.draw_node_images(self.ax, self.positions, node_alphas)
            self.draw_labels(node_alphas)
        elif self.page == 1: # Gossip Graph
            self.draw_node_images(self.ax, self.positions, node_alphas)
            self.draw_labels(node_alphas)
        else: # Trust Graph
            self.draw_node_images(self.ax, self.positions, node_alphas)
            self.draw_labels(node_alphas)

        # Draw to matplotlib figure, flush, and pause for smoothness
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        plt.pause(0.001)


    def activate_highlight(self, person):
        """Highlight a node and its immediate neighbors."""
        self.highlighted_node = person
        self.sim.interface.redraw_pending = True

    def clear_highlight(self):
        """Disable all highlighting."""
        self.highlighted_node = None
        self.sim.interface.redraw_pending = True

    def _on_hover(self, event):
        now = time.time()
        if now - self._last_hover_redraw < self._hover_redraw_interval:
            return
        self._last_hover_redraw = now

        # Tweak ms amounts to liking
        if event.inaxes != self.ax:
            self._hover_clear_timer.start(40) # ms
            return

        person = self._pick_node_at_event(event)

        if person is not None:
            self._hover_clear_timer.stop()
            if person != self.highlighted_node:
                self.highlighted_node = person
                self.redraw()
        else:
            # No node detected: schedule clear shortly
            self._hover_clear_timer.start(40)

    def _pick_node_at_event(self, event, radius_px=30):
        """
        Return the closest node within radius_px of the mouse event,
        or None if nothing is close enough.
        """
        if event.x is None or event.y is None:
            return None

        # Convert node positions to screen space
        for person, (x, y) in self.positions.items():
            sx, sy = self.ax.transData.transform((x, y))
            dx = sx - event.x
            dy = sy - event.y
            if dx*dx + dy*dy <= radius_px * radius_px:
                return person

        return None

    def _clear_hover_timeout(self):
        if self.highlighted_node is not None:
            self.highlighted_node = None
            self.redraw()


    def draw_node_images(self, ax, positions, node_alphas=None):
        for person, (x, y) in positions.items():
            visible = True
            if node_alphas is not None:
                # Qt backend refuses to show updated per-artist alphas so this is the current solution
                visible = node_alphas.get(person, 1.0) > 0.5

            img = OffsetImage(
                self.image_cache[person],
                zoom=self.portrait_zoom
            )

            ab = AnnotationBbox(
                img,
                (x, y),
                frameon=False,
                zorder=2
            )
            ab.set_visible(visible)
            ax.add_artist(ab)

    def draw_labels(self, node_alphas=None):
        for person, (x, y) in self.positions.items():
            alpha = node_alphas.get(person, 1.0) if node_alphas else 1.0

            offset = transforms.ScaledTranslation(
                0, -20 / 72, self.ax.figure.dpi_scale_trans
            )
            text_transform = self.ax.transData + offset

            self.ax.text(
                x,
                y,
                f"{person.data.fname} {person.data.lname}",
                transform=text_transform,
                ha='center',
                va='top',
                alpha=alpha,
                zorder=3,
                bbox=dict(
                    facecolor='white',
                    edgecolor='black',
                    boxstyle='round,pad=0.2',
                    alpha=0.8 * alpha
                )
            )
