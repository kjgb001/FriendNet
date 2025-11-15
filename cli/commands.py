

def add_person(graphs, person):
    for graph in graphs.values():
        graph.add_vertex(person)

def connect(graphs, a, b, weight = None):
    if not weight:
        graphs["friends"].add_edge(a, b)
    else:
        graphs["friends"].add_edge(a, b, weight)



