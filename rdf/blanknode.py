from .resource import Resource


class BlankNode(Resource):
    def __init__(self, node_id):
        self.node_id = node_id

    def __repr__(self):
        return "BlankNode(%r)" % (self.node_id,)
