from core.matrixGraph import *
from core.simEngine import Simulation
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

    # Use args to set graph types
    graphs = build_graphs(args.rep, load_list)

    # Call start here once profile generation and preloaded network setups are ready
    pop_bool = True if args.populate else False
    #sim_init(pop_bool)

    parser = Parser()
    interface = Interface(graphs, parser)
    interface.run()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run FriendNet simulation")

    # List based graphs not implemented yet, this does nothing
    parser.add_argument(
        "--rep",
        choices=["matrix", "list"],
        default="matrix",
        help="Choose graph representation: matrix or list"
    )

    parser.add_argument(
        "--load",
        default="all",
        help="Comma-separated list of graphs to load: undirected,directed,weighted,dag"
    )

    parser.add_argument(
        "--populate",
        help="Determines if the graph will be auto-populated by the simulation"

    )

    return parser.parse_args()


def build_graphs(rep, load_list):
    graphs = {}

    if "weighted" in load_list:
        graphs["friends"] = (
            WU_MatrixGraph(None, None, None) #if rep == "matrix"
        )
        graphs["trust"] = (
            W_MatrixGraph(None, None, None) #if rep == "matrix"
        )
    elif "undirected" in load_list:
        graphs["friends"] = (
            U_MatrixGraph(None, None) #if rep == "matrix"
        )

    if "directed" in load_list:
        graphs["gossip"] = (
            MatrixGraph(None, None) #if rep =="matrix"
        )

    # Add DAG once implemented

    return graphs

# initialize Simulation object
def sim_init(pop_bool):
    pass
