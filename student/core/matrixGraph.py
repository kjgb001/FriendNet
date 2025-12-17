from core.graphInterface import GraphInterface
from typing import Any


class DirectedMatrixGraph(GraphInterface):
    """Directed graph implemented using an adjacency matrix."""

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph.

        Args:
            vertex: The vertex to add.

        Side effects:
            Mutates the graph by adding a new vertex.

        Raises:
            ValueError: If the vertex already exists in the graph.
        """
        pass

    def add_edge(self, v1: Any, v2: Any, weight: float | None = None) -> None:
        """Add a directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The destination vertex.
            weight: Ignored for unweighted graphs.

        Side effects:
            Mutates the graph by adding a directed edge.

        Raises:
            KeyError: If either vertex does not exist.
            ValueError: If the edge already exists.
        """
        pass

    def remove_vertex(self, vertex: Any) -> Any:
        """Remove a vertex and all associated edges.

        Args:
            vertex: The vertex to remove.

        Returns:
            The removed vertex.

        Side effects:
            Mutates the graph by removing the vertex and its edges.

        Raises:
            KeyError: If the vertex does not exist.
        """
        pass

    def remove_edge(self, v1: Any, v2: Any) -> float:
        """Remove the directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The destination vertex.

        Returns:
            The weight of the removed edge, or a default value for unweighted graphs.

        Side effects:
            Mutates the graph by removing the edge.

        Raises:
            KeyError: If the edge does not exist.
        """
        pass

    def get_vertices(self) -> list:
        """Return a list of all vertices in the graph."""
        pass

    def get_edge(self, v1: Any, v2: Any) -> float:
        """Return the weight of the directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The destination vertex.

        Returns:
            The edge weight, or 0 if no edge exists.

        Raises:
            KeyError: If either vertex does not exist.
        """
        pass

    def get_edges(self) -> list:
        """Return a list of all directed edges in the graph."""
        pass

    def get_neighbors(self, vertex: Any) -> list:
        """Return all outgoing neighbors of a vertex.

        Args:
            vertex: The vertex whose neighbors are requested.

        Returns:
            A list of vertices directly reachable from the given vertex.

        Raises:
            KeyError: If the vertex does not exist.
        """
        pass


class UndirectedMatrixGraph(GraphInterface):
    """Undirected graph implemented using an adjacency matrix."""

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph.

        Args:
            vertex: The vertex to add.

        Side effects:
            Mutates the graph by adding a new vertex.

        Raises:
            ValueError: If the vertex already exists.
        """
        pass

    def add_edge(self, v1: Any, v2: Any, weight: float | None = None) -> None:
        """Add an undirected edge between v1 and v2.

        Args:
            v1: One endpoint of the edge.
            v2: The other endpoint of the edge.
            weight: Ignored for unweighted graphs.

        Side effects:
            Mutates the graph by adding edges in both directions.

        Raises:
            KeyError: If either vertex does not exist.
            ValueError: If the edge already exists.
        """
        pass

    def remove_vertex(self, vertex: Any) -> Any:
        """Remove a vertex and all associated edges.

        Args:
            vertex: The vertex to remove.

        Returns:
            The removed vertex.

        Side effects:
            Mutates the graph by removing the vertex and its edges.

        Raises:
            KeyError: If the vertex does not exist.
        """
        pass

    def remove_edge(self, v1: Any, v2: Any) -> float:
        """Remove the undirected edge between v1 and v2.

        Args:
            v1: One endpoint of the edge.
            v2: The other endpoint of the edge.

        Returns:
            The weight of the removed edge, or a default value for unweighted graphs.

        Side effects:
            Mutates the graph by removing edges in both directions.

        Raises:
            KeyError: If the edge does not exist.
        """
        pass

    def get_vertices(self) -> list:
        """Return a list of all vertices in the graph."""
        pass

    def get_edge(self, v1: Any, v2: Any) -> float:
        """Return the weight of the edge between v1 and v2.

        Args:
            v1: One endpoint of the edge.
            v2: The other endpoint of the edge.

        Returns:
            The edge weight, or 0 if no edge exists.

        Raises:
            KeyError: If either vertex does not exist.
        """
        pass

    def get_edges(self) -> list:
        """Return a list of all undirected edges in the graph."""
        pass

    def get_neighbors(self, vertex: Any) -> list:
        """Return all neighbors of a vertex.

        Args:
            vertex: The vertex whose neighbors are requested.

        Returns:
            A list of vertices connected to the given vertex.

        Raises:
            KeyError: If the vertex does not exist.
        """
        pass


class WeightedDirectedMatrixGraph(GraphInterface):
    """Weighted directed graph implemented using an adjacency matrix."""

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        pass

    def add_edge(self, v1: Any, v2: Any, weight: float | None = None) -> None:
        """Add a weighted directed edge from v1 to v2.

        Args:
            v1: The source vertex.
            v2: The destination vertex.
            weight: The weight of the edge.

        Side effects:
            Mutates the graph by adding a weighted directed edge.

        Raises:
            ValueError: If weight is None.
            KeyError: If either vertex does not exist.
        """
        pass

    def remove_vertex(self, vertex: Any) -> Any:
        """Remove a vertex and all associated edges."""
        pass

    def remove_edge(self, v1: Any, v2: Any) -> float:
        """Remove the directed edge from v1 to v2 and return its weight."""
        pass

    def get_vertices(self) -> list:
        """Return a list of all vertices in the graph."""
        pass

    def get_edge(self, v1: Any, v2: Any) -> float:
        """Return the weight of the directed edge from v1 to v2."""
        pass

    def get_edges(self) -> list:
        """Return a list of all weighted directed edges in the graph."""
        pass

    def get_neighbors(self, vertex: Any) -> list:
        """Return all outgoing neighbors of a vertex."""
        pass


class WeightedUndirectedMatrixGraph(GraphInterface):
    """Weighted undirected graph implemented using an adjacency matrix."""

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        pass

    def add_edge(self, v1: Any, v2: Any, weight: float | None = None) -> None:
        """Add a weighted undirected edge between v1 and v2."""
        pass

    def remove_vertex(self, vertex: Any) -> Any:
        """Remove a vertex and all associated edges."""
        pass

    def remove_edge(self, v1: Any, v2: Any) -> float:
        """Remove the undirected edge between v1 and v2 and return its weight."""
        pass

    def get_vertices(self) -> list:
        """Return a list of all vertices in the graph."""
        pass

    def get_edge(self, v1: Any, v2: Any) -> float:
        """Return the weight of the edge between v1 and v2."""
        pass

    def get_edges(self) -> list:
        """Return a list of all weighted undirected edges in the graph."""
        pass

    def get_neighbors(self, vertex: Any) -> list:
        """Return all neighbors of a vertex."""
        pass
