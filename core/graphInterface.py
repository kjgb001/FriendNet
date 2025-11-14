from abc import ABC, abstractmethod

class GraphInterface(ABC):
    @abstractmethod
    def add_vertex(self, vertex):
        pass

    @abstractmethod
    def add_edge(self, v1, v2, weight: float | None = None):
        pass

    @abstractmethod
    def remove_vertex(self, vertex):
        pass

    @abstractmethod
    def remove_edge(self, v1, v2):
        pass

    def size(self):
        return len(self.vertices)