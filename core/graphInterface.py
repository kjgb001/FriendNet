from abc import ABC, abstractmethod
from typing import Any

class GraphInterface(ABC):
    @abstractmethod
    def add_vertex(self, vertex: Any) -> None:
        pass

    @abstractmethod
    def add_edge(self, v1: Any, v2: Any, weight: float | None = None) -> None:
        pass

    @abstractmethod
    def remove_vertex(self, vertex: Any) -> Any:
        pass

    @abstractmethod
    def remove_edge(self, v1: Any, v2: Any) -> int | float:
        pass

    @abstractmethod
    def get_vertices(self) -> list:
        pass

    @abstractmethod
    def get_edge(self, v1: Any, v2: Any) -> int | float:
        pass

    @abstractmethod
    def get_edges(self) -> list:
        pass

    @abstractmethod
    def get_neighbors(self, vertex: Any) -> list:
        pass

    def size(self):
        return len(self.get_edges())

    def __len__(self):
        active = [(i, v) for i, v in enumerate(self.get_vertices()) if v is not None]
        return len(active)

    def __str__(self):
        if self.get_vertices():
            active = [(i, v) for i, v in enumerate(self.get_vertices()) if v is not None] # Guard against removal logic setting Nones
        else:
            active = []
        
        if len(active) == 0:
            return "[Empty Graph]"

        return f"Vertices: {len(active)}, Edges: {len(self.get_edges())}"

    def debug_graph(self):
        if not self.get_vertices():
            return "[Empty Graph]"

        # Collect active vertices: (index, Person)
        active = [(i, v) for i, v in enumerate(self.get_vertices()) if v is not None]

        # Header row, indexes only
        header = "     " + " ".join(f"{i:>6}" for i, _ in active)

        rows = []
        for i, v in active:
            row_vals = []
            for j, v2 in active:
                val = self.get_edge(i, j)

                if val == 0:
                    row_vals.append("     .")
                else:
                    row_vals.append(f"{val:>6.2f}")  # width 6, 2 decimals

            rows.append(f"{i:>3} | " + " ".join(row_vals))
        
        # Optional: map index, name for readability
        name_map = "\n".join(
            f"  {i:>3} = {v.data.fname} {v.data.lname}"
            for i, v in active
        )

        return (
            f"{header}\n" +
            "\n".join(rows) +
            "\n\nIndex map:\n" +
            name_map +
            "\n"
        )
