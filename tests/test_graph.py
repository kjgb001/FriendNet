from core.matrixGraph import *
from core.node import *
import pytest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def matrixGraph():
    return MatrixGraph(["A", "B", "C"], [[0,1],[1,2],[2,0]])

@pytest.fixture
def u_matrixGraph():
    return U_MatrixGraph(["A", "B", "C"], [[0,1],[1,2],[2,0]])

@pytest.fixture
def w_matrixGraph():
    return W_MatrixGraph(["A", "B", "C"], [[0,1],[1,2],[2,0]], {(0,1): 1.0, (1,2): 2.0, (2,0): 1.5})

@pytest.fixture
def wu_matrixGraph():
    return WU_MatrixGraph(["A", "B", "C"], [[0,1],[1,2],[2,0]], {(0,1): 1.0, (1,2): 2.0, (2,0): 1.5})


'''
@pytest.mark.parametrize("MatrixGraph", [
    matrixGraph
])
'''

def test_basic_matrix_graph_init(matrixGraph):
    assert matrixGraph.vertices == ["A", "B", "C"]
    assert matrixGraph.matrix[0][1] == 1 
    assert matrixGraph.matrix[1][2] == 1
    assert matrixGraph.matrix[2][0] == 1 
    assert matrixGraph.matrix[0][2] == 0 

    #logger.info("\n" + str(matrixGraph))
    

def test_basic_matrix_graph_add_vertex(matrixGraph):
    matrixGraph.add_vertex("D")
    
    assert matrixGraph.vertices == ["A", "B", "C", "D"]
    assert len(matrixGraph.matrix) == 4
    assert len(matrixGraph.matrix[0]) == 4

    logger.info("\n" + str(matrixGraph))


def test_basic_matrix_graph_remove_vertex(matrixGraph):
    matrixGraph.add_vertex("D")
    matrixGraph.remove_vertex("D")

    assert matrixGraph.vertices == ["A", "B", "C", None]
    assert matrixGraph.matrix[0][3] == None
    assert matrixGraph.vertices[3] == None

    logger.info("\n" + str(matrixGraph))


def test_basic_matrix_graph_add_edge(matrixGraph):
    matrixGraph.add_edge(0,2)

    assert matrixGraph.matrix[0][2] == 1
    assert [0,2] in matrixGraph.edges


def test_basic_matrix_graph_remove_edge(matrixGraph):
    matrixGraph.remove_edge(0,1)

    assert matrixGraph.matrix[0][1] == 0 
    assert matrixGraph.matrix[1][2] == 1
    assert matrixGraph.matrix[2][0] == 1 
    assert matrixGraph.matrix[0][2] == 0 

    assert [0,1] not in matrixGraph.edges

    assert len(matrixGraph.edges) == 2


def test_basic_matrix_graph_check_edges():
    incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [0,1])

    assert type(incorrectMatrixGraph.edges[0]) == list

    with pytest.raises(Exception):
        incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [0])

    with pytest.raises(Exception):
        incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [3,0])

    incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], None)


def test_undirected_matrix_graph_undirectedness(u_matrixGraph):

    assert u_matrixGraph.matrix[0][1] == 1
    assert u_matrixGraph.matrix[1][0] == 1
    assert u_matrixGraph.matrix[1][2] == 1
    assert u_matrixGraph.matrix[2][1] == 1
    assert u_matrixGraph.matrix[0][2] == 1
    assert u_matrixGraph.matrix[2][0] == 1


def test_undirected_matrix_graph_add_edge(u_matrixGraph):
    u_matrixGraph.add_vertex("D")
    u_matrixGraph.add_edge(0,3)

    assert u_matrixGraph.matrix[0][3] == 1
    assert u_matrixGraph.matrix[3][0] == 1

    assert [0,3] in u_matrixGraph.edges


def test_undirected_matrix_graph_remove_edge(u_matrixGraph):
    u_matrixGraph.remove_edge(0,1)

    assert u_matrixGraph.matrix[0][1] == 0 
    assert u_matrixGraph.matrix[1][2] == 1
    assert u_matrixGraph.matrix[2][0] == 1 
    assert u_matrixGraph.matrix[1][0] == 0 

    assert [0,1] not in u_matrixGraph.edges

    assert len(u_matrixGraph.edges) == 2


def test_weighted_matrix_graph_init(w_matrixGraph):

    assert w_matrixGraph.matrix[0][1] == 1.0
    assert w_matrixGraph.matrix[1][2] == 2.0
    assert w_matrixGraph.matrix[2][0] == 1.5


def test_weighted_matrix_graph_add_edge(w_matrixGraph):
    w_matrixGraph.add_edge(0,2,1.5)

    assert w_matrixGraph.matrix[0][2] == 1.5
    assert [0,2] in w_matrixGraph.edges


def test_weighted_undirected_matrix_graph_undirectedness(wu_matrixGraph):

    assert wu_matrixGraph.matrix[0][1] == 1.0
    assert wu_matrixGraph.matrix[1][0] == 1.0
    assert wu_matrixGraph.matrix[1][2] == 2.0
    assert wu_matrixGraph.matrix[2][1] == 2.0
    assert wu_matrixGraph.matrix[0][2] == 1.5
    assert wu_matrixGraph.matrix[2][0] == 1.5

logger.info("\n" + str(matrixGraph))
