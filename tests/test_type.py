import unittest

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.semantics.type import Type, TypeDescriptor, \
    PlainLiteralType, TypedLiteralType, ContainerMembershipPropertyType
from rdf.semantics.rule import Context
from rdf.namespace import RDF, XSD


class TestType(unittest.TestCase):
    def setUp(self):
        self.predicates = Type(URI)
        self.subjects = Type((URI, BlankNode))
        self.context = Context()

    def test_is_type(self):
        self.assert_(isinstance(self.predicates, Type))

    def test_uri_instance_in_uri_type(self):
        self.assert_(URI('test') in self.predicates)

    def test_blank_node_instance_not_in_uri_type(self):
        self.assert_(BlankNode() not in self.predicates)

    def test_uri_instance_not_in_uri_and_blank_node_type(self):
        self.assert_(URI('test') in self.subjects)

    def test_blank_node_instance_in_uri_and_blank_node_type(self):
        self.assert_(BlankNode() in self.subjects)

    def test_literal_instance_not_in_uri_and_blank_node_type(self):
        self.assert_(PlainLiteral("test") not in self.subjects)

    def test_has_blank_node_type_descriptor(self):
        self.assert_(isinstance(self.predicates.blank_node, TypeDescriptor))
        self.assert_(self.predicates.blank_node is self.predicates.nnn)

    def test_calling_blank_node_with_instance_returns_blank_node(self):
        bnode = self.predicates.blank_node(URI('test'), self.context)
        self.assert_(isinstance(bnode, BlankNode))

    def test_calling_blank_node_on_same_instance_returns_same_blank_node(self):
        bnode_1 = self.subjects.blank_node(URI('test'), self.context)
        bnode_2 = self.subjects.blank_node(URI('test'), self.context)
        self.assertEqual(bnode_1, bnode_2)

    def test_calling_blank_node_with_different_context_returns_different_blank_node(self):
        context = Context()
        bnode_1 = self.subjects.blank_node(URI('test'), self.context)
        bnode_2 = self.subjects.blank_node(URI('test'), context)
        self.assertNotEqual(bnode_1, bnode_2)

    def test_types_are_orderable(self):
        self.subjects < self.predicates
        self.subjects > self.predicates

    def test_type_ordering_is_consistent(self):
        self.assertEqual(self.subjects < self.predicates,
                         self.predicates > self.subjects)
        self.assertEqual(self.subjects > self.predicates,
                         self.predicates < self.subjects)
        self.assertNotEqual(self.subjects < self.predicates,
                            self.subjects > self.predicates)
        self.assertNotEqual(self.predicates > self.subjects,
                            self.predicates < self.subjects)

class TestTypedLiteralType(unittest.TestCase):
    def setUp(self):
        self.type = TypedLiteralType()
        self.string_type = TypedLiteralType(XSD.string)
        self.literal_descriptor = self.string_type.literal()
        self.context = Context()

    def test_matches_only_typed_literals(self):
        self.assertFalse(BlankNode() in self.type)
        self.assertFalse(URI('test') in self.type)
        self.assertFalse(PlainLiteral('1.5') in self.type)
        self.assertFalse(PlainLiteral('1.5', 'en') in self.type)
        self.assert_(TypedLiteral('1.5', XSD.float) in self.type)
        self.assert_(TypedLiteral('1.5', XSD.string) in self.type)

    def test_datatype_contrains_matched_literals(self):
        self.assertFalse(TypedLiteral('1.5', XSD.float) in self.string_type)
        self.assert_(TypedLiteral('1.5', XSD.string) in self.string_type)

    def test_has_datatype_type_descriptor(self):
        self.assert_(isinstance(self.type.datatype, TypeDescriptor))
        self.assert_(self.type.datatype is self.type.ddd)

    def test_calling_datatype_with_instance_returns_datatype(self):
        literal = TypedLiteral('1.5', XSD.float)
        self.assertEqual(self.type.datatype(literal, self.context),
                         XSD.float)

    def test_calling_literal_returns_descriptor(self):
        self.assert_(isinstance(self.literal_descriptor, TypeDescriptor))

    def test_calling_literal_descriptor_returns_plain_literal(self):
        literal = TypedLiteral('1.5', XSD.float)
        self.assertEqual(self.literal_descriptor(literal, self.context),
                         PlainLiteral('1.5'))

    def test_calling_literal_descriptor_with_datatype_returns_typed_literal(self):
        literal = PlainLiteral('1.5')
        literal_descriptor = self.string_type.literal(XSD.decimal)
        self.assertEqual(literal_descriptor(literal, self.context),
                         TypedLiteral('1.5', XSD.decimal))

class TestContainerMembershipPropertyType(unittest.TestCase):
    def setUp(self):
        self.cmp = ContainerMembershipPropertyType()

    def test_is_type(self):
        self.assert_(isinstance(self.cmp, Type))

    def test_cmp_uri_instance_in_type(self):
        self.assert_(RDF._0 in self.cmp)
        self.assert_(RDF._1 in self.cmp)
        self.assert_(RDF._42 in self.cmp)

    def test_cmp_uri_literal_not_in_type(self):
        self.assert_(PlainLiteral(str(RDF._1)) not in self.cmp)

    def test_blanknode_not_in_type(self):
        self.assert_(BlankNode() not in self.cmp)

