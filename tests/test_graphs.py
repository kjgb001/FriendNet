import pytest
from core.matrixGraph import (
    UndirectedMatrixGraph,
    DirectedMatrixGraph,
    WeightedUndirectedMatrixGraph,
    WeightedDirectedMatrixGraph,
)


# Graph classes under test

GRAPH_CLASSES = [
    UndirectedMatrixGraph,
    DirectedMatrixGraph,
    WeightedUndirectedMatrixGraph,
    WeightedDirectedMatrixGraph,
]

DIRECTED_CLASSES = {
    DirectedMatrixGraph,
    WeightedDirectedMatrixGraph,
}

WEIGHTED_CLASSES = {
    WeightedUndirectedMatrixGraph,
    WeightedDirectedMatrixGraph,
}


# Fixtures

@pytest.fixture(params=GRAPH_CLASSES)
def graph(request):
    return request.param()

@pytest.fixture
def vertices():
    return ["A", "B", "C"]


# Invariant tests

def test_add_vertices(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    verts = graph.get_vertices()
    assert len([v for v in verts if v is not None]) == 3
    assert len(graph) == 3


def test_add_edge(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    if type(graph) in WEIGHTED_CLASSES:
        graph.add_edge(0, 1, weight=1.0)
    else:
        graph.add_edge(0, 1)

    assert graph.get_edge(0, 1) != 0
    assert "B" in graph.get_neighbors(0)

    # Undirected graphs should mirror the edge
    if type(graph) not in DIRECTED_CLASSES:
        assert "A" in graph.get_neighbors(1)


def test_remove_edge(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    if type(graph) in WEIGHTED_CLASSES:
        graph.add_edge(0, 1, weight=1.0)
    else:
        graph.add_edge(0, 1)

    graph.remove_edge(0, 1)

    assert graph.get_edge(0, 1) == 0
    assert "B" not in graph.get_neighbors(0)

    if type(graph) not in DIRECTED_CLASSES:
        assert "A" not in graph.get_neighbors(1)


def test_remove_vertex(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    removed = graph.remove_vertex(1)

    verts = graph.get_vertices()
    assert verts[1] is None
    assert removed == "B"
    assert len(graph) == 2


def test_edges_with_removed_vertex_are_ignored(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    if type(graph) in WEIGHTED_CLASSES:
        graph.add_edge(0, 1, weight=1.0)
        graph.add_edge(1, 2, weight=1.0)
    else:
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)

    graph.remove_vertex(1)

    for a, b in graph.get_edges():
        assert a != 1
        assert b != 1


def test_size_matches_edge_count(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    if type(graph) in WEIGHTED_CLASSES:
        graph.add_edge(0, 1, weight=1.0)
        graph.add_edge(0, 2, weight=1.0)
    else:
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)

    assert graph.size() == len(graph.get_edges())


def test_str_graph(graph, vertices):
    for v in vertices:
        graph.add_vertex(v)

    s = str(graph)
    assert "Vertices:" in s
    assert "Edges:" in s
