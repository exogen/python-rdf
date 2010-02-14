from collections import defaultdict
from itertools import product

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal, TypedLiteral


class Graph(set):
    def __eq__(self, other):
        if not isinstance(other, Graph) or len(self) != len(other):
            return False
        bnode_triples = set(self._blank_node_triples(self))
        ground_triples = self - bnode_triples
        other_bnode_triples = set(self._blank_node_triples(other))
        other_ground_triples = other - other_bnode_triples
        if (len(ground_triples) != len(other_ground_triples) or
            ground_triples != other_ground_triples):
            return False
        elif bnode_triples:
            bnode_dict = self._blank_node_triple_dict(bnode_triples)
            other_bnode_dict = self._blank_node_triple_dict(other_bnode_triples)
            if len(bnode_dict) != len(other_bnode_dict):
                return False
            signatures = self._blank_node_signatures(bnode_dict)
            other_signatures = self._blank_node_signatures(other_bnode_dict)
            metasignature = self._metasignature(signatures)
            other_metasignature = self._metasignature(other_signatures)
            if metasignature != other_metasignature:
                return False
            for i, bijection in enumerate(self._blank_node_bijection_candidates(signatures, other_signatures)):
                for triple in self._apply_bijection(bijection, bnode_triples):
                    if triple not in other_bnode_triples:
                        break
                else:
                    return True
            else:
                return False
        else:
            return True

    def __ne__(self, other):
        return not self == other

    def is_ground(self):
        for triple in self._blank_node_triples(self):
            return False
        return True
    
    def nodes(self):
        return set(self._nodes())

    def _nodes(self):
        for triple in self:
            yield triple[0]
            yield triple[2]

    def names(self):
        return set(self._names())
    
    def _names(self):
        for triple in self:
            for term in triple[0], triple[2]:
                if isinstance(term, (URI, Literal)):
                    yield term
                if isinstance(term, TypedLiteral):
                    yield term.datatype
            yield triple[1]

    def vocabulary(self, include_datatypes=False):
        return set(self._vocabulary(include_datatypes))

    def _vocabulary(self, include_datatypes=False):
        for triple in self:
            for term in triple[0], triple[2]:
                if isinstance(term, (URI, Literal)):
                    yield term
                if isinstance(term, TypedLiteral) and include_datatypes:
                    yield term.datatype
            yield triple[1]

    @classmethod
    def _blank_node_triples(cls, triples):
        for triple in triples:
            if isinstance(triple[0], BlankNode) or isinstance(triple[2], BlankNode):
                yield triple

    @classmethod
    def _blank_node_triple_dict(cls, triples):
        map = defaultdict(set)
        for triple in triples:
            for term in triple:
                if isinstance(term, BlankNode):
                    map[term].add(triple)
        return map

    @classmethod
    def _blank_node_signatures(cls, bnode_dict):
        signatures = {}
        for bnode, triples in bnode_dict.items():
            signatures[bnode] = set(cls._blank_node_signature(triples))
        return signatures

    @classmethod
    def _blank_node_signature(cls, triples):
        count = len(triples)
        for triple in triples:
            triple = tuple(count if isinstance(term, BlankNode) else term
                           for term in triple)
            yield triple

    @classmethod
    def _metasignature(cls, signatures):
        metasignature = defaultdict(int)
        for triples in signatures.values():
            for triple in triples:
                metasignature[triple] += 1
        return metasignature

    @classmethod
    def _blank_node_bijection_candidates(cls, a_signatures, b_signatures):
        candidates = defaultdict(set)
        for a_bnode, a_signature in a_signatures.items():
            for b_bnode, b_signature in b_signatures.items():
                # Filter the set of possible candidates.
                if a_signature == b_signature:
                    candidates[a_bnode].add(b_bnode)

        product_pairs = [[(a_bnode, b_bnode) for b_bnode in b_bnodes]
                         for a_bnode, b_bnodes in candidates.items()]
        for bijection in product(*product_pairs):
            mapped = set()
            for a_bnode, b_bnode in bijection:
                if b_bnode not in mapped:
                    mapped.add(b_bnode)
                else:
                    break
            else:
                yield dict(bijection)

    @classmethod
    def _apply_bijection(cls, bijection, triples):
        for subject, predicate, object_ in triples:
            if isinstance(subject, BlankNode):
                subject = bijection[subject]
            if isinstance(object_, BlankNode):
                object_ = bijection[object_]
            yield (subject, predicate, object_)

