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
        print(f"{a} and {b} are now friends!")
    else:
        graphs["friends"].add_edge(a, b, weight)

        if weight:
            if weight > 1.5:
                print(f"{a} and {b} are now friends!")
            elif weight < 1.5:
                print(f"{a} and {b} are now enemies.")
            else:
                print(f"{a} and {b} are now acquainted.")


def disconnect(graphs, a, b):
    graphs["friends"].remove_edge(a, b)

    print(f"{a} and {b} are no longer acquainted.")


def strengthen_edge(graphs, a, b, weight):

    if graphs["friends"].get_edge(a, b) == 2.0:
        print(f"{a} and {b} are already best friends!")
        return

    graphs["friends"].strengthen_edge(a, b, weight)

    if graphs["friends"].get_edge(a, b) == 2.0:
        print(f"{a} and {b} are now best friends!")
    elif graphs["friends"].get_edge(a, b) == 1.5:
        print(f"{a} and {b} have a neutral relationship.")
    elif graphs["friends"].get_edge(a, b) > 1.5:
        print(f"{a} and {b} are now better friends!")
    else:
        print(f"{a} and {b} still dislike each other.")


def weaken_edge(graphs, a, b, weight):

    if graphs["friends"].get_edge(a, b) == 1.0:
        print(f"{a} and {b} already despise each other.")
        return

    graphs["friends"].weaken_edge(a, b, weight)

    if graphs["friends"].get_edge(a, b) == 1.0:
        print(f"{a} and {b} are now arch-enemies.")
    elif graphs["friends"].get_edge(a, b) == 1.5:
        print(f"{a} and {b} have a neutral relationship.")
    elif graphs["friends"].get_edge(a, b) < 1.5:
        print(f"{a} and {b} now dislike each other more.")
    else:
        print(f"{a} and {b} still like each other.")


# TODO: Write trust/distrust methods. Should be affected by 


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