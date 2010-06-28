import unittest
import operator
from collections import defaultdict
from itertools import product

from rdf.uri import URI
from rdf.blanknode import BlankNode
from rdf.literal import Literal, PlainLiteral, TypedLiteral
from rdf.namespace import Namespace, RDF, RDFS, XSD
from rdf.exceptions import UnsupportedDatatype, IllTypedLiteral

from util import EX


class Type:
    def __init__(self, class_set):
        self.class_set = class_set

    def contains(self, obj):
        return isinstance(obj, tuple(self.class_set))


class ContainerMembershipPropertyType(Type):
    def __init__(self):
        super().__init__({URI})

    def contains(self, obj):
        if super().contains(obj):
            head, sep, tail = obj.rpartition('_')
            return head == RDF and not tail.startswith('0') and tail.isdigit()
        return False


class DatatypeComparator:
    def __call__(self, a, b):
        try:
            return a.value() == b.value()
        except (UnsupportedDatatype, IllTypedLiteral):
            return False


TOKEN_COMPARATOR = operator.eq
TYPE_COMPARATOR = Type.contains
DATATYPE_COMPARATOR = DatatypeComparator()


class TestType(unittest.TestCase):
    def setUp(self):
        self.uuu = Type({URI, BlankNode})
        self.aaa = Type({URI})
        self.xxx = Type({URI, BlankNode, Literal})

    def test_is_type(self):
        self.assert_(isinstance(self.uuu, Type))
        self.assert_(isinstance(self.aaa, Type))
        self.assert_(isinstance(self.xxx, Type))

    def test_contains_instances_of_classes_in_class_set(self):
        uri = EX.test
        bnode = BlankNode()
        literal = Literal("cat")
        self.assert_(self.uuu.contains(uri))
        self.assert_(self.uuu.contains(bnode))
        self.assertFalse(self.uuu.contains(literal))
        self.assert_(self.aaa.contains(uri))
        self.assertFalse(self.aaa.contains(bnode))
        self.assertFalse(self.aaa.contains(literal))
        self.assert_(self.xxx.contains(uri))
        self.assert_(self.xxx.contains(bnode))
        self.assert_(self.xxx.contains(literal))


class TestContainerMembershipPropertyType(unittest.TestCase):
    def setUp(self):
        self.cmp = ContainerMembershipPropertyType()

    def test_is_type(self):
        self.assert_(isinstance(self.cmp, Type))

    def test_does_not_contain_nonmatching_uris(self):
        self.assertFalse(self.cmp.contains(EX['22-rdf-syntax-ns#_1']))
        self.assertFalse(self.cmp.contains(RDF.type))
        self.assertFalse(self.cmp.contains(RDF._))

    def test_does_not_contain_literals(self):
        self.assertFalse(self.cmp.contains(PlainLiteral("cat")))
        self.assertFalse(self.cmp.contains(TypedLiteral("10", XSD.decimal)))

    def test_does_not_contain_bnodes(self):
        self.assertFalse(self.cmp.contains(BlankNode()))

    def test_contains_member_counter_uris(self):
        self.assert_(self.cmp.contains(RDF._1))
        self.assert_(self.cmp.contains(RDF._42))
        self.assert_(self.cmp.contains(RDF._9876543210))

    def test_member_counter_must_be_numeric(self):
        self.assertFalse(self.cmp.contains(RDF._x))
    
    def test_member_counter_must_be_greater_than_zero(self):
        self.assertFalse(self.cmp.contains(RDF._0))
        self.assertFalse(self.cmp.contains(RDF['_-1']))

    def test_member_counter_must_not_have_leading_zeros(self):
        self.assertFalse(self.cmp.contains(RDF._01))
        self.assertFalse(self.cmp.contains(RDF._0042))


class Pattern(frozenset):
    def find(self, graph):
        bindings = defaultdict(list)
        for pattern in self:
            for triple in graph:
                binding = {}
                for type_, token in zip(pattern, triple):
                    type_ = binding.get(type_, type_)
                    if self.compare(type_, token):
                        binding[type_] = token
                    else:
                        break
                else:
                    bindings[pattern].append(binding)
            if pattern not in bindings:
                break
        if len(bindings) == len(self):
            for candidate_bindings in product(*bindings.values()):
                merged_binding = {}
                for binding in candidate_bindings:
                    for type_, token in binding.items():
                        merged_token = merged_binding.setdefault(type_, token)
                        if merged_token != token:
                            break
                    else:
                        continue
                    break
                else:
                    yield merged_binding

    def compare(self, type_, token):
        if isinstance(type_, Type):
            return TYPE_COMPARATOR(type_, token)
        elif not TOKEN_COMPARATOR(type_, token):
            if (isinstance(type_, TypedLiteral) and
                isinstance(token, TypedLiteral) and
                DATATYPE_COMPARATOR(type_, token)):
                return True
            return False
        return True
        

class TestPattern(unittest.TestCase):
    def setUp(self):
        self.uuu = Type({URI, BlankNode})
        self.aaa = Type({URI})
        self.xxx = Type({URI, BlankNode, Literal})
        self.pattern = Pattern({(self.uuu, self.aaa, self.xxx)})

    def test_is_pattern(self):
        self.assert_(isinstance(self.pattern, Pattern))

    def test_find_yields_valid_matches(self):
        triples = {(1, EX.prop, "foo"),
                   (EX.a, EX.prop, Literal("bar")),
                   (BlankNode('x'), RDF.type, BlankNode('y')),
                   (EX.b, BlankNode(), EX.c)}
        matches = list(self.pattern.find(triples))
        self.assertEqual(len(matches), 2)
        self.assert_({self.uuu: EX.a,
                      self.aaa: EX.prop,
                      self.xxx: Literal("bar")} in matches)
        self.assert_({self.uuu: BlankNode('x'),
                      self.aaa: RDF.type,
                      self.xxx: BlankNode('y')} in matches)

if __name__ == '__main__':
    unittest.main()   

