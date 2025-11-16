from core.matrixGraph import *

def add_person(graphs, person):
    # Add the person to each graph
    for graph in graphs.values():
        graph.add_vertex(person)

    print(f"{person} successfully added!")


def remove_person(graphs, person):
    # Remove the person from each graph
    for graph in graphs.values():
        graph.remove_vertex(person)

    print(f"{person} successfully removed.")


def connect(graphs, a, b, weight = None):
    # Check which type of graph is used for friends, then add edge
    if isinstance(graphs["friends"], U_MatrixGraph):
        graphs["friends"].add_edge(a, b)
    else:
        graphs["friends"].add_edge(a, b, weight)

    print(f"{a} and {b} are now friends!")


def disconnect(graphs, a, b):
    graphs["friends"].remove_edge(a, b)

    print(f"{a} and {b} are no longer friends.")


def print_people(graphs):
    people = graphs["friends"].vertices

    print("\nAll people present:\n")
    for person in sorted(people):
        print(f"    {person}")
    print()


def help_user(graphs, commands):
    # Print the commands that are available based on graphs
    print("\nAvailable commands:\n")
    for cmd in sorted(commands):
        print(f"    {cmd}")
    print()