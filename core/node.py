import uuid

class Node:
    def __init__(self, data = None, edges = None) -> None:
        self.data = data
        self.edges = edges


class Identity:
    """Encapsulates identifying attributes for a person."""
    
    def __init__(self, fname, lname, gender, picture) -> None:
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.picture = picture
        self.uid = uuid.uuid4()


class Person(Node):
    """Graph node representing a person in the simulation."""

    def __init__(self, identity: Identity, edges: list = None) -> None:
        super().__init__(identity, edges)

    def __eq__(self, other):
        return (
            isinstance(other, Person) and 
            self.data.uid == other.data.uid
        )

    def __hash__(self):
        return hash(self.data.uid)

    def __str__(self):
        return f"{self.data.fname} {self.data.lname}"

    