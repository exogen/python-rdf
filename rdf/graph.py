from rdf.blanknode import BlankNode


class Graph(set):
    def is_ground(self):
        for triple in self._blank_node_triples():
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False
        if len(self) != len(other):
            return False
        bnode_triples = set(self._blank_node_triples())
        ground_triples = self - bnode_triples
        other_bnode_triples = set(other._blank_node_triples())
        other_ground_triples = other - other_bnode_triples
        if ground_triples != other_ground_triples:
            return False
        if bnode_triples and other_bnode_triples:
            if len(bnode_triples) != len(other_bnode_triples):
                return False
            return False
        else:
            return True

    def _blank_node_triples(self):
        for triple in self:
            if any(isinstance(term, BlankNode) for term in triple):
                yield triple

