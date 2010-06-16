import unittest

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.semantics.type import Type, TypeDescriptor, \
    TypedLiteralType, ContainerMembershipPropertyType
from rdf.namespace import RDF, XSD


class TestType(unittest.TestCase):
    def setUp(self):
        self.predicates = Type(URI)
        self.subjects = Type((URI, BlankNode))

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
        bnode = self.predicates.blank_node(URI('test'))
        self.assert_(isinstance(bnode, BlankNode))

    def test_calling_blank_node_on_same_instance_returns_same_blank_node(self):
        bnode_1 = self.subjects.blank_node(URI('test'))
        bnode_2 = self.subjects.blank_node(URI('test'))
        self.assertEqual(bnode_1, bnode_2)

class TestTypedLiteralType(unittest.TestCase):
    def setUp(self):
        self.typed_literal = TypedLiteralType()

    def test_has_datatype_type_descriptor(self):
        self.assert_(isinstance(self.typed_literal.datatype, TypeDescriptor))
        self.assert_(self.typed_literal.datatype is self.typed_literal.ddd)

    def test_calling_datatype_with_instance_returns_datatype(self):
        literal = TypedLiteral('1.5', XSD.float)
        self.assertEqual(self.typed_literal.datatype(literal), XSD.float)

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

