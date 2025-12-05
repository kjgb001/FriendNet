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

    def __len__(self):
        return len(self.vertices)

    def __str__(self):
        # Could dynamically pad instead of hard coding 5
        if not self.vertices:
            return "[Empty Graph]"

        # Filter to live vertices
        active = [(i, v) for i, v in enumerate(self.vertices) if v is not None]

        header = "    " + " ".join(f"{v:>5}" for _, v in active)
        rows = []
        for i, v in active:
            # Only include columns for active vertices
            row_vals = [
                f"{self.matrix[i][j]:>5}" 
                for j, col_v in enumerate(self.vertices) if col_v is not None
            ]
            rows.append(f"{v:>3} " + " ".join(row_vals))
        return f"{header}\n" + "\n".join(rows) + (
            f"\n\nVertices: {len(active)}, Edges: {len(self.edges)}"
        )