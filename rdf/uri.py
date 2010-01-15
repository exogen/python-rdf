from .resource import Resource


class URI(Resource, str):
    def __repr__(self):
        return "URI(%r)" % str(self)
