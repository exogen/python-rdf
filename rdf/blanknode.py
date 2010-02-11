class BlankNode:
    __slots__ = 'node_id'

    def __init__(self, node_id=None):
        self.node_id = node_id

    def __repr__(self):
        if self.node_id is not None:
            return "BlankNode({!r})".format(self.node_id)
        else:
            return "BlankNode()"

    def __eq__(self, other):
        return isinstance(other, BlankNode) and other.node_id == self.node_id

    def __hash__(self):
        return hash(BlankNode) ^ hash(self.node_id)

