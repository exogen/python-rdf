from collections import defaultdict
from itertools import product

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
            bnodes = self._blank_node_map(bnode_triples)
            other_bnodes = self._blank_node_map(other_bnode_triples)
            if len(bnodes) != len(other_bnodes):
                return False
            return False
        else:
            return True

    def _blank_node_triples(self):
        for triple in self:
            if any(isinstance(term, BlankNode) for term in triple):
                yield triple

    def _blank_node_map(self, triples):
        map = defaultdict(set)
        for triple in triples:
            for term in triple:
                if isinstance(term, BlankNode):
                    map[term].add(triple)
        return map

    def _blank_node_bijections(self, a, b):
        candidates = defaultdict(set)
        for a_bnode, a_triples in a.items():
            for b_bnode, b_triples in b.items():
                # Filter the set of possible candidates.
                if len(a_triples) == len(b_triples):
                    candidates[a_bnode].add(b_bnode)

        done = False
        while not done:
            for a_node, b_bnodes in candidates.items():
                for b_bnode in b_bnodes:
                    bijection = {a_bnode: b_bnode}
                    inverse = {b_bnode: a_bnode}

