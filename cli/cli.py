from core.matrixGraph import *
from core.listGraph import *
from core.simulation import Simulation
from .interface import Interface
from .parser import Parser
import argparse


def main():
    args = parse_arguments()

    # Turn load string into list
    if args.load == "all":
        load_list = ["undirected", "directed", "weighted", "dag"]
    else:
        load_list = args.load.split(",")

    parser = Parser()
    interface = Interface(parser)

    # Start simulation with args if populate
    populate = args.populate
    location = args.location
    if populate:
        # Use args to set graph types
        graphs = build_graphs(args.rep, load_list)
        # Sim init
        sim = Simulation(graphs, interface, populate, location)
        # Pass simulation to interface and start the cli interface
        interface.sim = sim
    else:
        # TODO: init startup GUI, pass interface
        pass
    
    interface.run()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run FriendNet simulation")
    
    parser.add_argument(
        "--rep",
        choices=["matrix", "list"],
        default="list",
        help="Choose graph representation: matrix or list"
    )

    # Could replace with automatic detection that checks to see if the graphs have any properties after init.
    parser.add_argument(
        "--load",
        default="all",
        help="Comma-separated list of graphs to load: undirected,directed,weighted,dag"
    )

    parser.add_argument(
        "--populate",
        nargs = "?",
        const = 50,
        type = int,
        default = None,
        help="Auto-populate the graph on startup with n people"
    )

    parser.add_argument(
        "--location",
        default = "generated_set",
        type = str,
        help="Choose which directory to store and retrieve people from."
    )

    return parser.parse_args()


def build_graphs(rep, load_list):

    graphs = {}

    if "weighted" in load_list:
        graphs["friends"] = (
            WeightedUndirectedMatrixGraph() if rep == "matrix" else WeightedUndirectedListGraph()
        )
        graphs["trust"] = (
            WeightedDirectedMatrixGraph() if rep == "matrix" else WeightedDirectedListGraph()
        )
    elif "undirected" in load_list:
        graphs["friends"] = (
            UndirectedMatrixGraph() if rep == "matrix" else UndirectedListGraph()
        )

    if "directed" in load_list:
        graphs["gossip"] = (
            DirectedMatrixGraph() if rep =="matrix" else DirectedListGraph()
        )

    # Add DAG once implemented

    return graphs
