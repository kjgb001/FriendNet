import uuid

class Vertex:
    """! The node.Vertex class.

    Defines the basic vertex class, stores data and edges for graph structure.
    """
    def __init__(self, data = None, edges = None) -> None:
        self.data = data
        self.edges = edges


class Identity:
    """! The node.Identity class.

    Defines the Identity class, stores identifying information used by Person class
    """
    def __init__(self, fname, lname, gender) -> None:
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.uid = uuid.uuid4()


class Person(Vertex):
    """! The node.Person class.

    Inherits from Vertex class, adding an identity parameter.
    """
    def __init__(self, identity: Identity, edges: list = None) -> None:
        self.identity = identity
        self.edges = edges

    def __eq__(self, other):
        return (
            isinstance(other, Person) and 
            self.identity.uid == other.identity.uid
        )

    def __hash__(self):
        return hash(self.identity.uid)
