from typing import Any
from .node import *
from .graphInterface import GraphInterface
import numbers

class MatrixGraph(GraphInterface):
    '''
    Basic directed graph structure using a 2D matrix (nested lists) to store edges.
    Serves as the parent class for undirected, weighted, and acyclic graph variants.
    Vertices must be a list of non-numeric values/objects, and edges must be a pair
    of integers representing the indexes of two vertices.
    '''
    # Could rewrite class to allow either index based OR vertex object based edges
    def __init__(self, vertices: list | None, edges: list[list[int]] | None, weights: dict = None) -> None:
        if vertices == None:
            vertices = []
        
        if edges is None:
            edges = []
        
        self.vertices = self._check_vertices(vertices)
        self.edges = self._check_edges(edges)
        
        # Create square 2D matrix of zeros based on number of vertices.
        self.matrix = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]

        # Create dict to track the index of each vertex.
        self._index_map = {vertex: i for i, vertex in enumerate(self.vertices)}

        self._populate_matrix()


    def _populate_matrix(self):
        '''
        Helper function to set starting values of the matrix according to
        the vertices and edges passed as arguments during initialization.
        '''
        # Assign 1 to each matrix coordinate listed in edges to represent directional connection.
        for i in self.edges:
            y = i[0]
            x = i[1]
            self.add_edge(y, x)

    
    def _check_vertices(self, vertices: list):
        '''Helper function to check if any vertices are numbers.'''
        if len(set(vertices)) != len(vertices):
            raise ValueError("Duplicate vertices detected.")

        for i in vertices:
            if isinstance(i, numbers.Number):
                raise ValueError("Invalid vertex: " + str(i) 
                + "\nVertices cannot be numeric")

        return vertices


    def _check_edges(self, edges: list):
        '''Helper function to check viability of edges, and corrects if possible.'''
        # Check for empty list.
        if edges in([], [[]]):
            return edges

        # Check for and correct 1D list.
        if not isinstance(edges[0], list):
            edges = [edges]

        # Call _check_edge helper function for each edge.
        for i in edges:
            self._check_edge(i)

        return edges


    def _check_edge(self, edge: list):
        '''
        Helper function to check if each edge is length of 2 
        and only contains ints representing an existing vertex.
        '''
        if len(edge) != 2 or not all(isinstance(i, int) for i in edge):
            raise ValueError("Edge must be a list of two integer indices.")

        for i in edge:
            if not 0 <= i < len(self.vertices):
                raise ValueError(f"Edge index {i} out of range for vertices {len(self.vertices)}.")

        
    def add_vertex(self, vertex: Any):
        '''Adds a single vertex to the graph. A vertex can be any object type.'''
        if vertex in self.vertices:
            raise ValueError(f"Vertex {vertex!r} already exists.")

        self.vertices.append(vertex)
        self._index_map[vertex] = len(self.vertices) - 1

        # Append extra column of zeros to each row.
        for i in self.matrix:
            if i:
                i.append(0)

        # Append new row of zeros with length of vertices list.
        self.matrix.append([0 for _ in range(len(self.vertices))])

    
    def remove_vertex(self, vertex: Any):
        '''
        Removes a vertex by finding the index if vertex param not an int
        then calling _remove_vertex_by_index. Vertex param can be either an
        int to remove by index, or the vertex object to be removed.
        '''
        # Check that entered vertex param is valid
        if isinstance(vertex, int):
            if vertex < 0 or vertex >= len(self.vertices):
                raise IndexError("Vertex index out of range.")
        elif vertex not in self.vertices:
            raise ValueError(f"Vertex {vertex!r} not found.")

        # Sets the vertex variable to the corresponding index if needed
        if not isinstance(vertex, int):
            vertex = self.vertices.index(vertex)

        self._remove_vertex_by_index(vertex)

    
    def _remove_vertex_by_index(self, index: int):
        '''Removes a vertex from the graph by index.'''
        # Remove column by iterating through rows and setting to None.
        for i in self.matrix:
            if i:
                i[index] = None

        # Remove from index map.
        del self._index_map[self.vertices[index]]

        # Remove row from matrix by setting to None.
        self.matrix[index] = None

        # Remove from vertices list by setting to None.
        self.vertices[index] = None

    
    def _vertex_index(self, vertex) -> int:
        '''Return index of vertex object, raise if not found.'''
        try:
            vertex = self._index_map[vertex] if not isinstance(vertex, int) else vertex

            return vertex

        except KeyError as e:
            raise ValueError(f"Vertex not found in graph.") from e


    def add_edge(self, v1, v2, weight = None):
        '''Adds a single directed edge to the graph: v1 -> v2. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Checks edge validity
        self._check_edge(edge)

        if edge not in self.edges:
            self.edges.append(edge)

        # Set value at edge cooridinate to one to represent connection.
        self.matrix[edge[0]][edge[1]] = 1


    def remove_edge(self, v1, v2):
        '''Removes an edge from the graph. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]
        
        # Checks edge validity
        self._check_edge(edge)

        # Iterate through edges to find match
        for e in self.edges[:]:
            if e == edge:
                self.edges.remove(e)

        # Set value at edge cooridinate to zero to represent no connection.
        self.matrix[edge[0]][edge[1]] = 0

    
    def get_matrix(self) -> list[list[int]]:
        '''Return a copy of the matrix'''
        return [row[:] for row in self.matrix]

    
    def get_edge(self, v1, v2):

        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        return self.matrix[edge[0]][edge[1]]


class U_MatrixGraph(MatrixGraph):
    
    def _populate_matrix(self):
        '''
        Helper function to set starting values of the matrix according to
        the vertices and edges passed as arguments during initialization.
        '''

        # Assign 1 to each matrix coordinate listed in edges to represent directional connection.
        for i in self.edges:
            y = i[0]
            x = i[1]
            self.add_edge(y, x)

    
    def add_edge(self, v1, v2, weight = None):
        '''Adds a single directed edge to the graph: v1 -> v2. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Create mirrored edge list
        edge_mirror = [edge[1], edge[0]]

        # Checks edge validity
        self._check_edge(edge)

        if edge not in self.edges and edge_mirror not in self.edges:
            self.edges.append(edge)

        # Set value at edge cooridinate to one to represent connection.
        self.matrix[edge[0]][edge[1]] = 1
        self.matrix[edge[1]][edge[0]] = 1


    def remove_edge(self, v1, v2):
        '''Removes an edge from the graph. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Create mirrored edge list
        edge_mirror = [edge[1], edge[0]]
        
        # Checks edge validity
        self._check_edge(edge)

        # Iterate through edges to find match for removal
        for e in self.edges[:]:
            if e == edge or e == edge_mirror:
                self.edges.remove(e)

        # Set value at edge cooridinate to zero to represent no connection.
        self.matrix[edge[0]][edge[1]] = 0
        self.matrix[edge[1]][edge[0]] = 0


class W_MatrixGraph(MatrixGraph):
    
    def __init__(self, vertices: list, edges: list[list[int]] | None, weights: dict) -> None:
        if vertices == None:
            vertices = []
        
        if edges is None:
            edges = []

        if weights is None:
            weights = {}
        
        self.vertices = self._check_vertices(vertices)
        self.edges = self._check_edges(edges)
        self.weights = self._check_weights(weights)
        
        # Create square 2D matrix of zeros based on number of vertices.
        self.matrix = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]

        # Create dict to track the index of each vertex.
        self._index_map = {vertex: i for i, vertex in enumerate(self.vertices)}

        self._populate_matrix()


    def _populate_matrix(self):
        '''
        Helper function to set starting values of the matrix according to
        the vertices and edges passed as arguments during initialization.
        '''
        # Assign 1 to each matrix coordinate listed in edges to represent directional connection.
        for i in self.edges:
            y = i[0]
            x = i[1]
            w = self.weights[(y, x)]
            self.add_edge(y, x, w)


    def _check_weights(self, weights: dict):
        if len(weights) != len(self.edges):
            raise ValueError("Number of weigths != number of edges. Every edge must have a weight.")

        for edge, weight in weights.items():
            self._check_weight(edge, weight)

        return weights

    
    def _check_weight(self, edge, weight):
        if not isinstance(weight, float):
            raise TypeError(f"Weight must be a number, got {type(weight).__name__}.")

        if weight < 1 or weight > 2:
            raise ValueError(f"Weight {weight} is out of allowed range [1, 2].")

        if len(edge) > 2 or not isinstance(edge, tuple):
            raise TypeError("Weight entries must have tuple keys of two vertices.")

        if not isinstance(edge, list):
            list_edge = [self._vertex_index(edge[0]), self._vertex_index(edge[1])]

        self._check_edge(list_edge)


    def add_edge(self, v1, v2, weight: float):
        '''Adds a single directed edge to the graph: v1 -> v2. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, weight)

        if edge not in self.edges:
            self.edges.append(edge)

        # Set value at edge cooridinate to weighted value to represent connection.
        self.matrix[edge[0]][edge[1]] = weight


    def strengthen_edge(self, v1, v2, weight: float):
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        if weight <= 0.0 or weight > 1.0:
            raise ValueError("Weight strengthen value must be a float value greater than zero and less than or equal to one.")

        # Increment edge weights
        self.matrix[edge[0]][edge[1]] += weight

        if self.matrix[edge[0]][edge[1]] > 2.0:
            self.matrix[edge[0]][edge[1]] = 2.0

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, self.matrix[edge[0]][edge[1]])

    
    def weaken_edge(self, v1, v2, weight: float):
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        if weight <= 0.0 or weight > 1.0:
            raise ValueError("Weight weaken value must be a float value greater than zero and less than or equal to one.")

        # Decrement edge weights
        self.matrix[edge[0]][edge[1]] -= weight

        if self.matrix[edge[0]][edge[1]] < 1.0:
            self.matrix[edge[0]][edge[1]] = 1.0

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, self.matrix[edge[0]][edge[1]])


class WU_MatrixGraph(W_MatrixGraph):

    def add_edge(self, v1, v2, weight):
        '''Adds a single directed edge to the graph: v1 -> v2. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Create mirrored edge list
        edge_mirror = [edge[1], edge[0]]

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, weight)

        if edge not in self.edges and edge_mirror not in self.edges:
            self.edges.append(edge)

        # Set value at edge cooridinate to one to represent connection.
        self.matrix[edge[0]][edge[1]] = weight
        self.matrix[edge[1]][edge[0]] = weight

    def remove_edge(self, v1, v2):
        '''Removes an edge from the graph. Both vertex args must either be an int
        representing the index of the vertex OR an object/value currently stored as a vertex.'''
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        # Create mirrored edge list
        edge_mirror = [edge[1], edge[0]]
        
        # Checks edge validity
        self._check_edge(edge)

        # Iterate through edges to find match for removal
        for e in self.edges[:]:
            if e == edge or e == edge_mirror:
                self.edges.remove(e)

        # Set value at edge cooridinate to zero to represent no connection.
        self.matrix[edge[0]][edge[1]] = 0
        self.matrix[edge[1]][edge[0]] = 0


    def strengthen_edge(self, v1, v2, weight: float):
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        if weight <= 0.0 or weight > 1.0:
            raise ValueError("Weight strengthen value must be a float value greater than zero and less than or equal to one.")

        # Increment edge weights
        self.matrix[edge[0]][edge[1]] += weight
        self.matrix[edge[1]][edge[0]] += weight

        if self.matrix[edge[0]][edge[1]] > 2.0:
            self.matrix[edge[0]][edge[1]] = 2.0
            self.matrix[edge[1]][edge[0]] = 2.0

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, self.matrix[edge[0]][edge[1]])

    
    def weaken_edge(self, v1, v2, weight: float):
        # Convert objects to indices if necessary
        edge = [self._vertex_index(v1), self._vertex_index(v2)]

        if weight <= 0.0 or weight > 1.0:
            raise ValueError("Weight weaken value must be a float value greater than zero and less than or equal to one.")

        # Decrement edge weights
        self.matrix[edge[0]][edge[1]] -= weight
        self.matrix[edge[1]][edge[0]] -= weight

        if self.matrix[edge[0]][edge[1]] < 1.0:
            self.matrix[edge[0]][edge[1]] = 1.0
            self.matrix[edge[1]][edge[0]] = 1.0

        # Checks weighted edge validity
        tuple_edge = (self._vertex_index(edge[0]), self._vertex_index(edge[1]))
        self._check_weight(tuple_edge, self.matrix[edge[0]][edge[1]])

