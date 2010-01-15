from rdf.blanknode import BlankNode


class Graph(set):
    def is_ground(self):
        for triple in self:
            if any(isinstance(term, BlankNode) for term in triple):
                return False
        return True

