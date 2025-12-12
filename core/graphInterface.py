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
        if not self.vertices:
            return "[Empty Graph]"

        active = [(i, v) for i, v in enumerate(self.vertices) if v is not None]

        return f"Vertices: {len(active)}, Edges: {len(self.edges)}"

    def debug_matrix(self):
        if not self.vertices:
            return "[Empty Graph]"

        # Collect active vertices: (index, Person)
        active = [(i, v) for i, v in enumerate(self.vertices) if v is not None]

        # Header row, indexes only
        header = "     " + " ".join(f"{i:>6}" for i, _ in active)

        rows = []
        for i, v in active:
            row_vals = []
            for j, v2 in active:
                val = self.matrix[i][j]

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
