from core.graph import *
from core.node import *
import pytest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

matrixGraph = MatrixGraph(["A", "B", "C"], [[0,1],[1,2],[2,0]])

def test_basic_matrix_graph_init():
    assert matrixGraph.vertices == ["A", "B", "C"]
    assert matrixGraph.matrix[0][1] == 1 
    assert matrixGraph.matrix[1][2] == 1
    assert matrixGraph.matrix[2][0] == 1 
    assert matrixGraph.matrix[0][2] == 0 

    #logger.info("\n" + str(matrixGraph))
    

def test_basic_matrix_graph_add_vertex():
    matrixGraph.add_vertex("D")
    
    assert matrixGraph.vertices == ["A", "B", "C", "D"]
    assert len(matrixGraph.matrix) == 4
    assert len(matrixGraph.matrix[0]) == 4

    logger.info("\n" + str(matrixGraph))


def test_basic_matrix_graph_remove_vertex():
    matrixGraph.remove_vertex("D")

    assert matrixGraph.vertices == ["A", "B", "C", None]
    assert matrixGraph.matrix[0][3] == None
    assert matrixGraph.vertices[3] == None

    matrixGraph.add_vertex("D")
    matrixGraph.remove_vertex("D")

    assert matrixGraph.vertices == ["A", "B", "C", None, None]
    assert matrixGraph.matrix[0][4] == None
    assert matrixGraph.vertices[4] == None

    logger.info("\n" + str(matrixGraph))


def test_basic_matrix_graph_remove_edge():
    matrixGraph.remove_edge(0,1)

    assert matrixGraph.matrix[0][1] == 0 
    assert matrixGraph.matrix[1][2] == 1
    assert matrixGraph.matrix[2][0] == 1 
    assert matrixGraph.matrix[0][2] == 0 

    assert len(matrixGraph.edges) == 2


def test_basic_matrix_graph_check_edges():
    incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [0,1])

    assert type(incorrectMatrixGraph.edges[0]) == list

    with pytest.raises(Exception):
        incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [0])

    with pytest.raises(Exception):
        incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], [3,0])

    incorrectMatrixGraph = MatrixGraph(["A", "B", "C"], None)

logger.info("\n" + str(matrixGraph))
