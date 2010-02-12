class BlankNode:
    __slots__ = 'node_id'

    def __init__(self, node_id=None):
        self.node_id = node_id

    def __repr__(self):
        if self.node_id is not None:
            return "BlankNode({!r})".format(self.node_id)
        else:
            return "<BlankNode at {!s}>".format(hex(id(self)))

    def __eq__(self, other):
        return (isinstance(other, BlankNode) and
                (self is other or
                 (self.node_id is not None and
                  self.node_id == other.node_id)))

    def __hash__(self):
        identity = self.node_id if self.node_id is not None else id(self)
        return hash(BlankNode) ^ hash(identity)

    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)

