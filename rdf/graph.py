import operator
from collections import defaultdict
from itertools import product

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal, TypedLiteral


class Graph(set):
    def __eq__(self, other):
        if not isinstance(other, (set, frozenset)) or len(self) != len(other):
            return False
        elif not isinstance(other, Graph):
            return frozenset(self) == other

        ground_triples = set(self._ground_triples())
        other_ground_triples = set(other._ground_triples())
        if ground_triples != other_ground_triples:
            return False

        bnode_triples = set(self._bnode_triples())
        if not bnode_triples:
            return True

        other_bnode_triples = set(other._bnode_triples())
        bnode_dict = self._bnode_dict(bnode_triples)
        other_bnode_dict = other._bnode_dict(other_bnode_triples)
        if len(bnode_dict) != len(other_bnode_dict):
            return False

        signatures = self._bnode_signatures(bnode_dict)
        other_signatures = other._bnode_signatures(other_bnode_dict)
        metasignature = self._metasignature(signatures)
        other_metasignature = other._metasignature(other_signatures)
        if metasignature != other_metasignature:
            return False

        for bijection in self._bnode_bijections(signatures, other_signatures):
            for triple in self._apply_bijection(bijection, bnode_triples):
                if triple not in other_bnode_triples:
                    break
            else:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, (set, frozenset)):
            return NotImplemented
        elif len(self) >= len(other):
            return False
        elif not isinstance(other, Graph):
            return frozenset(self) < other

        ground_triples = set(self._ground_triples())
        other_ground_triples = set(other._ground_triples())
        if not ground_triples <= other_ground_triples:
            return False

        bnode_triples = set(self._bnode_triples())
        other_bnode_triples = set(other._bnode_triples())
        if not bnode_triples:
            return True

        bnode_dict = self._bnode_dict(bnode_triples)
        other_bnode_dict = other._bnode_dict(other_bnode_triples)
        if len(bnode_dict) > len(other_bnode_dict):
            return False

        signatures = self._bnode_signatures(bnode_dict)
        other_signatures = other._bnode_signatures(other_bnode_dict)
        for bijection in self._bnode_bijections(signatures, other_signatures,
            self._subgraph_bnode_comparator):
            for triple in self._apply_bijection(bijection, bnode_triples):
                if triple not in other_bnode_triples:
                    break
            else:
                return True
        return False

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if isinstance(other, Graph):
            return other < self
        elif isinstance(other, (set, frozenset)):
            return frozenset(self) > other
        else:
            return NotImplemented

    def __ge__(self, other):
        return self == other or self > other

    def is_ground(self):
        for triple in self._bnode_triples():
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
            if isinstance(triple[0], URI):
                yield triple[0]
            yield triple[1]
            if isinstance(triple[2], (URI, Literal)):
                yield triple[2]
            if isinstance(triple[2], TypedLiteral):
                yield triple[2].datatype

    def vocabulary(self, include_datatypes=False):
        return set(self._vocabulary(include_datatypes))

    def _vocabulary(self, include_datatypes=False):
        for triple in self:
            if isinstance(triple[0], URI):
                yield triple[0]
            yield triple[1]
            if isinstance(triple[2], (URI, Literal)):
                yield triple[2]
            if isinstance(triple[2], TypedLiteral) and include_datatypes:
                yield triple[2].datatype

    def _bnode_triples(self):
        for triple in self:
            if (isinstance(triple[0], BlankNode) or
                isinstance(triple[2], BlankNode)):
                yield triple

    def _ground_triples(self):
        for triple in self:
            if (not isinstance(triple[0], BlankNode) and
                not isinstance(triple[2], BlankNode)):
                yield triple

    def _bnode_dict(self, triples):
        map = defaultdict(set)
        for triple in triples:
            for term in triple:
                if isinstance(term, BlankNode):
                    map[term].add(triple)
        return map

    def _bnode_signatures(self, bnode_dict):
        placeholders = {}
        signatures = {}
        bnode_triples = bnode_dict.items()
        for bnode, triples in bnode_triples:
            placeholders[bnode] = self._bnode_placeholder(bnode, triples)
        for bnode, triples in bnode_triples:
            signatures[bnode] = set(self._bnode_signature(bnode, triples,
                                                          placeholders))
        return signatures

    def _bnode_signature(self, bnode, triples, placeholders):
        for triple in triples:
            yield tuple(placeholders.get(term, term) for term in triple)

    def _bnode_placeholder(self, bnode, triples):
        subject_count = 0
        object_count = 0
        for triple in triples:
            subject_count += int(triple[0] == bnode)
            object_count += int(triple[2] == bnode)
        return (subject_count, object_count)

    def _metasignature(self, signatures):
        metasignature = defaultdict(int)
        for triples in signatures.values():
            for triple in triples:
                metasignature[triple] += 1
        return metasignature

    def _subgraph_bnode_comparator(self, a_signature, b_signature):
        if len(a_signature) <= len(b_signature):
            for a_triple in a_signature:
                for b_triple in b_signature:
                    if self._subgraph_triple_comparator(a_triple, b_triple):
                        break
                else:
                    return False
            return True
        else:
            return False
            
    def _subgraph_triple_comparator(self, a_triple, b_triple):
        for a_term, b_term in zip(a_triple, b_triple):
            if isinstance(a_term, tuple) and isinstance(b_term, tuple):
                for a_count, b_count in zip(a_term, b_term):
                    if a_count > b_count:
                        return False
            elif a_term != b_term:
                return False
        return True

    def _bnode_bijections(self, a_signatures, b_signatures,
                          comparator=operator.eq):
        candidates = defaultdict(set)
        for a_bnode, a_signature in a_signatures.items():
            for b_bnode, b_signature in b_signatures.items():
                if comparator(a_signature, b_signature):
                    candidates[a_bnode].add(b_bnode)

        product_args = [[(a_bnode, b_bnode) for b_bnode in b_bnodes]
                        for a_bnode, b_bnodes in candidates.items()]
        for pairs in product(*product_args):
            bijection = {}
            for a_bnode, b_bnode in pairs:
                if a_bnode not in bijection:
                    bijection[a_bnode] = b_bnode
                else:
                    break
            else:
                yield bijection

    def _apply_bijection(self, bijection, triples):
        for subject, predicate, object_ in triples:
            if isinstance(subject, BlankNode):
                subject = bijection[subject]
            if isinstance(object_, BlankNode):
                object_ = bijection[object_]
            yield (subject, predicate, object_)

