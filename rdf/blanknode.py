from rdf.resource import Resource


class BlankNode(Resource):
    __slots__ = 'node_id'

    def __init__(self, node_id=None):
        self.node_id = node_id

    def __repr__(self):
        return "BlankNode(%r)" % (self.node_id,)

